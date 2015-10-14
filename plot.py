#!/usr/bin/python

import matplotlib.pyplot as plt
import pandas as pd
pd.set_option('display.width', 120)
import argparse

def plot(stats, players):
  trans = stats.set_index(['id','name']).T

  tuples = []
  for player in players:
    p_name = stats['name'][stats.id == player].values[0]
    tuples.append((player, p_name))

  index = pd.MultiIndex.from_tuples(tuples, names=['id','name'])
  trans[index].plot(kind='line', grid=True, use_index=True)

  plt.show()

def main():
  parser = argparse.ArgumentParser(description = 'Fantasy Data Visualization')
  parser.add_argument('players', metavar='PLAYER', \
                      type=int, nargs='*', help='ids of players to display')
  parser.add_argument('-d', '--display', type=int, \
                      choices=[10,25,50], default=10, help='number of rows to display')
  parser.add_argument('-n', '--number', type=int, \
                      choices=[1,2,3,4,5,6,7], default=5, help='number of columns to display')
  args = parser.parse_args()

  show = int(args.display)
  length = int(args.number)
  stats = pd.DataFrame.from_csv('.cache/res.csv')
  
  if len(args.players) > 0:
    plot(stats=stats, players=args.players)

  print stats.sort_values(by=['avg_2014'], ascending=[False]).head(show)
  
if __name__ == "__main__":
  main()
