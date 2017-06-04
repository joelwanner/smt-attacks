__SEPARATOR = "=========================================================="
__SUBSEP = "----------------------------------------------------------"


def __print_header(title, subtitle, separator):
    print(separator)
    print(title)
    if subtitle:
        print(subtitle)
    print(separator)


def print_header(title, subtitle=None):
    __print_header(title, subtitle, __SEPARATOR)


def print_subheader(title, subtitle=None):
    __print_header(title, subtitle, __SUBSEP)


def print_sep():
    print(__SEPARATOR)


def print_subsep():
    print(__SUBSEP)
