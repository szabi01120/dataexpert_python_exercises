import pandas as pd

input_fajl = "input_excel.xlsx"
output_fajl = "output_excel.xlsx"

input_df = pd.read_excel(input_fajl, header=None)
output_df = pd.read_excel(output_fajl)

sorok_kivonas = 9  

for index, row in input_df.iterrows():
    parameterek = [x.strip() for x in str(row[0]).split(',')]
    print(parameterek)

    for i, param in enumerate(parameterek):
        kezdo_index = i * sorok_kivonas + 1 
        zaro_index = kezdo_index + sorok_kivonas

        kinyert_adatok = row[kezdo_index:zaro_index].values  

        output_oszlopok = [col for col in output_df.columns if col.startswith(f'KL5_{param}')]

        if len(output_oszlopok) == 9:
            output_df.loc[index, output_oszlopok] = kinyert_adatok
        else:
            print(f"Figyelem: A(z) {param} paraméterhez 9 oszlopot vártunk, de csak {len(output_oszlopok)} található.")

output_df.to_excel("modified_output_excel.xlsx", index=False)
print("sikeres fajl iras")
