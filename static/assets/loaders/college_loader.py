import json
from accounts.models import College

with open('static/assets/json/colleges.json') as f:
    data = json.load(f)

for item in data:
    College.objects.create(name=item['name'])
