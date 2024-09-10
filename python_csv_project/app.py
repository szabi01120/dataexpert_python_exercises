import pandas as pd
import numpy as np
import os

import config

class DataLoader:
    def __init__(self, base_dir, data_dir_name):
        self.base_dir = base_dir
        self.data_dir = os.path.join(base_dir, data_dir_name)
        self.event_path = os.path.join(self.data_dir, 'Deb2010')
        self.scoring_path = os.path.join(base_dir, 'Scoring')

    def read_players(self) -> pd.DataFrame:
        return pd.read_csv(os.path.join(self.base_dir, 'Players.csv'))

    def read_games(self) -> pd.DataFrame:
        return pd.read_csv(os.path.join(self.base_dir, 'Games.csv'))

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
    def calculate_rank_score(row):
        weights = {
            'Participation': 1,
            'Abort': -2,
            'Kills': 3,
            'Deaths': -1,
            'Wins': 5,
            'Combos': 4,
            'Frags': 2
        }

        rank_score = (
            weights['Participation'] * row['Participation'] +
            weights['Abort'] * row['Abort'] +
            weights['Kills'] * row['Kills'] +
            weights['Deaths'] * row['Deaths'] +
            weights['Wins'] * row['Wins'] +
            weights['Combos'] * row['Combos'] +
            weights['Frags'] * row['Frags']
        )
        return rank_score

    def write_top_scores(self, df, head_size, players_df) -> pd.DataFrame:
        headers = ['Rank', 'Rankscore', 'Nick', 'Name']
        df_out = pd.DataFrame(columns=headers)
        df_out['Rankscore'] = (
            df['Participation'] + df['Abort'] + df['Kills'] - df['Deaths'] +
            df['Wins'] + df['Combos']
        )
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
                if name.startswith('Match'):
                    df = pd.read_csv(os.path.join(root, name))
                    headers = df.columns
                    data = pd.concat([data, df])
        df = pd.DataFrame(data, columns=headers)
        if not os.path.isfile('merged_data.csv'):
            df.to_csv('merged_data.csv', index=False)
        else:
            print('File already exists')

    def merge_event_tables(self):
        for path in os.listdir(self.event_path):
            for root, _, files in os.walk(os.path.join(self.event_path, path)):
                data = pd.DataFrame()
                for name in files:
                    if name.startswith('Match'):
                        df = pd.read_csv(os.path.join(root, name))
                        data = pd.concat([data, df])
                df = pd.DataFrame(data, columns=df.columns)
                output_path = os.path.join(self.event_path, path, 'merged_event_data.csv')
                if not os.path.isfile(output_path):
                    df.to_csv(output_path, index=False)

    def top_n_by_event(self, head_size=10, output_path=None): # alap 10, kezeli a top100-at is
        players_df = self.data_loader.read_players()
        score_manager = ScoreManager()

        if head_size == 100:
            # Merged data beolvasása és a top 100 játékos meghatározása
            df = pd.read_csv('merged_data.csv')
            df_out = score_manager.write_top_scores(df, head_size, players_df)
            
            # Ha nincs megadva output_path, az alapértelmezett a főmappa
            output_path = output_path or 'top100.csv'
            df_out.to_csv(output_path, index=False)
        else:
            # Eseményenkénti top 10 rangsor
            for path in os.listdir(self.event_path):
                df = pd.read_csv(os.path.join(self.event_path, path, 'merged_event_data.csv'))
                df_out = score_manager.write_top_scores(df, head_size, players_df)
                df_out.to_csv(os.path.join(self.event_path, path, f'top{head_size}.csv'), index=False)

    def top_n_by_event_game_type(self, head_size=10):
        players_df = self.data_loader.read_players()
        score_manager = ScoreManager()
        game_types = set(pd.read_csv(os.path.join(self.data_loader.base_dir, 'Games.csv'))['Id'])
        for path in os.listdir(self.event_path):
            df = pd.read_csv(os.path.join(self.event_path, path, 'merged_event_data.csv'))
            for game_type in game_types:
                df_filtered = df[df['GameType'] == game_type]
                df_out = score_manager.write_top_scores(df_filtered, head_size, players_df)
                df_out.to_csv(os.path.join(self.event_path, path, f'top{head_size}_{game_type}.csv'), index=False)

    def player_by_wins(self, players_dir):
        headers = ['Event', 'EarnedRank', 'RankScore']  # Csak a szükséges oszlopok
        player_set = set(pd.read_csv('Top100.csv')['Nick'])  # Top100 játékos beolvasása

        for player in player_set:
            player_dir = os.path.join(players_dir, player)
            os.makedirs(player_dir, exist_ok=True)

            player_data = []

            for event in os.listdir(self.event_path):  # Eventek bejárása
                event_dir_path = os.path.join(self.event_path, event)
                all_matches_df = pd.DataFrame()

                for match_file in os.listdir(event_dir_path):  # Meccsek bejárása
                    if match_file.startswith('Match_') and match_file.endswith('.csv'):
                        match_df = pd.read_csv(os.path.join(event_dir_path, match_file))
                        all_matches_df = pd.concat([all_matches_df, match_df])

                for game_type in set(all_matches_df['GameType']):  # Játéktípusok bejárása
                    df_game_type = all_matches_df[all_matches_df['GameType'] == game_type].copy()  # .copy() a SettingWithCopyWarning elkerülésére
                    df_player = df_game_type[df_game_type['Player'] == player]

                    if not df_player.empty:
                        df_game_type.loc[:, 'RankScore'] = df_game_type.apply(ScoreManager.calculate_rank_score, axis=1)
                        df_game_type = df_game_type.sort_values(by='RankScore', ascending=False).reset_index(drop=True)
                        df_game_type.loc[:, 'EarnedRank'] = df_game_type.index + 1

                        top_player_row = df_game_type[df_game_type['Player'] == player].head(1)

                        player_data.append({
                            'Event': event,
                            'EarnedRank': top_player_row['EarnedRank'].values[0],
                            'RankScore': top_player_row['RankScore'].values[0]
                        })

            # dict -> DataFrame -> CSV
            if player_data:
                df_new = pd.DataFrame(player_data, columns=headers)
                df_new = df_new.sort_values(by='EarnedRank', ascending=True).head(10)  # Csak az első 10
                csv_path = os.path.join(player_dir, 'top10.csv')

                if not os.path.isfile(csv_path):
                    df_new.to_csv(csv_path, index=False)


def main():
    data_loader = DataLoader(config.baseDir, config.dataDirName)
    event_manager = EventManager(data_loader)

    event_manager.merge_all_tables()
    event_manager.merge_event_tables()

    # Top 100 
    event_manager.top_n_by_event(100, output_path='top100.csv')

    # Top 10 event
    event_manager.top_n_by_event(10)

    # Top 10 event game type
    event_manager.top_n_by_event_game_type(10)

    # Játékosok nyerési rangsora
    event_manager.player_by_wins(os.path.join(config.baseDir, 'Players'))

if __name__ == "__main__":
    main()
