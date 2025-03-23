import candidate_key


def check_2NF(r, fd):
    result = {}
    result["ck"] = set()
    result["np"] = set()
    result["violating_fds"] = []
    
    cks = candidate_key.find_ck(r, fd)
    for ck in cks:
        for attr in ck:
            result["ck"].add(attr)
    
    result["ck"] = "".join(sorted(result["ck"]))
    result["np"] = "".join(sorted(r - set(result["ck"])))

    for lhs, rhs in fd:
        violates = False
        if lhs == result["ck"]:
            continue
        for attr in lhs:
            if attr in result["ck"]:
                violates = True
                break
        
        if violates:
            result["violating_fds"].append((lhs, rhs))   

    return result
    


if __name__ == "__main__":
    r = {"A", "B", "C", "D", "E", 'P', "G"}
    fd = [
        ("AB", "CD"),
        ("DE", "P"),
        ("C", "E"),
        ("P", "C"),
        ("B", "G"),
        ("A", "F"),
    ]

    print(check_2NF(r, fd))