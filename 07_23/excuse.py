import requests
from bs4 import BeautifulSoup
import time

def get_excuse():
    r = requests.get("http://developerexcuses.com")
    soup = BeautifulSoup(r.text, "html.parser")
    excuse = soup.find("a").get_text()
    return excuse

def collect(duration):
    excuses = set()
    end_time = time.time() + duration
    print("Számolás...")
    req_count = 0
    while time.time() < end_time:
        excuse = get_excuse()
        req_count += 1
        excuses.add(excuse)
    print(f"{req_count} kérést küldtünk a weboldalnak.")
    return excuses

def write_to_file(excuses):
    with open("excuses.txt", "w") as f:
        for excuse in excuses:
            f.write(excuse + "\n")

def main():
    excuses = collect(10)
    print(f"Összesen {len(excuses)} kifogás gyűlt össze.")
    write_to_file(excuses)    
    
if __name__ == '__main__':
    main()