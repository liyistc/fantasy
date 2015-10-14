#!/usr/bin/python

import matplotlib.pyplot as plt
import pandas as pd
pd.set_option('display.width', 100)
import argparse

def plot(stats, players):
  #print stats
  fig, ax = plt.subplots()

  #player_mask = {'id' : [201566]}
  #row_mask = stats.isin(player_mask).all(1)
  #print stats[row_mask]

  names = []
  for player in players:

    column = stats[['avg_2010', \
                    'avg_2011', \
                    'avg_2012', \
                    'avg_2013', \
                    'avg_2014']][(stats.id == player)].transpose()
    
    ax = column.plot(ax=ax, kind='line', use_index=False)
    names.append(stats[stats.id == player]['name'])

  ax.legend(names)
  plt.show()

def main():
  parser = argparse.ArgumentParser(description = 'Fantasy Data Visualization')
  parser.add_argument('players', metavar='PLAYER', \
                      type=int, nargs='*', help='ids of players to display')
  parser.add_argument('-d', '--display', type=int, \
                      choices=[10,25,50], default=10, help='number of rows to display')
  args = parser.parse_args()

  show = int(args.display)
  stats = pd.DataFrame.from_csv('.cache/res.csv')
  
  if len(args.players) > 0:
    plot(stats=stats, players=args.players)

  print stats.sort_values(by=['avg_2014'], ascending=[False]).head(show)
  
if __name__ == "__main__":
  main()
