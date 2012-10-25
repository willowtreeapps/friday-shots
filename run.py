
from datetime import datetime
import json
import random
import sys

names = list(set(sys.argv[1:]))

print 'There are %d players: %s' % (len(names), ', '.join(sorted(names)))
raw_input('Continue?')

random.shuffle(names)

results = {}

while names:
    name = names.pop()

    result = raw_input('[%d] %s: ' % (len(results), name))
    result = result.lower()

    if result in ('y', 'yes'):
        results[name] = True

    elif result in ('n', 'no'):
        results[name] = False

    elif result in ('w', 'wait'):
        names.insert(0, name)

    elif result in ('s', 'skip'):
        continue

    else:
        print 'Unrecognized'
        names.append(name)


with open('data.json', 'r') as f:
    data = json.load(f)

data.append({'date': str(datetime.now().date()), 'results': results})

with open('data.json', 'w') as f:
    json.dump(data, f, indent=2)
