import candidate_key


def find_minimal_cover(r, fd):
    for lhs, rhs in fd:
        if len(rhs) > 1:
            for a in rhs:
                fd.append((lhs, a))
            fd.remove((lhs, rhs))

    new_fd = fd.copy()
    for lhs, rhs in fd:
        if len(lhs) > 1:
            for a in lhs:
                if rhs in candidate_key.find_closure(fd, a):
                    new_fd.append((a, rhs))
                    new_fd.remove((lhs, rhs))
                    break
    fd = sorted(new_fd)

    for lhs, rhs in fd:
        temp_fd = fd.copy()
        temp_fd.remove((lhs, rhs))
        if rhs in candidate_key.find_closure(temp_fd, lhs):
            fd.remove((lhs, rhs))

    return fd


if __name__ == "__main__":
    r = {'A', 'B', 'C', 'D', 'E'}
    fd = [
        ("A", "BC"),
        ("D", "AB"),
    ]

    print(find_minimal_cover(r, fd))