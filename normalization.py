import candidate_key

def check_2NF(r, fd):
    result = {
        "ck": set(),
        "np": set(),
        "violating_fds": []
    }
    
    cks = candidate_key.find_ck(r, fd)
    for ck in cks:
        for attr in ck:
            result["ck"].add(attr)

    result["ck"] = set(result["ck"])
    result["np"] = r - result["ck"]

    for lhs, rhs in fd:
        for ck in cks:
            if set(lhs).issubset(set(ck)) and set(lhs) != set(ck):
                if set(rhs).intersection(result["np"]):
                    result["violating_fds"].append((lhs, rhs))
    
    return result


def check_3NF(r, fd):
    result = {
        "ck": set(),
        "np": set(),
        "violating_fds": []
    }

    cks = candidate_key.find_ck(r, fd)
    for ck in cks:
        for attr in ck:
            result["ck"].add(attr)

    result["ck"] = set(result["ck"])
    result["np"] = r - result["ck"]

    for lhs, rhs in fd:
        closure = candidate_key.find_closure(fd, lhs)
        is_superkey = set(closure) >= r
        rhs_prime = set(rhs).issubset(result["ck"])

        if not (is_superkey or rhs_prime):
            result["violating_fds"].append((lhs, rhs))

    return result


if __name__ == "__main__":
    r = {"A", "B", "C", "D", "E", 'F'}
    fd = [
        ("A", "BCDEF"),
        ("BC", "ADEF"),
        ("B", "F"),
        ("D", "E"),
    ]

    print("2NF Check:", check_2NF(r, fd))
    print("3NF Check:", check_3NF(r, fd))
