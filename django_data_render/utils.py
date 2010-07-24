# -*- coding: utf-8 -*-


def eval_dict(d):
    d = copy.deepcopy(d) if d else {}
    for k in d:
        value = d[k]
        d[k] = value() if callable(value) else value
    return d
