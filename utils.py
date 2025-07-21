from bson import ObjectId

def to_str_id(obj):
    obj["id"] = str(obj["_id"])
    del obj["_id"]
    return obj
