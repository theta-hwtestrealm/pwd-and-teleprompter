#T9 DETERMINISTIC PASSCODE LOW-RAM ENVIRONMENT LOGIC + PROBABILITY GRAPH
#Where each index is a digit, the value is its most likely next digit

# 1 2 3
# 4 5 6
# 7 8 9
# X 0 X

# 1,3,7,0,9 are corner keys

#same key = always 0 entropy
#increment/decrement always 1 entropy except to/from 0 (2 entropy)
#distanced corner keys are 4 entropy (unless inc/dec or nearby)
#2->0 and 1->9 is 2 entropy due to 2000s and 1900s
#distanced non-corner key 5 entropy
#nearby key is 2 entropy (diagonal, 3 entropy)

import numpy as np

test_pwd = 5253 # show the security level of this password <---
digits = 4 #standard length <---

tries = 0
depthlist = [0] * digits
startfrom = [1,0,2,3,7,9,8,4,5,6] #most likely start digits
important = [# this can be removed if it is too cluttered, it is just common passwords to try first
    [], # 0 digit
    [], # 1 digit
    [], # 2 digit
    [], # 3 digit
    [4321,6767,6969,1337],  #4 digit common keys that should be tried first. 1234 is excluded here because it will be immediatelty tried in the main logic
    [12345,54321],  #5 digit common keys that should be tried first
    [123456,654321],  #6 digit common keys that should be tried first
    [1234567,7654321],  #7 digit common keys that should be tried first
    [12345678,87654321],  #8 digit common keys that should be tried first
    [123456789,987654321],  #9 digit common keys that should be tried first
]
entropies = np.array([
    [
        0,  # 0 -> 0 |same number is *always* 0 entropy
        2,  # 0 -> 1 |distanced increment 2 entropy
        5,  # 0 -> 2 |0 is far from 2
        4,  # 0 -> 3 |0 is far from 3, but is a corner number
        5,  # 0 -> 4 |0 is far from 4
        5,  # 0 -> 5 |0 is far from 5
        5,  # 0 -> 6 |0 is far from 6
        3,  # 0 -> 7 |diagonal key is 3 entropy
        1,  # 0 -> 8 |(special case) adjacent from 0 always 1
        3,  # 0 -> 9 |diagonal key is 3 entropy
    ],
    [
        2,  # 1 -> 0 |distanced decrement 2 entropy
        0,  # 1 -> 1 |same number is *always* 0 entropy
        1,  # 1 -> 2 |increment 1 entropy
        4,  # 1 -> 3 |1 is far from 3, but 3 is a corner number
        2,  # 1 -> 4 |adjacent key is 2 entropy
        3,  # 1 -> 5 |diagonal key is 3 entropy
        5,  # 1 -> 6 |1 is far from 6
        4,  # 1 -> 7 |1 is far from 7, but 7 is a corner number
        5,  # 1 -> 8 |1 is far from 8
        2,  # 1 -> 9 |(special case) 1->9 is 2 entropy due to 1900s
    ],
    [
        2,  # 2 -> 0 |(special case) 2->0 is 2 entropy due to 2000s years
        1,  # 2 -> 1 |decrement 1 entropy
        0,  # 2 -> 2 |same number is *always* 0 entropy
        1,  # 2 -> 3 |increment 1 entropy
        3,  # 2 -> 4 |diagonal key is 3 entropy
        2,  # 2 -> 5 |adjacent key is 2 entropy
        3,  # 2 -> 6 |diagonal key is 3 entropy
        4,  # 2 -> 7 |2 is far from 7, but 7 is a corner number
        5,  # 2 -> 8 |2 is far from 8
        4,  # 2 -> 9 |2 is far from 9, but 9 is a corner number
    ],
    [
        4,  # 3 -> 0 |3 is far away from 0, but 0 is a corner number
        4,  # 3 -> 1 |3 is far away from 1, but 1 is a corner number
        1,  # 3 -> 2 |decrement 1 entropy
        0,  # 3 -> 3 |same number is *always* 0 entropy
        1,  # 3 -> 4 |increment 1 entropy
        3,  # 3 -> 5 |diagonal key is 3 entropy
        2,  # 3 -> 6 |adjacent key is 2 entropy
        4,  # 3 -> 7 |3 is far away from 7, but 7 is a corner number
        5,  # 3 -> 8 |3 is far away from 8
        4,  # 3 -> 9 |3 is far away from 9, but 9 is a corner number
    ],
    [
        4,  # 4 -> 0 |4 is far away from 0, but 0 is a corner number
        2,  # 4 -> 1 |adjacent key is 2 entropy
        3,  # 4 -> 2 |diagonal key is 3 entropy
        1,  # 4 -> 3 |decrement 1 entropy
        0,  # 4 -> 4 |same number is *always* 0 entropy
        1,  # 4 -> 5 |increment 1 entropy
        5,  # 4 -> 6 |4 is far away from 6
        2,  # 4 -> 7 |adjacent key is 2 entropy
        3,  # 4 -> 8 |diagonal key is 3 entropy
        4,  # 4 -> 9 |4 is far away from 9, but 9 is a corner number
    ],
    [
        4,  # 5 -> 0 |5 is far away from 0, but 0 is a corner number
        3,  # 5 -> 1 |diagonal key is 3 entropy
        2,  # 5 -> 2 |adjacent key is 2 entropy
        3,  # 5 -> 3 |diagonal key is 3 entropy
        1,  # 5 -> 4 |decrement 1 entropy
        0,  # 5 -> 5 |same number is *always* 0 entropy
        1,  # 5 -> 6 |increment 1 entropy
        3,  # 5 -> 7 |diagonal key is 3 entropy
        2,  # 5 -> 8 |adjacent key is 2 entropy
        3,  # 5 -> 9 |diagonal key is 3 entropy
    ],
    [
        4,  # 6 -> 0 |6 is far away from 0, but 0 is a corner number
        4,  # 6 -> 1 |6 is far away from 1, but 1 is a corner number
        3,  # 6 -> 2 |diagonal key is 3 entropy
        2,  # 6 -> 3 |adjacent key is 2 entropy
        5,  # 6 -> 4 |6 is far away from 4
        1,  # 6 -> 5 |increment 1 entropy
        0,  # 6 -> 6 |same number is *always* 0 entropy
        1,  # 6 -> 7 |increment 1 entropy
        3,  # 6 -> 8 |diagonal key is 3 entropy
        2,  # 6 -> 9 |adjacent key is 2 entropy
    ],
    [
        3,  # 7 -> 0 |diagonal key is 3 entropy
        4,  # 7 -> 1 |7 is far from 1, but 1 is a corner number
        5,  # 7 -> 2 |7 is far from 2
        3,  # 7 -> 3 |7 is far from 3, but 3 is a corner number
        2,  # 7 -> 4 |adjacent key is 2 entropy
        3,  # 7 -> 5 |diagonal key is 3 entropy
        1,  # 7 -> 6 |decrement 1 entropy
        0,  # 7 -> 7 |same number is *always* 0 entropy
        1,  # 7 -> 8 |increment 1 entropy
        4,  # 7 -> 9 |7 is far from 9, but 9 is a corner number
    ],
    [
        2, #8 -> 0 |adjacent key is 2 entropy
        4, #8 -> 1 |8 is far from 1, but 1 is a corner number
        5, #8 -> 2 |8 is far from 2
        4, #8 -> 3 |8 is far from 3, but 3 is a corner number
        3, #8 -> 4 |diagonal key is 3 entropy
        2, #8 -> 5 |adjacent key is 2 entropy
        3, #8 -> 6 |diagonal key is 3 entropy
        1, #8 -> 7 |decrement 1 entropy
        0, #8 -> 8 |same number is *always* 0 entropy
        1, #8 -> 9 |increment 1 entropy
    ],
    [
        3,  # 9 -> 0 |diagonal key is 3 entropy
        4,  # 9 -> 1 |9 is far from 1, but 1 is a corner number
        5,  # 9 -> 2 |9 is far from 2
        4,  # 9 -> 3 |9 is far from 3, but 3 is a corner number
        5,  # 9 -> 4 |9 is far from 4
        3,  # 9 -> 5 |diagonal key is 3 entropy
        2,  # 9 -> 6 |adjacent key is 2 entropy
        4,  # 9 -> 7 |9 is far from 7, but 7 is a corner number
        1,  # 9 -> 8 |decrement 1 entropy
        0,  # 9 -> 9 |same number is *always* 0 entropy
    ],
], dtype=np.int8)
precalculated = np.argsort(entropies, axis=1, kind='stable')
del entropies

