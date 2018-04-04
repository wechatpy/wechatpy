# -*- coding: utf-8 -*-


def skip_if_no_cryptography():
    try:
        import cryptography  # NOQA
        return False
    except ImportError:
        return True