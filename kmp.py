def get_prefix(string: str) -> list:
    prefix = []
    for i in range(len(string)-1):
        prefix.append(string[:i+1])
    return prefix


def get_suffix(string: str) -> list:
    suffix = []
    for i in range(len(string)-1):
        suffix.append(string[i+1:])
    return suffix


def get_common(prefix: list, suffix: list) -> set:
    common =  set(prefix) & set(suffix)
    if len(common) == 0:
        common_len = 0
    else:
        common_len = len(max(common))
    print('\t', 'prefix', prefix, 'suffix', suffix, 'common', common)
    return common_len


def get_table(string: str) -> dict:
    table = dict()
    for i in range(len(string)):
        sub = string[0:i+1]
        prefix = get_prefix(sub)
        suffix = get_suffix(sub)
        common = get_common(prefix, suffix)
        table[i] = common
    return table


def print_table(string, table):
    print('char', string, sep='\t')
    print('index', table.keys(), sep='\t')
    print('value', table.values(), sep='\t')
    return


def main():
    string = 'asdfjkkllzxcxvzxcvasdujjjasdfghh'
    a = 'asdfas'
    # b = 'xcvacv'
    b = 'abababca'
    table = get_table(b)
    print_table(b, table)


main()
