from __future__ import annotations

import csv
import random
import os
import config

dataDir = os.path.join(config.baseDir, config.dataDirName)
evDir = os.path.join(dataDir, 'Deb2010')

def ReadCsv(fn:str):
    fp = os.path.join(config.baseDir, fn)
    with open(fp, 'r', newline='', encoding='utf-8') as f:
        r = csv.reader(f)
        for row in r:
            yield row[0]

firstNames = list(ReadCsv('firstNames.csv'))
lastNames = list(ReadCsv('lastNames.csv'))
gameTypes = {'WormsAr':8, 'Doom2dm':4, 'TF2':6, 'SnL':8}
gameTypeNames = list(gameTypes.keys())
scores = ['Participation', 'Abort', 'Kills', 'Deaths', 'Wins', 'Combos', 'Frags']


def genName(first_names:list[str], last_names:list[str]):
    f = random.choice(first_names)
    l = random.choice(last_names)
    return ' '.join((f, l))

def genEvGames(n:int):
    for i in range(1, n):
        gameType = random.choice(gameTypeNames)
        seats = gameTypes[gameType]
        row = [i, gameType, seats]
        yield row
        
def genEvPlayers(i:int, nicks:dict):
    name = genName(firstNames, lastNames)
    nick = f'Player{i:04x}'
    email = f'e{i:04x}@example.com'
    row = [i, nick, name, email]
    nicks.append(nick)
    return row

def genMatchScore(round:int, nicks:list[str], gametype:str, scores:list[str]) -> dict:
    name = random.choice(nicks)
    row = {'Player': name, 'GameType':gametype, 'Round': round}
    for s in scores:
        row[s] = random.randint(1, 100)
    return row
    
def writeEvGames(fn:str, n:int):
    with open(fn, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, lineterminator='\n')
        heads = ['Id', 'Game', 'Seats']
        w.writerow(heads)
        for row in genEvGames(n):
            w.writerow(row)
            
def writeEvPlayers(fn:str, n:int, nicks:list[str]):
    with open(fn, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, lineterminator='\n')
        heads = ['Id', 'Nick', 'Name', 'Email']
        w.writerow(heads)
        for i in range(1, n + 1):
            row = genEvPlayers(i, nicks)
            w.writerow(row)
            
def writeMatchScores(fn:str, n:int, nicks:list[str], scores:list[str]):
    with open(fn, 'w', newline='', encoding='utf-8') as f:
        heads = ['Player', 'Round', 'GameType'] + scores
        w = csv.DictWriter(f, heads, lineterminator='\n')
        w.writeheader()
        for i in range(1, n + 1):
            gametype = random.choice(gameTypeNames)
            row = genMatchScore(i, nicks, gametype, scores)
            w.writerow(row)

def main():
    fn = os.path.join(evDir, 'Games.csv')
    os.makedirs(evDir, exist_ok=True)
    writeEvGames(fn, 10)    
    
    fn = os.path.join(evDir, 'Players.csv')
    nicks = []
    writeEvPlayers(fn, 100, nicks)
    
    for t in range(1, 10):
        for m in range(1, 10):
            dn = os.path.join(evDir, f'Table_{t:04}')
            os.makedirs(dn, exist_ok=True)
            fn = os.path.join(dn,  f'Match_{m:04}.csv')
            writeMatchScores(fn, 100, nicks, scores)

if __name__ == "__main__":
    main()    
