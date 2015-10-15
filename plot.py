#!/usr/bin/python

import matplotlib.pyplot as plt
import pandas as pd
pd.set_option('display.width', 120)
from pandas import ExcelWriter
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
  parser.add_argument('-e', '--excel', dest='excel', \
                      action='store_true', default=False, help='to excel')
  args = parser.parse_args()

  show = int(args.display)
  stats = pd.DataFrame.from_csv('.cache/res.csv')
  
  if (args.excel):
    writer = ExcelWriter('.cache/res.xlsx')
    stats.to_excel(writer, 'Sheet1')
    writer.save()
  
  if len(args.players) > 0:
    plot(stats=stats, players=args.players)

  print stats.sort_values(by=['avg_2014'], ascending=[False]).head(show)
  
if __name__ == "__main__":
  main()
