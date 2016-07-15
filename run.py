
from datetime import datetime
import json
import random
import sys

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

names = list(set(sys.argv[1:]))

print 'There are %d players: %s' % (len(names), ', '.join(sorted(names)))
raw_input('Continue?')
print "'y' for a hit, 'n' for a miss, 's' to skip someone no longer playing, 'w' to wait"

random.shuffle(names)

results = {}

while names:
    name = names.pop()

    if len(names) > 0:
        print 'On deck: %s' % names[-1]
        
    result = raw_input('[%d] %s: ' % (len(results) + 1, bcolors.BOLD + bcolors.HEADER + name.upper() + bcolors.ENDC))
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
