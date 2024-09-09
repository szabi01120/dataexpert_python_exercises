import pandas as pd
import numpy as np
import os

import config

path = os.path.join(config.baseDir, config.dataDirName)
eventPath = os.path.join(path, 'Deb2010')

def readPlayers() -> pd.DataFrame:    
    df = pd.read_csv('Players.csv')
    return df

def readGames() -> pd.DataFrame:
    df = pd.read_csv('Games.csv')
    return df

def ScoreTypes() -> dict:
    scoringPath = os.path.join(config.baseDir, 'Scoring')
    
    df_doom = pd.read_csv(os.path.join(scoringPath, 'Doom2dm.csv'))
    df_snl = pd.read_csv(os.path.join(scoringPath, 'SnL.csv'))
    df_wormsar = pd.read_csv(os.path.join(scoringPath, 'WormsAr.csv'))
    
    ScoreTypes = {
        'Doom2dm': {
            'ScoreType': df_doom['ScoreType'],
            'RankingWeight': df_doom['RankingWeight']
        },
        'SnL': {
            'ScoreType': df_snl['ScoreType'],
            'RankingWeight': df_snl['RankingWeight']
        },
        'WormsAr': {
            'ScoreType': df_wormsar['ScoreType'],
            'RankingWeight': df_wormsar['RankingWeight']
        }
    }
    print("scoretypes:", ScoreTypes['Doom2dm']['RankingWeight'].abs().sum())
    return ScoreTypes

def writeTopScores(df, headSize, players_df) -> pd.DataFrame:
    headers = ['Rank', 'Rankscore', 'Nick', 'Name']
    
    df_out = pd.DataFrame(columns=headers)
    df_out['Rankscore'] = df['Participation'] + df['Abort'] + df['Kills'] - df['Deaths'] + df['Wins'] + df['Combos']
    df_out = df_out.sort_values(by='Rankscore', ascending=False)
    df_out = df_out.head(headSize)
    df_out['Rank'] = np.arange(1, headSize + 1, 1)
    df_out['Nick'] = df['Player']
    df_out['Name'] = df_out['Nick'].map(players_df.set_index('Nick')['Name'])
    
    return df_out

def MergeAllTables():
    headers = []
    data = pd.DataFrame()
    
    for root, _, files in os.walk(eventPath):
        for name in files:
            if name.startswith('Match'):
                with open(os.path.join(root, name), "r", encoding='utf-8') as file:
                    reader = pd.read_csv(file)
                    headers = reader.columns
                    data = pd.concat([data, reader])    
    df = pd.DataFrame(data, columns=headers)
    
    if os.path.isfile('merged_data.csv'):
        return print('File already exists')
    df.to_csv('merged_data.csv', index=False)
    
def MergeEventTables():
    paths_to_write = os.listdir(eventPath)
    
    for path in paths_to_write:
        for root, _, files in os.walk(os.path.join(eventPath, path)):
            data = pd.DataFrame()
            for name in files:
                if name.startswith('Match'):
                    with open(os.path.join(root, name), "r") as file:
                        reader = pd.read_csv(file)
                        headers = reader.columns
                        
                        data = pd.concat([data, reader])
                                            
                        df = pd.DataFrame(data, columns=headers)
                        if os.path.isfile(os.path.join(eventPath, path, 'merged_event_data.csv')):
                            continue
                        df.to_csv(os.path.join(eventPath, path, 'merged_event_data.csv'), index=False)    
                
def Top100():
    df = pd.read_csv('merged_data.csv')
    headSize = 100
    
    players_df = readPlayers()
    
    df_out = writeTopScores(df, headSize, players_df)
    df_out['GameType'] = df['GameType']
    
    return df_out.to_csv('top100.csv', index=False)

def Top10ByEvent():
    headSize = 10
    players_df = readPlayers()
    
    paths_to_read = os.listdir(eventPath)
    for path in paths_to_read:
        print(path)
        df = pd.read_csv(os.path.join(eventPath, path, 'merged_event_data.csv'))
        
        df_out = writeTopScores(df, headSize, players_df)        
        
        df_out.to_csv(os.path.join(eventPath, path, 'top10.csv'), index=False)
        
