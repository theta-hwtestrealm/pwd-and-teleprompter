import numpy as np

digits = 4 #standard length <---
depthlist = [0] * digits
startfrom = [1,0,2,3,7,9,8,4,5,6] #most likely start digits
precalculated = np.array([
    [0, 8, 1, 7, 9, 3, 2, 4, 5, 6],
    [1, 2, 0, 4, 9, 5, 3, 7, 6, 8],
    [2, 1, 3, 0, 5, 4, 6, 7, 9, 8],
    [3, 2, 4, 6, 5, 0, 1, 7, 9, 8],
    [4, 3, 5, 1, 7, 2, 8, 0, 9, 6],
    [5, 4, 6, 2, 8, 1, 3, 7, 9, 0],
    [6, 5, 7, 3, 9, 2, 8, 0, 1, 4],
    [7, 6, 8, 4, 0, 3, 5, 1, 9, 2],
    [8, 7, 9, 0, 5, 4, 6, 1, 3, 2],
    [9, 8, 6, 0, 5, 1, 3, 7, 2, 4]
], dtype=np.int8)

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
    
    two_ago = (history // 10) % 10 if history >= 10 else None
    fromdigit = history % 10
    candidates = precalculated[fromdigit].tolist()

    def get_bonus(d):
        temp_h = history
        bonus = 0
        if d == two_ago: #give oscillations a lower entropy (2525,4545)
            bonus -= 15
        elif two_ago is not None and (fromdigit - two_ago) == (d - fromdigit): # give runs of increments/decrements lower entropy
            bonus -= 10
        while temp_h > 0: # lower entropy for digits that have already appeared
            if d == temp_h % 10: bonus -= 2
            temp_h //= 10
        return bonus
    
    adjusted = sorted(candidates, key=lambda d: (candidates.index(d) + get_bonus(d), candidates.index(d)))

    return adjusted[centropy10]

def get_next_pwd():
    pwd = 0
    for i in range(0,digits):
        digit = get_likely_follow(i,pwd)
        pwd = pwd * 10 + digit

    return pwd

tries = 0
for combination in get_combinations_by_sum(digits, 9):
    depthlist = combination
    pwd = get_next_pwd()
    tries += 1
    input(f"[Prompt #{tries}] {pwd:0{digits}d}")
