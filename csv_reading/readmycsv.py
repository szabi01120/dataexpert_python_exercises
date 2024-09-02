import csv

def translated():
    with open('translated.txt', 'r', encoding='utf-8') as f:
        translations = [line.strip() for line in f]
    f.close()
    return translations

def operations(translations):
    # már olvasható csv import és output file megnyitás
    with open('readable.csv', 'r', encoding='utf-8') as r, \
        open('mycsv.csv', 'w', encoding='utf-8', newline='') as w:

        reader = csv.reader(r)
        writer = csv.writer(w)

        for i, row in enumerate(reader):
            if i < len(translations):
                row.append(translations[i])
            else:
                row.append('')  #üres ha nincs megfelelő fordítás

            writer.writerow(row)

    #több lett a fordítás mint sor, warning
    if len(translations) > i + 1:
        print(f"{len(translations) - (i + 1)} fordítás nem került be a fájlba, mert több van mint sor")
    r.close()
    w.close()
    
def main():
    translations = translated()
    operations(translations)
        
if __name__ == "__main__":
    main()