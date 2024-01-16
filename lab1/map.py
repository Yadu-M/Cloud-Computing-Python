import random

"""
hello
"""
def create_map(row, col) -> None:
    f = open('map.txt', 'w')
    
    with open('map.txt', 'w') as f:
        f.write(f'{row} {col}\n')
        for i in range(row):
            for j in range(col):
                if (random.randint(0, 1)):
                    f.write('1')
                else:
                    f.write('0')
            f.write('\n')
    f.close()
    
create_map(5, 7)