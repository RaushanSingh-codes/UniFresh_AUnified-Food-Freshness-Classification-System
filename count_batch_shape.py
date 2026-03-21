path = 'food_freshness_model/config.json'
with open(path, 'r', encoding='utf-8') as f:
    data = f.read()
print('count batch_shape:', data.count('"batch_shape"'))
