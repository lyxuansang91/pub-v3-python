# -*- coding: utf-8 -*-
import string
from random import choice, randint


def generate_random_code(n=6):
    return ''.join([str(randint(0, 9)) for _ in range(n)])


def generate_random_string(n=20):
    return ''.join([choice(string.ascii_lowercase) for _ in range(n)])
