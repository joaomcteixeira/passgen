"""
An utterly simple password generator made in Python.

By default, a password contains lower and upper case characters, digits,
and punctuation. You can disable these different types separately.

USAGE:
    $ python passgen.py -h
    $ python passgen.py
    $ python passgen.py -pu
"""
import argparse
import random
import secrets
import string
from contextlib import suppress


class _JoinDisable(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        disable = ''.join(chars for d in values for chars in d).replace(" ", "")
        setattr(namespace, self.dest, disable)


ap = argparse.ArgumentParser(description=__doc__)

ap.add_argument('-l', help='Password length. Defaults to 16.', default=16, type=int)
ap.add_argument('-lo', help='Disable lower case chars.', action="store_false")
ap.add_argument('-up', help='Disable upper case chars.', action="store_false")
ap.add_argument('-di', help='Disable digits.', action="store_false")
ap.add_argument('-pu', help='Disable punctuation.', action="store_false")
ap.add_argument(
    '-D',
    '--disable',
    help=(
        'Disable characters. Give a list of characters to disregard. '
        'For example: --disable "A B u ( )". '
        'To disable complex punctuation you might need to use the backslash: '
        '--disable "\`" for example.'
        ),
    nargs="*",
    action=_JoinDisable,
    )

chars_possibilities = {
    'lower': string.ascii_lowercase,
    'upper': string.ascii_uppercase,
    'digits': string.digits,
    'punctuation': string.punctuation,
    }


def main(l=16, lo=True, up=True, di=True, pu=True, disable=None):
    """Create a password."""
    original_len = l

    # maps CLI choices
    choices = {
        'lower': lo,
        'upper': up,
        'digits': di,
        'punctuation': pu,
        }

    CA = chars_possibilities

    # disables chars. Simplistic implementation
    if disable:
        for char_type, chars in CA.items():
            char_list = list(chars)
            for char in disable:
                with suppress(ValueError):
                    char_list.remove(char)
            CA[char_type] = ''.join(char_list)

    # gets one char for each type the user selected
    pass_chars = []
    for char_type, user_choice in choices.items():
        if user_choice:
            pass_chars.append(secrets.choice(CA[char_type]))
            l -= 1

    # all possible chars according to the user choices
    all_chars = ''.join(opt for typ, opt in CA.items() if choices[typ])

    # chooses chars for the remaining pass length
    rest_chars = [secrets.choice(all_chars) for _ in range(l)]

    # joins the first unique-type chars with the random selection
    password = pass_chars + rest_chars

    # further shuffles the password
    len_range = list(range(original_len))
    final_pass = ''
    while len_range:
        idx = secrets.choice(len_range)
        final_pass += password[idx]
        len_range.remove(idx)

    print(final_pass)


if __name__ == '__main__':
    args = vars(ap.parse_args())
    main(**args)
