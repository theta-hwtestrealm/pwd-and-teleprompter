#NUMPAD DETERMINISTIC PASSCODE LOW-RAM ENVIRONMENT LOGIC + PROBABILITY GRAPH
#Where each index is a digit, the value is its most likely next digit
#This should ideally be used in low-ram enviorments and be implemented in a target language

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

digits = 4 #standard length <---

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
    [0,2,5,4,5,5,5,3,1,3],
    [2,0,1,4,2,3,5,4,5,2],
    [2,1,0,1,3,2,3,4,5,4],
    [4,4,1,0,1,3,2,4,5,4],
    [4,2,3,1,0,1,5,2,3,4],
    [4,3,2,3,1,0,1,3,2,3],
    [4,4,3,2,5,1,0,1,3,2],
    [3,4,5,3,2,3,1,0,1,4],
    [2,4,5,4,3,2,3,1,0,1],
    [3,4,5,4,5,3,2,4,1,0],
], dtype=np.int8)
precalculated = np.argsort(entropies, axis=1, kind='stable')
del entropies

def send_pwd(pwd):
    print("Sending passcode:", f"{pwd:0{digits}d}")
    #device logic here
    #if correct answer, optionally tell the user how many attempts were made
    
def next_perimiter(two_ago, fromdigit): # look for a circular pattern
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
        if d == two_ago: #give oscillations a lower entropy (2525,4545)
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


for imp_pwd in important[digits]:
    send_pwd(imp_pwd)

for combination in get_combinations_by_sum(digits, 9):
    #print(combination)
    depthlist = combination
    pwd = get_next_pwd()

    if pwd in important[digits]: 
        continue

    send_pwd(pwd)