def Top10ByEvent_GameType():
    headSize = 10
    players_df = readPlayers()
    
    paths_to_read = os.listdir(eventPath)
    gameTypes = set(pd.read_csv('Games.csv')['Id'])
    
    for path in paths_to_read:
        df = pd.read_csv(os.path.join(eventPath, path, 'merged_event_data.csv'))
        
        for gameType in gameTypes:
            df_new = df[df['GameType'] == gameType]           
            
            df_out = writeTopScores(df_new, headSize, players_df)
            df_out['GameType'] = gameType
            
            df_out.to_csv(os.path.join(eventPath, path, f'top10_{gameType}.csv'), index=False)          
            
def Top100_GameType():
    headSize = 100
    players_df = readPlayers()
    
    df = pd.read_csv('merged_data.csv')
    gameTypes = set(pd.read_csv('Games.csv')['Id'])
    
    for gameType in gameTypes:
        df_new = df[df['GameType'] == gameType]
        
        df_out = writeTopScores(df_new, headSize, players_df)
        df_out['GameType'] = gameType
        
        df_out.to_csv(f'top100_{gameType}.csv', index=False)  

def calculate_rank_score(row):
    weights = {
        'Participation': 1,  # Participation points
        'Abort': -2,         # Penalty for aborting games
        'Kills': 3,          # Points per kill
        'Deaths': -1,        # Negative points for deaths
        'Wins': 5,           # Points per win
        'Combos': 4,         # Points per combo
        'Frags': 2           # Points per frag
    }

    rank_score = (weights['Participation'] * row['Participation'] +
                  weights['Abort'] * row['Abort'] +
                  weights['Kills'] * row['Kills'] +
                  weights['Deaths'] * row['Deaths'] +
                  weights['Wins'] * row['Wins'] +
                  weights['Combos'] * row['Combos'] +
                  weights['Frags'] * row['Frags'])
    
    return rank_score

def PlayerByWins(path, eventPath):
    headers = ['Event', 'EarnedRank', 'RankScore']
    
    playersPath = os.path.join(path, 'Players')
    print(playersPath)

    if not os.path.isdir(playersPath):
        os.mkdir(playersPath)
        
    playerSet = set(pd.read_csv('Top100.csv')['Nick'])
    print(len(playerSet))
    
    for player in playerSet:
        playerDir = os.path.join(playersPath, player)
        
        if not os.path.isdir(playerDir):
            os.mkdir(playerDir)
            
        df_new = pd.DataFrame(columns=headers)
        
        for event in os.listdir(eventPath):
            eventFilePath = os.path.join(eventPath, event, 'merged_event_data.csv')
            df = pd.read_csv(eventFilePath)
            
            for gameType in set(df['GameType']):
                df_gameType = df[df['GameType'] == gameType]
                df_player = df_gameType[df_gameType['Player'] == player]
                
                if not df_player.empty:
                    # RankScore kiszámítása az apply függvény használatával, loc indexeléssel a hibák elkerülése érdekében
                    df_gameType.loc[:, 'RankScore'] = df_gameType.apply(calculate_rank_score, axis=1)
                    
                    # Rendezés a RankScore alapján és EarnedRank hozzáadása
                    df_gameType = df_gameType.sort_values(by='Wins', ascending=False).reset_index(drop=True)
                    df_gameType['EarnedRank'] = df_gameType.index + 1
                    
                    # Az aktuális játékos legjobb eredményének kiválasztása és az esemény nevének beállítása
                    df_player = df_gameType[df_gameType['Player'] == player].head(1)
                    df_player['Event'] = event  # Az esemény nevének beállítása
        
                    df_new = pd.concat([df_new, df_player])
        
        df_new.to_csv(os.path.join(playerDir, 'player.csv'), index=False)

def main():
    MergeAllTables()
    MergeEventTables()
    
    Top100()
    Top10ByEvent()    
    Top10ByEvent_GameType()
    Top100_GameType()
    PlayerByWins(path, eventPath)
    ScoreTypes()
    
if __name__ == "__main__":
    main()