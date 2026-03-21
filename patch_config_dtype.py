import json
import os

path = os.path.join(os.path.dirname(__file__), "food_freshness_model", "config.json")
with open(path, "r", encoding="utf-8") as f:
    cfg = json.load(f)

changed = 0

def fix_dtype(obj):
    global changed
    if isinstance(obj, dict):
        if obj.get("module") == "keras" and obj.get("class_name") == "DTypePolicy":
            changed += 1
            return "float32"
        # otherwise traverse
        for k, v in list(obj.items()):
            obj[k] = fix_dtype(v)
        return obj
    if isinstance(obj, list):
        return [fix_dtype(x) for x in obj]
    return obj

cfg = fix_dtype(cfg)

if changed:
    print(f"Replaced {changed} DTypePolicy objects with 'float32'.")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(cfg, f)
else:
    print("No DTypePolicy objects found.")
