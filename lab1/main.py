import requests
import json
from map import create_map

row = 5
col = 7

def main():
    create_map(row, col)
    api = 'https://coe892.reev.dev/lab1/rover'
    r = requests.get(f'{api}/10')
    if (r.ok):
        content = json.loads(r.content)
    print(content['data'])
        # for i in r.content:
        #     print(chr(i))




if (__name__ == "__main__"):
    main()
