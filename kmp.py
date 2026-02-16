#!/usr/bin/python3


def get_prefix(string: str) -> list:
    prefix = []
    for i in range(len(string) - 1):
        prefix.append(string[: i + 1])
    return prefix


def get_suffix(string: str) -> list:
    suffix = []
    for i in range(len(string) - 1):
        suffix.append(string[i + 1 :])
    return suffix


def get_common(prefix: list, suffix: list) -> set:
    common = set(prefix) & set(suffix)
    if len(common) == 0:
        common_len = 0
    else:
        common_len = len(max(common))
    return common_len


def get_table(string: str) -> dict:
    table = []
    for i in range(len(string)):
        sub = string[0 : i + 1]
        prefix = get_prefix(sub)
        suffix = get_suffix(sub)
        common = get_common(prefix, suffix)
        table.append(common)
    return table


def get_table2(pattern: str):
    table = [0]
    i = 1
    j = 0
    k = 0
    while i < len(pattern):
        if pattern[j] == pattern[i]:
            i += 1
            j += 1
            k += 1
        else:
            i += 1
            k = 0
        table.append(k)
    return table


def kmp(string: str, pattern: str):
    print("char", string)
    print("pattern", list(pattern))
    table = get_table(pattern)
    table2 = get_table2(pattern)
    print("table", table)
    print("table2", table2)
    s_len = len(string)
    p_len = len(pattern)
    i = 0
    j = 0
    while i < s_len:
        if string[i] == pattern[j]:
            i += 1
            j += 1
        if j == p_len:
            index = i - j
            print("found at ", index)
            return index
        if string[i] != pattern[j]:
            if j == 0:
                i += 1
            else:
                j = table[j - 1]
    print("Not found")
    return -1


def main():
    string = "asdfjkkllzxcxvzxzxccvasdujjjaszxzxzxccdfghh"
    a = "zxzxzxc"
    # b = 'xcvacv'
    b = "abababca"
    index = kmp(string, a)
    print("answer", string.index(a))


main()
