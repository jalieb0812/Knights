from itertools import *
import random
import copy

""" jordan lieber cs50ai project1b minesweeper"""

class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return copy.deepcopy(self.cells)
        else:
            return set()


    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count < 1:
            return copy.deepcopy(self.cells)
        else:
            return set()


        #raise NotImplementedError

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        The mark_mine function should first check to see if cell is one of the
        cells included in the sentence.
        If cell is in the sentence, the function should update the sentence so
        that cell is no longer in the sentence, but still represents a logically
        correct sentence given that cell is known to be a mine.
        If cell is not in the sentence, then no action is necessary.
        """

        #if cell not in sentence then do nohting
            # if cell not in self.cells:
            #     pass

        #if cell in sentence, remove cell and reduce count
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1



        #raise NotImplementedError

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        The mark_safe function should first check to see if cell is one of the
        cells included in the sentence.
        If cell is in the sentence, the function should update the sentence so
         that cell is no longer in the sentence, but still represents a
         logically correct sentence given that cell is known to be safe.
        If cell is not in the sentence, then no action is necessary.
        """
        #if cell not in sentence then do nohting
            # if cell not in self.cells:
            #     pass

        #if cell in sentence, remove cell and reduce count
        if cell in self.cells:
            self.cells.remove(cell)


        #raise NotImplementedError


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)


        # my own function to find all nieghbors of the cell
    def neighbours(self, cell):

        #width and hieght of the board
        size = 8
        neighbours = []
        # yeilds all cell values betwwen (i-1) and (j+2)
        #example cell is (6,6); yields all perumutations (i.e. product)
        # of (5,5), (5,6), (5,7); which is (5,5)(5,6),(5,7)(6,5)(6,6)(6,7),(7,5)(7,6)(7,7)
        for c in product(*(range(n-1, n+2) for n in cell)):
            #print(c)
            #filters out c if c == cell and cell is within the board
            if c != cell and all(0 <= n < size for n in c):
                neighbours.append(c)

        return neighbours

    def neighbours_unknown(self, cell):
        """ returns all nieghbours where status is unkown """
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
            if cell not in self.mines and cell not in self.safes:
                unkown_neighbours.add(cell)

        return unkown_neighbours

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        #mark cell as a move that has been made
        self.moves_made.add(cell)
        #mark cell as safe and update
        self.mark_safe(cell)
        #self.safe.add(cell)

        #add a new sentence to the AI's knowledge base
        #based on the value of `cell` and `count`
        #to indicate that count of the cell’s neighbors are mines.
        #Be sure to only include cells whose state is still undetermined in the sentence.

        print(f"cell: {cell} \n")
        print(f"count: {count} \n")
        neighbours = self.neighbours(cell)



        if len(neighbours) > 0:
            new_sentence = Sentence(neighbours,count)
            #update sentence and count
            for mine in self.mines:
                new_sentence.mark_mine(mine)
            for safe in self.safes:
                new_sentence.mark_safe(safe)
            print(f"new __ sentence: {new_sentence} \n")
            if new_sentence.cells != set():

                self.knowledge.append(new_sentence)


                #check for new safes
        for sentence in self.knowledge:
            if sentence.count == 0:
                copy_cells = copy.deepcopy(sentence.cells)
                #print(f"sentence full of safe cells: {sentence} \n")
                for cell in copy_cells:

                    self.mark_safe(cell)
                self.knowledge.remove(sentence)
        print(f"safe cells: {self.safes - self.moves_made} \n")
        print(f"moves made: {self.moves_made} \n")

        #check for mines

        for sentence in self.knowledge:

            if len(sentence.cells) == sentence.count:
                copy_cells = copy.deepcopy(sentence.cells)
                #print(f"sentence full of mines: {sentence} \n")
                for cell in copy_cells:
                    self.mark_mine(cell)
                self.knowledge.remove(sentence)
        print(f"known_mines: {self.mines} \n")





        for i in range(len(self.knowledge)):
            print(f"knowledge{i}: {self.knowledge[i]} \n")



        inferred_sentences = []


        copy_knowledge = copy.deepcopy(self.knowledge)

        for set1 in self.knowledge:
            #print(f"set1: {set1} \n")
            #copy_knowledge.remove(set1)
            for set2 in copy_knowledge:

                #print(f"set2: {set2} \n")
                if set1.cells != set() and set2.cells != set() and set1 != set2 and set2.cells.issubset(set1.cells):
                    cells = set1.cells - set2.cells
                    count = set1.count - set2.count
                    new_sentence = Sentence(cells, count)
                    print(f"implied sentence set2 subset of set 1: {new_sentence} \n")
                    if new_sentence not in self.knowledge and len(new_sentence.cells) != 0:
                        inferred_sentences.append(new_sentence)



        self.knowledge += inferred_sentences


                    #check for new safes
        for sentence in self.knowledge:
            if sentence.count == 0:
                copy_cells = copy.deepcopy(sentence.cells)
                #print(f"sentence full of safe cells: {sentence} \n")
                for cell in copy_cells:

                    self.mark_safe(cell)
                self.knowledge.remove(sentence)
        #print(f" new safe cells all: {self.safes} \n")
        print(f"new safe cells: {self.safes - self.moves_made} \n")

        #check for mines

        for sentence in self.knowledge:

            if len(sentence.cells) == sentence.count:
                copy_cells = copy.deepcopy(sentence.cells)
                #print(f"sentence full of mines: {sentence} \n")
                for cell in copy_cells:
                    self.mark_mine(cell)
                self.knowledge.remove(sentence)
        print(f"new known_mines: {self.mines} \n")


        #remove empy senteces
        for sentence in self.knowledge:
            if sentence == Sentence(set(), 0):
                self.knowledge.remove(sentence)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """



        safe_moves = self.safes - self.moves_made


        if len(safe_moves) > 0:

            safe_move = safe_moves.pop()

            #safe_move = random.sample(safe_moves, k=1)
            print(f"safe move: {safe_move} \n")
            return safe_move

        if len(safe_moves) <= 0:
            return None





    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """

        # all possible moves
        all_moves = set(product((range(0, 8)), (range(0,8))))

        prohibited_moves = self.moves_made | self.mines

        random_moves = all_moves - prohibited_moves

        #print(f"random moves: {random_moves} \n")

        if len(random_moves) > 0:

            random_move = random.sample(random_moves, k=1)
            print(f"random move: {random_move} \n")

            return random_move[0]

        if len(random_moves) <= 0:
            return None