def send_pwd(pwd):
    print("Sending passcode:", f"{pwd:0{digits}d}")

def next_perimiter(two_ago, fromdigit):
    if two_ago is None:
        return None
    elif (fromdigit == 4 or fromdigit == 6) and two_ago == 8:
        return 2
    elif (fromdigit == 4 or fromdigit == 6) and two_ago == 2:
        return 8
    elif (fromdigit == 2 or fromdigit == 8) and two_ago == 6:
        return 4
    elif (fromdigit == 2 or fromdigit == 8) and two_ago == 4:
        return 6
    else:
        return None
    

def get_combinations_by_sum(length, max_val):
    for target_sum in range((length * max_val) + 1):
        yield from _find_sums(length, target_sum, max_val)

def _find_sums(length, target_sum, max_val):
    if length == 1:
        if 0 <= target_sum <= max_val:
            yield [target_sum]
        return

    for val in range(min(target_sum, max_val) + 1):
        for rest in _find_sums(length - 1, target_sum - val, max_val):
            yield [val] + rest

def get_likely_follow(cdepth,history):
    centropy10 = depthlist[cdepth]

    if cdepth == 0:
        return startfrom[centropy10]
    
    two_ago = (history // 10) % 10 if cdepth > 1 else None
    fromdigit = history % 10
    candidates = precalculated[fromdigit].tolist()

    def get_bonus(d):
        next_perimiter_result = next_perimiter(two_ago, fromdigit)
        temp_h = history
        bonus = 0
        if d == two_ago: #give oscillations a lower entropy
            bonus -= 15
        elif two_ago is not None and (fromdigit - two_ago) == (d - fromdigit): # give runs of increments/decrements lower entropy
            bonus -= 10
        elif next_perimiter_result is not None and d == next_perimiter_result: # give circular patterns lower entropy
            bonus -= 10
        if digits == 4 and (1930 <= history <= 2030):
            bonus -= 15
        while temp_h > 0: # lower entropy for digits that have already appeared
            if d == temp_h % 10: bonus -= 2
            temp_h //= 10

        return bonus
    
    adjusted = sorted(
        candidates, 
        key=lambda d: (candidates.index(d) + get_bonus(d), candidates.index(d))
    )

    return adjusted[centropy10]

def get_next_pwd():
    pwd = 0

    for i in range(0,digits):
        digit = get_likely_follow(i,pwd)
        pwd = pwd * 10 + digit

    return pwd

pwd_reached_at = 0
#print(precalculated)


for imp_pwd in important[digits]:
    send_pwd(imp_pwd)
    tries += 1

for combination in get_combinations_by_sum(digits, 9):
    #print(combination)
    depthlist = combination
    pwd = get_next_pwd()

    if pwd in important[digits]: 
        continue

    if tries: # < 100
        send_pwd(pwd)
    tries += 1

    
    if pwd == test_pwd:
        pwd_reached_at = tries
        break #include this line to stop at the test password, and you will also be able to see other passwords of a similar security level

print(f"{test_pwd:0{digits}d} is the {pwd_reached_at}th'nd'st password guessed out of {10**digits} total. (~{(pwd_reached_at/10**digits)*100:.2f}% relative security)")