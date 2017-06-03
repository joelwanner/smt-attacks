__SEPARATOR = "=============================================="
__SUBSEP = "----------------------------------------------"


def print_header(title, subtitle=None):
    print(__SEPARATOR)
    print(title)
    if subtitle:
        print(subtitle)
    print(__SEPARATOR)


def print_subsep():
    print(__SUBSEP)
