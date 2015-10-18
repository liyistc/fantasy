#!/usr/bin/python

# Fantasy Basketball Analytics
# Author Yi Li
# Last modified: Oct 18, 2015


from goldsberry import *
from goldsberry.player import demographics, game_logs
import pandas as pd
from progressbar import ProgressBar, Bar, ETA, Percentage, RotatingMarker
import os
import argparse


class Analyzer:

    def __init__(self, cache, default_season):
        self.cache = cache
        self.default_cache = os.path.join(cache, 'default')
        self.default_season = default_season
        if not os.path.exists(self.default_cache):
            os.makedirs(self.default_cache)

    def merge_table_on_id_name(self, table_list, seasons, column):
        i = 0
        merge = table_list[i][['id','name','team',column]]
        # rename column avg to avg_<season>
        merge = merge.rename(columns = {column : column+'_'+str(seasons[i])})
        
        for r in table_list[1:]:
            i = i + 1
            margin = r[['id','name','team',column]].\
                     rename(columns = \
                            {column : column+'_'+str(seasons[i])})
            merge = pd.merge(merge, margin, \
                             on=['id','name','team'])
        return merge

    def analyse(self, seasons):
        rank_list = []
        merged_ranking = dict()

        for s in seasons:
            if s < 2000 or s > 2015:
                print 'Invalid season!'
                exit(1)
            
            print 'Analyzing season ', s
            s = str(s)
            season_cache = os.path.join(self.cache, s)
            
            # we only care about players appeared in the latest rosters
            players_cache = os.path.join(self.default_cache, 'players.csv')
            if not os.path.exists(season_cache):
                os.makedirs(season_cache)

            if not os.path.exists(players_cache):
                p_2015 = pd.DataFrame(PlayerList(self.default_season))
                p_2015.to_csv(players_cache)
            else:
                p_2015 = pd.DataFrame.from_csv(players_cache)

            season_ranking = self.analyse_season(players=p_2015, season=s, cache=season_cache)
            rank_list.append(season_ranking)

        merged_ranking['avg'] = self.merge_table_on_id_name(rank_list, seasons, 'avg')
        merged_ranking['total'] = self.merge_table_on_id_name(rank_list, seasons, 'total')
        merged_ranking['games'] = self.merge_table_on_id_name(rank_list, seasons, 'games')

        return merged_ranking
        

    def get_player_info(self, pid):
        player_info_cache = os.path.join(self.default_cache, str(pid) + '.csv')
        if not os.path.exists(player_info_cache):
            info = pd.DataFrame(demographics(pid).player_info())
            info.to_csv(player_info_cache)
        else:
            info = pd.DataFrame.from_csv(player_info_cache)
            
        team = info['TEAM_ABBREVIATION'].values[0]
        from_year = info['FROM_YEAR'].values[0]
        to_year = info['TO_YEAR'].values[0]
        return (team, from_year, to_year)

    def analyse_season(self, players, season, cache):
        ranking = pd.DataFrame(columns=('id', 'name','total','games','avg'))

        widgets = ['Analyzing: ', Percentage(), ' ', Bar(marker=RotatingMarker()), ' ', ETA()]
        pbar = ProgressBar(widgets=widgets, maxval=len(players.index)).start()
    
        for index, row in players.iterrows():
            name = row['DISPLAY_LAST_COMMA_FIRST']
            person = row['PERSON_ID']
            playerlog = str(person) + '.csv'
            player_cache = os.path.join(cache, playerlog)
            team = row['TEAM_ABBREVIATION']

            if not os.path.exists(player_cache):
                stats = pd.DataFrame(game_logs(playerid=person, season=season).logs())
                stats.to_csv(player_cache)
            else:
                stats = pd.DataFrame.from_csv(player_cache)

            game_played = len(stats.index)
            # if the played any game in the season
            if game_played > 0:
                game_win = len(stats[stats.WL == 'W'].index)
                game_lose = len(stats[stats.WL == 'L'].index)
                double_double = len(stats[ \
                                           ((stats.AST >= 10) & (stats.PTS >= 10)) | \
                                           ((stats.AST >= 10) & (stats.REB >= 10)) | \
                                           ((stats.AST >= 10) & (stats.BLK >= 10)) | \
                                           ((stats.AST >= 10) & (stats.STL >= 10)) | \
                                           ((stats.PTS >= 10) & (stats.REB >= 10)) | \
                                           ((stats.PTS >= 10) & (stats.BLK >= 10)) | \
                                           ((stats.PTS >= 10) & (stats.STL >= 10)) | \
                                           ((stats.REB >= 10) & (stats.BLK >= 10)) | \
                                           ((stats.REB >= 10) & (stats.STL >= 10)) | \
                                           ((stats.BLK >= 10) & (stats.STL >= 10)) \
                                       ].index)
                triple_double = len(stats[ \
                                           ((stats.AST >= 10) & (stats.PTS >= 10) & (stats.REB >= 10)) | \
                                           ((stats.AST >= 10) & (stats.PTS >= 10) & (stats.BLK >= 10)) | \
                                           ((stats.AST >= 10) & (stats.PTS >= 10) & (stats.STL >= 10)) | \
                                           ((stats.AST >= 10) & (stats.REB >= 10) & (stats.BLK >= 10)) | \
                                           ((stats.AST >= 10) & (stats.REB >= 10) & (stats.STL >= 10)) | \
                                           ((stats.AST >= 10) & (stats.BLK >= 10) & (stats.STL >= 10)) | \
                                           ((stats.PTS >= 10) & (stats.REB >= 10) & (stats.BLK >= 10)) | \
                                           ((stats.PTS >= 10) & (stats.REB >= 10) & (stats.STL >= 10)) | \
                                           ((stats.PTS >= 10) & (stats.BLK >= 10) & (stats.STL >= 10)) | \
                                           ((stats.REB >= 10) & (stats.BLK >= 10) & (stats.STL >= 10)) \
                                       ].index)
                                
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

                total_score = 1 * total_pts \
                              + 1.25 * total_reb \
                              + 1.5 * total_ast \
                              + 3 * total_stl \
                              + 3 * total_blk \
                              + 1 * total_fg3m \
                              - 1 * total_tov \
                              - 0.5 * (total_fgmiss + total_ftmiss) \
                              + 5 * (double_double - triple_double) \
                              + 20 * triple_double
                avg_score = total_score / game_played
            else:
                avg_score = 0.0
                total_score = 0.0

            line = pd.DataFrame({'id' : [person], \
                                 'name' : [name], \
                                 'team' : [team], \
                                 'total' : [total_score], \
                                 'games' : [game_played], \
                                 'avg' : [avg_score]})
            ranking = ranking.append(line, ignore_index=True)
            
            pbar.update(index)
        
        pbar.finish()
        return ranking

def main():
    parser = argparse.ArgumentParser(description = 'Fantasy Player Analytics')
    parser.add_argument('season', metavar='SEASON', \
                        type=int, nargs='+', help='season to analyse')
    parser.add_argument('-d', '--display', type=int, \
                        choices=[10,25,50], default=10, help='number of results to display')
    args = parser.parse_args()
    
    season_list = args.season
    show = int(args.display)
    cache = ".cache"
    default_season = '2015'
    
    analyzer = Analyzer(cache, default_season)
    ranking = analyzer.analyse(seasons=season_list)

    print ranking['avg']
    # print query results to standard output
    # print ranking.sort_values(by=['avg'], ascending=[False]).head(show)
    # cache query results
    ranking['avg'].to_csv(os.path.join(cache, 'res_avg.csv'), index=True)
    ranking['total'].to_csv(os.path.join(cache, 'res_total.csv'), index=True)
    ranking['games'].to_csv(os.path.join(cache, 'res_games.csv'), index=True)
    
if __name__ == "__main__":
    main()
