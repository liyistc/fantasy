#!/usr/bin/python

# Fantasy Basketball Analytics
# Author Yi Li
# Last modified: Oct 13, 2015


from goldsberry import *
from goldsberry.player import game_logs
import pandas as pd
from progressbar import ProgressBar, Bar, ETA, Percentage, RotatingMarker
import os
import argparse

def analyse(season, cache):
    ranking = pd.DataFrame(columns=('name','score'))

    players = pd.DataFrame(PlayerList(season))
    widgets = ['Analyzing: ', Percentage(), ' ', Bar(marker=RotatingMarker()), ' ', ETA()]
    pbar = ProgressBar(widgets=widgets, maxval=len(players.index)).start()
    
    for index, row in players.iterrows():
        name = row['DISPLAY_LAST_COMMA_FIRST']
        person = row['PERSON_ID']
        
        playerlog = str(person) + '.csv'
        player_cache = os.path.join(cache, playerlog)
        if not os.path.exists(player_cache):
            stats = pd.DataFrame(game_logs(playerid=person, season=season).logs())
            stats.to_csv(player_cache)
        else:
            stats = pd.DataFrame.from_csv(player_cache)

        game_played = len(stats.index)
        if game_played > 0:
            game_win = len(stats[stats.WL == 'W'].index)
            game_lose = len(stats[stats.WL == 'L'].index)
            double_double = len(stats[((stats.AST >= 10) & (stats.PTS >= 10)) | ((stats.AST >= 10) & (stats.REB >= 10)) | ((stats.PTS >= 10) & (stats.REB >= 10))].index)
            triple_double = len(stats[((stats.AST >= 10) & (stats.PTS >= 10)) & (stats.REB >= 10)].index)
            sum = stats.sum()
            total_pts = sum['PTS']
            total_ast = sum['AST']
            total_blk = sum['BLK']
            total_fgm = sum['FGM']
            total_fgmiss = sum['FGA'] - sum['FGM']
            total_fg3m = sum['FG3M']
            total_fg3miss = sum['FG3A'] - sum['FG3M']
            total_reb = sum['REB']
            total_pf = sum['PF']
            total_ftm = sum['FTM']
            total_ftmiss = sum['FTA'] - sum['FTM']
            total_stl = sum['STL']
            total_tov = sum['TOV']

            total_score = 1 * total_pts + 1.25 * total_reb + 1.5 * total_ast + 3 * total_stl + 3 * total_blk + 1 * total_fg3m - 1 * total_tov - 0.5 * (total_fgmiss + total_ftmiss) + 5 * (double_double - triple_double) + 20 * triple_double
            avg_score = total_score / game_played
        else:
            avg_score = 0.0

        line = pd.DataFrame({'name' : [name], 'score' : [avg_score]})
        ranking = ranking.append(line, ignore_index=True)

        pbar.update(index)
        
    pbar.finish()
    return ranking
    
def main():

    parser = argparse.ArgumentParser(description = 'Fantasy Player Analytics')
    parser.add_argument('season', metavar='SEASON', type=int, nargs='+', help='season to analyse')
    parser.add_argument('-d', '--display', type=int, choices=[10,25,50], default=10, help='number of results to display')
    args = parser.parse_args()
    
    season = args.season
    show = int(args.display)
    cache = "cache"
    
    for s in season:
        if s < 2000 or s > 2015:
            print 'Invalid season!'
            exit(1)
            
        print 'Analyzing season ', s
        s = str(s)
        season_cache = os.path.join(cache, s)
        if not os.path.exists(season_cache):
            os.makedirs(season_cache)

        ranking = analyse(season=s, cache=season_cache)
        
        
    print ranking.sort_values(by=['score'], ascending=[False]).head(show)
    ranking.to_csv('res.csv')
    
if __name__ == "__main__":
    main()
