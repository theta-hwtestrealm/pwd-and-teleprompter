#include <stdio.h>

#define DIGITS 4

unsigned int depthbuffer[DIGITS] = {0};
unsigned int startfrom[10] = {1,0,2,3,7,9,8,4,5,6};

unsigned int entropies[10][10] = {
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
};

void send_pwd(unsigned int pwd) {
    printf("%0*u\n", DIGITS, pwd);
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

void find_sums(int length, int target_sum, int max_val, int current_idx, void (*callback)(unsigned int *, int)) {
    if (length == 1) {
        if (target_sum >= 0 && target_sum <= max_val) {
            depthbuffer[current_idx] = (int)(target_sum);
            callback(depthbuffer, current_idx + 1);
        }
        return;
    }

    int limit = (target_sum < max_val) ? target_sum : max_val;
    for (int val = 0; val <= limit; ++val) {
        depthbuffer[current_idx] = (int)(val);
        find_sums(length - 1, target_sum - val, max_val, current_idx + 1, callback);
    }
}

int get_bonus(unsigned int d, int history, int depth) {
    int has_history = depth > 1;
    int two_ago = (history / 10) % 10;
    int fromdigit = history % 10;
    int next_perimiter_result = has_history && next_perimiter(two_ago, fromdigit) || -1;
    int bonus = 0;

    if (has_history && d == two_ago) {
        bonus -= 15;
    } else if (has_history && (fromdigit - two_ago) == ((int)(d) - fromdigit)) {
        bonus -= 10;
    } else if (next_perimiter_result != -1 && d == next_perimiter_result) {
        bonus -= 10;
    }
    if (DIGITS == 4 && (1930 <= history && history <= 2030)) {
        bonus -= 15;
    }
    while (history > 0) {
        if (d == (history % 10)) bonus -= 2;
        history /= 10;
    }
    return bonus;
};

unsigned int get_likely_follow(int depth, unsigned int history) {
    unsigned int entropy10 = depthbuffer[depth];
    if (depth == 0) return startfrom[entropy10];

    int fromdigit = history % 10;
    unsigned int candidates[10];
    int scores[10];
    int indices[10];

    for (int i = 0; i < 10; i++) {
        candidates[i] = entropies[fromdigit][i];
        indices[i] = i;
        scores[i] = i + get_bonus(candidates[i], (int)history, depth);
    }

    // Stable Insertion Sort
    for (int i = 1; i < 10; i++) {
        int key_idx = indices[i];
        int key_score = scores[i];
        int j = i - 1;
        while (j >= 0 && scores[j] > key_score) {
            indices[j + 1] = indices[j];
            scores[j + 1] = scores[j];
            j--;
        }
        indices[j + 1] = key_idx;
        scores[j + 1] = key_score;
    }

    return candidates[indices[entropy10]];
}

void send_next_pwd(unsigned int * combo, int length) {
    unsigned int pwd = 0;
    for (int i = 0; i < DIGITS; ++i) {
        unsigned int digit = get_likely_follow(i, pwd);
        pwd = pwd * 10 + digit;
    }
    send_pwd(pwd);
}

int main() {
    for (int target_sum = 0; target_sum <= (DIGITS * 9); ++target_sum) {
        find_sums(DIGITS, target_sum, 9, 0, send_next_pwd);
    }

    return 0;
}