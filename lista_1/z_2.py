def tabliczka(x1, x2, y1, y2) :
    max_long = max (abs (x1), abs (x2)) * max (abs (y1), abs (y2)) 
    width = len(str(max_long)) + 1
    if (x1 < 0 or y1 < 0):
        width += 1
    
    print (f'{x1:> {2 * width}}', end='')
    for i in range(x1 + 1, x2 + 1):
        print (f'{i:> {width}}', end='')
    print ("\n")

    for i in range(y1, y2 + 1):
        print (f'{i:> {width}}', end='')
        for j in range(x1, x2 + 1):
            print (f'{(i * j):> {width}}', end='')
        print ("\n")

tabliczka (-8, -3, -1, 2)


