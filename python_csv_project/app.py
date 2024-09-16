import pandas as pd
import numpy as np
import os
from concurrent.futures import ThreadPoolExecutor
import config

class DataLoader:
    def __init__(self, base_dir, data_dir_name):
        self.base_dir = base_dir
        self.data_dir = os.path.join(base_dir, data_dir_name)
        self.event_path = os.path.join(self.data_dir, 'Deb2010')
        self.scoring_path = os.path.join(base_dir, 'Scoring')
        
    def read_players(self) -> pd.DataFrame:
        return pd.read_csv('Players.csv')

    def read_games(self) -> pd.DataFrame:
        return pd.read_csv('Games.csv')
    
    def read_score_types(self) -> dict:
        score_types = {}
        for game in ['Doom2dm', 'SnL', 'WormsAr']:
            df = pd.read_csv(os.path.join(self.scoring_path, f'{game}.csv'))
            score_types[game] = {
                'ScoreType': df['ScoreType'],
                'RankingWeight': df['RankingWeight']
            }
        return score_types

class ScoreManager:
    @staticmethod
    def calculate_rank_score(row_or_df):
        weights_df = pd.read_csv('Scoring/Doom2dm.csv')
        weights = dict(zip(weights_df['ScoreType'], weights_df['RankingWeight']))

        rank_score = (
                weights['Participation'] * row_or_df['Participation'] +
                weights['Abort'] * row_or_df['Abort'] +
                weights['Kills'] * row_or_df['Kills'] +
                weights['Deaths'] * row_or_df['Deaths'] +
                weights['Wins'] * row_or_df['Wins'] +
                weights['Combos'] * row_or_df['Combos'] +
                weights['Frags'] * row_or_df['Frags']
            )
        return rank_score

    def write_top_scores(self, df, head_size, players_df) -> pd.DataFrame:
        headers = ['Rank', 'Rankscore', 'Nick', 'Name']
        
        df_out = pd.DataFrame(columns=headers)
        df_out['Rankscore'] = self.calculate_rank_score(df)
        
        # Sort values by Rankscore and select top N
        df_out = df_out.sort_values(by='Rankscore', ascending=False).head(head_size)
        df_out['Rank'] = np.arange(1, head_size + 1, 1)
        df_out['Nick'] = df['Player']
        df_out['Name'] = df_out['Nick'].map(players_df.set_index('Nick')['Name'])
        return df_out

