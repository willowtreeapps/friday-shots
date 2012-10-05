from __future__ import division

from collections import defaultdict
import json
import math
from operator import itemgetter
import sys


def player_records(data):
    """Count the number of wins and losses for each player.
    Args:
      data: JSON representing the results of the competitions

    Returns: 
      list of (player, (#wins, #losses, %wins)) pairs sorted descending by %wins
    """

    counter = defaultdict(lambda: defaultdict(int))
    for day in data:
        for player, successful in day['results'].iteritems():
            if successful:
                counter[player]['wins'] += 1
            else:
                counter[player]['losses'] += 1

    ret = [(player, counts['wins'], counts['losses'], 
            counts['wins'] / (counts['wins'] + counts['losses'])) 
           for player, counts in counter.iteritems()]

    ret.sort(key=itemgetter(3), reverse=True)
    return ret


def money_by_player(data, include_losers=False):
    """Count the amount of money each player has won.
    Args:
      data: JSON representing the results of the competitions
      include_losers: whether players with 0 wins should be included

    Returns: a list of (player, #wins) pairs sorted descending by #wins.
    """

    counter = defaultdict(int)
    money_in_the_pot = 0
    for day in data:
        money_in_the_pot += len(day['results'])

        winners = [player for (player, success) in day['results'].iteritems() 
                          if success]

        if winners:
            money_won = money_in_the_pot / len(winners)
            for player in winners:
                counter[player] += money_won

            money_in_the_pot = 0


        if include_losers:
            for player in day['results'].iterkeys():
                counter[player] += 0


    return sorted(counter.iteritems(), key=itemgetter(1), reverse=True)


def players_per_game(data):
    """
    Args:
      data: JSON data representing results from games.
    Returns: a 4-tuple (min, max, mean, std)
    """
    nums = [len(day['results'])  for day in data]
    return (min(nums), max(nums), mean(nums), stdev(nums))


def mean(xxs):
    xs = list(xxs)
    return sum(xs) / len(xs)

def stdev(xs):
    mn = mean(xs)
    return math.sqrt(mean((x - mn) ** 2 for x in xs))



def main(args):

    if not args:
        raise Exception('First arg must be path to data file.')

    data_fp = args[0]
    with open(data_fp, 'r') as f:
        data = json.load(f)


    print "####  Players' records  ####"
    for player, wins, losses, win_percentage in player_records(data):
        print '* %d of %d (%.0f%%) %s' % (wins, wins + losses, win_percentage * 100, player)

    print

    print '#### Money by player  ####'
    for player, money_won in money_by_player(data):
        print '* [$%.2f] %s' % (money_won, player)

    print

    print '#### Players per game  ####'
    mini, maxi, avg, std = players_per_game(data)
    print '* Average: %.2f' % avg
    print '* Std dev: %.2f' % std
    print '* Minimum: %d' % mini
    print '* Maximum: %d' % maxi



if __name__ == '__main__':
    main(sys.argv[1:])
