#include <algorithm>
#include <iostream>
#include <vector>
#include <array>

const int DIGITS = 4;

std::array<unsigned int, DIGITS> depthbuffer;
std::array<unsigned int, 10> startfrom = {1,0,2,3,7,9,8,4,5,6};
std::vector<std::vector<unsigned int>> priority = { // this *can* be removed but its helpful
    {}, // 0 digits
    {}, // 1 digits
    {},
    {},
    {4321,6767,6969,1337},
    {12345,54321},
    {123456,654321},
    {1234567,7654321},
    {12345678,87654321},
    {123456789,987654321},
};

std::array<std::array<unsigned int, 10>, 10> entropies = {{
    {0, 8, 1, 7, 9, 3, 2, 4, 5, 6},
    {1, 2, 0, 4, 9, 5, 3, 7, 6, 8},
    {2, 1, 3, 0, 5, 4, 6, 7, 9, 8},
    {3, 2, 4, 6, 5, 0, 1, 7, 9, 8},
    {4, 3, 5, 1, 7, 2, 8, 0, 9, 6},
    {5, 4, 6, 2, 8, 1, 3, 7, 9, 0},
    {6, 5, 7, 3, 9, 2, 8, 0, 1, 4},
    {7, 6, 8, 4, 0, 3, 5, 1, 9, 2},
    {8, 7, 9, 0, 5, 4, 6, 1, 3, 2},
    {9, 8, 6, 0, 5, 1, 3, 7, 2, 4}
}};

void send_pwd(unsigned int pwd) {
    std::cout << pwd << std::endl;
}

int next_perimiter(int two_ago, int fromdigit) {
    if ((fromdigit == 4 || fromdigit == 6) && two_ago == 8) {
        return 2;
    } else if ((fromdigit == 4 || fromdigit == 6) && two_ago == 2) { 
        return 8;
    } else if ((fromdigit == 2 || fromdigit == 8) && two_ago == 6) {
        return 4;
    } else if ((fromdigit == 2 || fromdigit == 8) && two_ago == 4) {
        return 6;
    } else {
        return -1;
    }
}

void find_sums(int length, int target_sum, int max_val, int current_idx, void (*callback)(const std::array<unsigned int, DIGITS>&, int)) {
    if (length == 1) {
        if (target_sum >= 0 && target_sum <= max_val) {
            depthbuffer[current_idx] = static_cast<unsigned int>(target_sum);
            callback(depthbuffer, current_idx + 1);
        }
        return;
    }

    int limit = std::min(target_sum, max_val);
    for (int val = 0; val <= limit; ++val) {
        depthbuffer[current_idx] = static_cast<unsigned int>(val);
        find_sums(length - 1, target_sum - val, max_val, current_idx + 1, callback);
    }
}

void process_combinations(int length, int max_val, void (*callback)(const std::array<unsigned int, DIGITS>&, int)) {
    for (int target_sum = 0; target_sum <= (length * max_val); ++target_sum) {
        find_sums(length, target_sum, max_val, 0, callback);
    }
}

unsigned int get_likely_follow(int depth, unsigned int history) {
    unsigned int entropy10 = depthbuffer[depth];
    if (depth == 0) return startfrom[entropy10];

    bool has_history = depth > 1;
    int two_ago = (history / 10) % 10;
    int fromdigit = history % 10;
    std::vector<unsigned int> candidates(entropies[fromdigit].begin(),entropies[fromdigit].end());

    auto get_bonus = [&](unsigned int d) -> int {
        int next_perimiter_result = has_history && next_perimiter(two_ago, fromdigit) || -1;
        int bonus = 0;
        int temp_h = static_cast<int>(history);

        if (has_history && d == two_ago) {
            bonus -= 15;
        } else if (has_history && (fromdigit - two_ago) == (static_cast<int>(d) - fromdigit)) {
            bonus -= 10;
        } else if (next_perimiter_result != -1 && d == next_perimiter_result) {
            bonus -= 10;
        }
        if (DIGITS == 4 && (1930 <= history && history <= 2030)) {
            bonus -= 15;
        }
        while (temp_h > 0) {
            if (d == (temp_h % 10)) bonus -= 2;
            temp_h /= 10;
        }
        return bonus;
    };

    std::vector<size_t> indices(candidates.size());
    for (size_t i = 0; i < 10; ++i) indices[i] = i;

    std::stable_sort(indices.begin(), indices.end(), [&](size_t i, size_t j) {
        int score_i = static_cast<int>(i) + get_bonus(candidates[i]);
        int score_j = static_cast<int>(j) + get_bonus(candidates[j]);
        if (score_i != score_j) return score_i < score_j;
        return i < j;
    });

    // 6. Return the digit at the specified entropy index
    return candidates[indices[entropy10]];
}

void send_next_pwd(const std::array<unsigned int, DIGITS>& combo, int length) {
    unsigned int pwd = 0;
    for (int i = 0; i < DIGITS; ++i) {
        unsigned int digit = get_likely_follow(i, pwd);
        pwd = pwd * 10 + digit;
    }

    if (std::find(priority[DIGITS].begin(), priority[DIGITS].end(), pwd) != priority[DIGITS].end()) return; else send_pwd(pwd);
}

int main() {
    for (unsigned int ppwd : priority[DIGITS]) send_pwd(ppwd); // Check prioritized PINs first
    process_combinations(DIGITS, 9, send_next_pwd);

    return 0;
}