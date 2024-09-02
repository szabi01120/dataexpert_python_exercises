import pandas as pd
import numpy as np

import random

def main():    
    n = 200000
    with open("trends.txt", "r", encoding='utf-8') as file:
        trends_list = file.readlines()
    trends_list = [trend.strip() for trend in trends_list]

    countries = ["USA", "Németország", "Franciaország", "Japán", "Kanada", "Egyesült Királyság", "Olaszország", "Ausztrália", "Spanyolország", "Kína"]
    categories = ["Technológia", "Életmód", "Kultúra", "Gazdaság", "Egészség", "Divat", "Fenntarthatóság", "Szórakozás", "Sport", "Politika", "Világhír"]
    audience = ["Fiatalok", "Idősek", "Gyerekek", "Felnőttek", "Középkorúak", "Tinédzserek", "Vállalkozók", "Munkanélküliek", "Dolgozók", "Nyugdíjasok", ]

    data = pd.DataFrame()
        
    data['Trend'] = [random.choice(trends_list) for _ in range(n)]
    data["Ország"] = [random.choice(countries) for _ in range(n)]
    data["Dátum"] = pd.to_datetime(np.random.choice(pd.date_range("2010-01-01 00:00:00", "2024-08-29 23:59:59"), size=n))
    data["Dátum"] = data["Dátum"].apply(lambda x: x.replace(hour=random.randint(0, 23), minute=random.randint(0, 59)))
    data["Típus"] = [random.choice(categories) for _ in range(n)]
    data["Közönség"] = [random.choice(audience) for _ in range(n)]
    data["Negyedév"] = pd.to_datetime(data["Dátum"]).dt.quarter

    data.to_csv("trends.csv", index=False)
    print(data)

if __name__ == '__main__':
    main()