#!/usr/bin/python

import matplotlib.pyplot as plt
import pandas as pd

def main():

  stats = pd.DataFrame.from_csv('.cache/res.csv')
  
  column = stats[['name', \
                  'avg_2010', \
                  'avg_2011', \
                  'avg_2012', \
                  'avg_2013', \
                  'avg_2014']][(stats.id == 201566) | (stats.id == 200746)].transpose()

  print column[1:]

  column[1:].plot(kind='line', use_index=False)
  plt.show()
  
if __name__ == "__main__":
  main()
