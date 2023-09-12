def object_to_dict(obj: object):
    if obj is None:
        return None
    if isinstance(obj, dict):
        return obj
