import json

__all__ = ["load", "save"]


def load(filename, encoding="utf-8"):
    with open(filename, "r", encoding=encoding) as fp:
        return json.load(fp)


def save(obj, filename, encoding="utf-8"):
    with open(filename, "w", encoding=encoding) as fp:
        fp.write(json.dumps(obj, indent=2, ensure_ascii=False))
