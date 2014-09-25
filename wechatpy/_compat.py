from __future__ import absolute_import, unicode_literals
import six
try:
    import simplejson as json
except ImportError:
    import json  # NOQA


def byte2int(s, index=0):
    if six.PY2:
        return ord(s[index])
    return s[index]
