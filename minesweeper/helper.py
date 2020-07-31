from itertools import *

board = [[1,2,3,4,5,6,7,8],
        [9,10,11,12,13,14, 15, 16],
        [17,18,19,20, 21,22,23,24],
        [25,26,27,28,29,30,31,32],
        [33, 34, 35, 36, 37, 38, 39, 40],
        [41, 42, 43, 44, 45, 46, 47, 48],
        [49, 50, 51, 52, 53, 54, 55, 56],
        [57, 58, 59, 60, 61, 62, 63, 64]]


    # def nieghbors(cell):
    #
    #     i = cell[0]
    #     j = cell[1]

mines = {(2,2), (2,0), (1,0)}
safe = {(0,0), (3,0), (2,1)}
moves_made = {(3,3), (3,2), (3,4)}

def neighbours(cell):

    #width and hieght of the board
    size = 8
    # yeilds all cell values betwwen (i-1) and (j+2)
    #example cell is (6,6); yields all perumutations (i.e. product)
    # of (5,5), (5,6), (5,7); which is (5,5)(5,6),(5,7)(6,5)(6,6)(6,7),(7,5)(7,6)(7,7)
    for c in product(*(range(n-1, n+2) for n in cell)):
        #print(c)
        #filters out c if c == cell and cell is within the board
        if c != cell and all(0 <= n < size for n in c):
            yield c

def neighbours_unknown(cell):
    size = 8

    # yeilds all cell values betwwen (i-1) and (j+2)
    #example cell is (6,6); yields all perumutations (i.e. product)
    # of (5,5), (5,6), (5,7); which is (5,5)(5,6),(5,7)(6,5)(6,6)(6,7),(7,5)(7,6)(7,7)
    all_neighbours = []
    for c in product(*(range(n-1, n+2) for n in cell)):
        #print(c)
        #filters out c if c == cell and cell is within the board
        if c != cell and all(0 <= n < size for n in c):
            all_neighbours.append(c)

    unkown_neighbours = set()

    for cell in all_neighbours:
        if cell not in mines and cell not in safe and cell not in moves_made:
            unkown_neighbours.add(cell)

    return unkown_neighbours

cell = (0,1)

neighbours = list(neighbours(cell))
answer = neighbours_unknown(cell)
print(neighbours)
print (answer)

x = (set(product((range(0, 8)), (range(0,8)))))

print(x)
print(len(x))
