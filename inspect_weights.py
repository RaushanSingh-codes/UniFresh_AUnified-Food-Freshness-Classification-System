import h5py
import os
import sys

model_dir = sys.argv[1] if len(sys.argv) > 1 else "food_freshness_model"
path = os.path.join(model_dir, "model.weights.h5")
print("Inspecting:", path)
with h5py.File(path, 'r') as f:
    layers = f['layers']['functional']['layers']
    keys = list(layers.keys())
    conv = [k for k in keys if 'conv' in k.lower()]
    print('conv-like layers:', conv[:40])
    print('total conv-like:', len(conv))
