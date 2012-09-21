
from datetime import datetime
import json
import random
import sys

names = list(set(sys.argv[1:]))

print 'There are %d players: %s' % (len(names), ', '.join(sorted(names)))
raw_input('Continue?')

random.shuffle(names)


results = {}
for index, name in enumerate(names):
    result = raw_input('[%d] %s: ' % (index, name))
    if result.lower() in ('y', 't', '1'):
        results[name] = True
    elif result.lower() == 'skip':
        continue
    else:
        results[name] = False


with open('results.json', 'r') as f:
    data = json.load(f)

data.append({'date': str(datetime.now().date()), 'results': results})

with open('results.json', 'w') as f:
    json.dump(data, f, indent=2)
