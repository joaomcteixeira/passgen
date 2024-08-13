"""
An utterly simple password generator made in Python.

By default, a password contains lower and upper case characters, digits,
and punctuation. You can disable these different types separately.

USAGE:
    $ python passgen.py -h
    $ python passgen.py
    $ python passgen.py -pu
    $ python passgen.py -pum  # uses only -_$%& chars as punctuation
"""
import argparse
import random
import secrets
import string
import time
from contextlib import suppress
from tkinter import Tk


class _JoinDisable(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        disable = ''.join(chars for d in values for chars in d).replace(" ", "")
        setattr(namespace, self.dest, disable)


class InputError(Exception):
    pass


ap = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    )

ap.add_argument('-l', help='Password length. Defaults to 16.', default=16, type=int)
ap.add_argument('-lo', help='Disable lower case chars.', action="store_false")
ap.add_argument('-up', help='Disable upper case chars.', action="store_false")
ap.add_argument('-di', help='Disable digits.', action="store_false")
ap.add_argument('-pu', help='Disable punctuation.', action="store_false")
ap.add_argument('-pum', help='Uses minimal punctuation chars (- and _).', action="store_true")
ap.add_argument('-url', help='Uses URL characters only [A-Za-z0-9_.-~].', action="store_true")
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
    'pum': r"-_",
    'url': r"-_.~",
    }


def main(l=16, lo=True, up=True, di=True, pu=True, pum=False, url=False, disable=None):
    """Create a password."""
    original_len = l

    # maps CLI choices
    choices = {
        'lower': lo,
        'upper': up,
        'digits': di,
        'punctuation': pu and (not pum and not url),
        'url': url,
        'pum': pum
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
    try:
        rest_chars = [secrets.choice(all_chars) for _ in range(l)]
    except IndexError:
        raise InputError(
            'There are no characters left to create a password. '
            'You have likely disabled all of them. '
            'Please review your input. '
            ) from None

    # joins the first unique-type chars with the random selection
    password = pass_chars + rest_chars

    # further shuffles the password
    len_range = list(range(original_len))
    final_pass = ''
    while len_range:
        idx = secrets.choice(len_range)
        final_pass += password[idx]
        len_range.remove(idx)

    r = Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(final_pass)
    r.update()
    r.destroy()


if __name__ == '__main__':
    args = vars(ap.parse_args())
    main(**args)
