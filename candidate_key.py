import itertools


def find_closure(fd, attr):
    closure = set(attr)

    while True:
        new_elements = set()
        for lhs, rhs in fd:
            if set(lhs).issubset(closure):
                new_elements.update(rhs)
        if new_elements.issubset(closure):
            break
        closure.update(new_elements)
    
    return set(sorted(closure))

def prepare_lmr_matrix(r, fd):
    lmr = {"l": set(), "m": set(), "r": set()}
    for lhs, rhs in fd:
        if lhs not in lmr["m"]:
            lmr["l"].update(lhs)
        if rhs not in lmr["m"]:
            lmr["r"].update(rhs)
        
        if lhs in lmr["r"]:
            lmr["l"].remove(lhs)
            lmr["r"].remove(lhs)
            lmr["m"].update(lhs)
        if rhs in lmr["l"]:
            lmr["l"].remove(rhs)
            lmr["r"].remove(rhs)
            lmr["m"].update(rhs)
        
    lmr["l"] = sorted(lmr["l"])
    lmr["m"] = sorted(lmr["m"])
    lmr["r"] = sorted(lmr["r"])
    
    return lmr

def generate_combinations(s):
    combinations = []
    for i in range(1, len(s) + 1):
        combinations.extend([''.join(comb) for comb in itertools.combinations(s, i)])
    return combinations

def find_ck(r, fd):
    ck = set()
    lmr = prepare_lmr_matrix(r, fd)

    left = ""
    for attr in r:
        if attr not in lmr["l"] + lmr["m"] + lmr["r"]:
            left += attr

    posssible_ck = generate_combinations("".join(lmr["l"] + lmr["m"]))

    length = 999
    for key in posssible_ck:
        if len(key) > length:
            break
        if set(find_closure(fd, key)) == set(lmr["l"] + lmr["m"] + lmr["r"]):
            ck.add(key+left)
            length = len(key)

    return sorted(ck)


if __name__ == '__main__':
    r = {"A", "B", "C", "D", "E", 'H'}
    fd = [
        ("A", "D"),
        ("C", "B"),
        ("E", "A"),
        ("E", "D"),
        ("BC", "A"),
        ("BC", "D"),
    ]
    attr = "C"
    
    print(find_closure(fd, attr))