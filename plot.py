#!/usr/bin/python

# Author: Yi Li
# Last modified: Oct 15, 2015

import matplotlib.pyplot as plt
import pandas as pd
pd.set_option('display.width', 120)
from pandas import ExcelWriter
import argparse

def plot(stats, players):
  # compute transpose of player stats table
  trans = stats.set_index(['id','name','team']).T

  # collect selected player indices
  tuples = []
  for player in players:
    p_name = stats['name'][stats.id == player].values[0]
    p_team = stats['team'][stats.id == player].values[0]
    tuples.append((player, p_name, p_team))

  index = pd.MultiIndex.from_tuples(tuples, names=['id','name','team'])
  trans[index].plot(kind='line', grid=True, use_index=True)
  
  # show graph
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

  show = int(args.display) # number of stats to show
  stats = pd.DataFrame.from_csv('.cache/res_avg.csv')
  
  # write all stats to excel file
  if (args.excel):
    writer = ExcelWriter('.cache/res_avg.xlsx')
    stats.to_excel(writer, 'Sheet1')
    writer.save()
  
  # display plot
  if len(args.players) > 0:
    plot(stats=stats, players=args.players)

  # print short summary
  print stats.sort_values(by=['avg_2015'], ascending=[False]).head(show)
  
if __name__ == "__main__":
  main()
