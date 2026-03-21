import h5py
import os

p = os.path.join(r"c:\Users\Pc\Documents\project", "food_freshness_model", "model.weights.h5")
with h5py.File(p, "r") as f:
    print("root keys:", list(f.keys()))
    print("layers sample:", list(f['layers'].keys())[:20])
    print("conv-like:", [k for k in f['layers'].keys() if 'Conv' in k or 'conv' in k][:20])
