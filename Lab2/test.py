with open('map.txt', 'r') as f:
    x = f.readline()
    grid = []
    row = []
    while(len(x) != 0):
        if (x == '\n'):
            grid.append(row)
            row = []
        elif (x == '0'):  
            row.append(0)            
        elif (x == '1'):
            row.append(1)
        x = f.read(1)
    grid.append(row)
    
    print(grid)
    
        