class EventManager:
    def __init__(self, data_loader):
        self.event_path = data_loader.event_path
        self.data_loader = data_loader
        
    def merge_all_tables(self):
        headers = []
        data = pd.DataFrame()
        for root, _, files in os.walk(self.event_path):
            for name in files:
                if name.startswith('Match_'):
                    df = pd.read_csv(os.path.join(root, name))
                    headers = df.columns
                    data = pd.concat([data, df], ignore_index=True)  # Optimalizált concat
        df = pd.DataFrame(data, columns=headers)
        
        if not os.path.exists('merged_data.csv'):
            df.to_csv('merged_data.csv', index=False)  # A fájl felülírható, nem kell ellenőrizni
        return df
        
    def merge_event_tables(self):
        def merge_single_event(event_dir_path, event_name):
            data = pd.DataFrame()
            for match_file in os.listdir(event_dir_path):
                if match_file.startswith('Match_'):
                    match_df = pd.read_csv(os.path.join(event_dir_path, match_file))
                    data = pd.concat([data, match_df], ignore_index=True)  # Optimalizált concat
            df = pd.DataFrame(data, columns=data.columns)
            
            event_data_path = os.path.join(self.event_path, event_name, 'merged_event_data.csv')
            if not os.path.exists(event_data_path):           
                df.to_csv(event_data_path, index=False)
                return df

        with ThreadPoolExecutor() as executor:
            for path in os.listdir(self.event_path):
                event_dir_path = os.path.join(self.event_path, path)
                executor.submit(merge_single_event, event_dir_path, path)  # Párhuzamos feldolgozás
                
    def top_n_by_event(self, merged_data_df, head_size=10, output_path=None):
        players_df = self.data_loader.read_players()
        score_manager = ScoreManager()
        print("merged_data_df:\n", merged_data_df)
        
        if head_size == 100:
            df_out = score_manager.write_top_scores(merged_data_df, head_size, players_df)
            output_path = output_path or 'top100.csv'
            
            if not os.path.exists(output_path):
                df_out.to_csv(output_path, index=False)
        else:
            def process_event(event_name):
                df = pd.read_csv(os.path.join(self.event_path, event_name, 'merged_event_data.csv'))
                df_out = score_manager.write_top_scores(df, head_size, players_df)
                
                top_n_path = os.path.join(self.event_path, event_name, f'top{head_size}.csv')
                
                if not os.path.exists(top_n_path):
                    df_out.to_csv(top_n_path, index=False)
                    print("lefut top10")
            with ThreadPoolExecutor() as executor:
                for path in os.listdir(self.event_path):
                    executor.submit(process_event, path)  # Párhuzamos feldolgozás
                    
    def top_n_by_event_game_type(self, head_size=10):
        players_df = self.data_loader.read_players()
        score_manager = ScoreManager()
        game_types = set(pd.read_csv(os.path.join(self.data_loader.base_dir, 'Games.csv'))['Id'])
        
        def process_event_game_type(event_name):
            df = pd.read_csv(os.path.join(self.event_path, event_name, 'merged_event_data.csv'))
            for game_type in game_types:
                df_filtered = df[df['GameType'] == game_type]
                df_out = score_manager.write_top_scores(df_filtered, head_size, players_df)
                
                top_n_gametype = os.path.join(self.event_path, event_name, f'top{head_size}_{game_type}.csv')
                
                if not os.path.exists(top_n_gametype):
                    df_out.to_csv(top_n_gametype, index=False)
                    
        with ThreadPoolExecutor() as executor:
            for path in os.listdir(self.event_path):
                executor.submit(process_event_game_type, path)  # Párhuzamos feldolgozás
                
    def player_top_ten_data(self, players_dir):
            headers = ['Event', 'EarnedRank', 'RankScore']
            player_set = set(pd.read_csv('Top100.csv')['Nick'])  # Top100 nevek
            
            def process_player_game_type(player):
                player_dir = os.path.join(players_dir, player)
                os.makedirs(player_dir, exist_ok=True)

                unique_game_types = self.data_loader.read_games()['Id'].tolist()

                overall_player_data = []  # Az összesített adatok lista

                for game_type in unique_game_types:
                    player_data = []
                    for event in os.listdir(self.event_path):
                        event_dir_path = os.path.join(self.event_path, event)
                        all_matches_df = pd.DataFrame()
                        for match_file in os.listdir(event_dir_path):
                            if match_file.startswith('Match_'):
                                match_df = pd.read_csv(os.path.join(event_dir_path, match_file))
                                all_matches_df = pd.concat([all_matches_df, match_df], ignore_index=True)
                        df_game_type = all_matches_df[all_matches_df['GameType'] == game_type]
                        df_player = df_game_type[df_game_type['Player'] == player]
                        
                        if not df_player.empty:
                            # Készítsünk mély másolatot, hogy elkerüljük a SettingWithCopyWarning-ot
                            df_game_type = df_game_type.copy(deep=True)
                            df_game_type['RankScore'] = df_game_type.apply(ScoreManager.calculate_rank_score, axis=1)
                            df_game_type = df_game_type.sort_values(by='RankScore', ascending=False).reset_index(drop=True)
                            df_game_type['EarnedRank'] = df_game_type.index + 1
                            top_player_row = df_game_type[df_game_type['Player'] == player].head(1)
                            player_event_data = {
                                'Event': event,
                                'EarnedRank': top_player_row['EarnedRank'].values[0],
                                'RankScore': top_player_row['RankScore'].values[0]
                            }
                            player_data.append(player_event_data)
                            overall_player_data.append(player_event_data)  # Adatok hozzáadása az összesített listához
                            
                    if player_data:
                        df_new = pd.DataFrame(player_data, columns=headers)
                        df_new = df_new.sort_values(by='EarnedRank', ascending=True).head(10)
                        csv_path = os.path.join(player_dir, f'top10_{game_type}.csv')
                        if not os.path.exists(csv_path):
                            df_new.to_csv(csv_path, index=False)
                            
                # Összesített top10.csv player mappákba
                if overall_player_data:
                    df_overall = pd.DataFrame(overall_player_data, columns=headers)
                    df_overall = df_overall.sort_values(by='EarnedRank', ascending=True).head(10)
                    overall_csv_path = os.path.join(player_dir, 'top10.csv')
                    if not os.path.exists(overall_csv_path):
                        df_overall.to_csv(overall_csv_path, index=False)
                        
            # Párhuzamos feldolgozás ThreadPoolExecutorral
            with ThreadPoolExecutor() as executor:
                for player in player_set:
                    executor.submit(process_player_game_type, player)
                    
    def player_by_event(self):
        headers = ['Event', 'GameType', 'MatchId', 'ScoreType', 'Score']
        player_set = set(pd.read_csv('Players.csv')['Nick'])  # Top100 nevek

        # Párhuzamos feldolgozáshoz ThreadPoolExecutor
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.process_player_events, player, headers) for player in player_set]

            for future in futures:
                future.result()  # Várjuk meg a feldolgozást minden játékosra

    def process_player_events(self, player, headers):
        os.makedirs(os.path.join(config.baseDir, 'Players', player), exist_ok=True)
        output_df = pd.DataFrame(columns=headers)

        for event in os.listdir(self.event_path):
            for match in os.listdir(os.path.join(self.event_path, event)):
                if match.startswith('Match_'):
                    match_df = pd.read_csv(os.path.join(self.event_path, event, match))
                    match_df['Event'] = event
                    match_df['MatchId'] = match.split('.')[0]

                    player_data_df = match_df[match_df['Player'] == player].copy()

                    if not player_data_df.empty:
                        player_data_df.loc[:, 'ScoreType'] = "SUM"
                        player_data_df.loc[:, 'Score'] = player_data_df.apply(ScoreManager.calculate_rank_score, axis=1)

                        player_data_df = player_data_df[['Event', 'GameType', 'MatchId', 'ScoreType', 'Score']]

                        output_df = pd.concat([output_df, player_data_df], ignore_index=True)

        print(f"output_df for {player}:\n", output_df)
        output_df.to_csv(os.path.join(config.baseDir, 'Players', player, 'Deb2010.csv'), index=False)

        self.player_top_scores(output_df, player) # top 100 scores 

    def player_top_scores(self, output_df, player):
        headers = ['Score', 'ScoreType', 'GameType', 'Event']
        top_score_df = pd.DataFrame(columns=headers)

        def get_top_scores():
            output_df['Score'] = pd.to_numeric(output_df['Score'], errors='coerce') # coerce -> NaN ha nem jó az input
            return output_df.nlargest(100, 'Score')

        # top100 score to top_score_df
        top_scores = get_top_scores()
        top_score_df = pd.concat([top_score_df, top_scores[['Score', 'ScoreType', 'GameType', 'Event']]], ignore_index=True)

        top_scores_path = os.path.join(config.baseDir, 'Players', player, 'top100_scores.csv')
        top_score_df.to_csv(top_scores_path, index=False)

        print(f"Top 100 scores for {player} written to {top_scores_path}")
        
    def match_current_score(self):
        headers = ['Rank', 'Player', 'Name', 'RankScore']
        data = pd.DataFrame(columns=headers)
        
        for path in os.listdir(self.event_path):
            event_dir_path = os.path.join(self.event_path, path)
            for match_file in os.listdir(event_dir_path):
                if match_file.startswith('Match'):
                    match_df = pd.read_csv(os.path.join(event_dir_path, match_file))
                    match_df['RankScore'] = match_df.apply(ScoreManager.calculate_rank_score, axis=1)
                    match_df = match_df.sort_values(by='RankScore', ascending=False).reset_index(drop=True).head(10)
                    match_df['Rank'] = np.arange(1, 11, 1)
                    match_df['Name'] = match_df['Player'].map(self.data_loader.read_players().set_index('Nick')['Name'])
                    
                    data = match_df[['Rank', 'Player', 'Name', 'RankScore']]
                    data_path = os.path.join(event_dir_path, f'current_top10_{match_file.split(".")[0]}.csv')
                    
                    if not os.path.exists(data_path):
                        data.to_csv(data_path, index=False)
        
def main():
    data_loader = DataLoader(config.baseDir, config.dataDirName)
    event_manager = EventManager(data_loader)
    merged_df = event_manager.merge_all_tables()
    print("merged_df:\n", merged_df) # MERGED DF-ET MEG KELL FIXELNI

    event_manager.merge_event_tables()

    event_manager.top_n_by_event(merged_df, 100, output_path='top100.csv')
    event_manager.top_n_by_event(merged_df, 10)
    event_manager.top_n_by_event_game_type(10)

    event_manager.player_top_ten_data(os.path.join(config.baseDir, 'Players'))

    event_manager.player_by_event()
    
    event_manager.match_current_score()

if __name__ == "__main__":
    main()