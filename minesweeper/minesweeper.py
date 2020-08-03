import itertools
from itertools import *
import random


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
            return self.cells
        else:
            return set()


        raise NotImplementedError

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
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
        if cell not in self.cells:
            return False

        #if cell in sentence, remove cell and reduce count
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
            return True


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
        if cell not in self.cells:
            return False

        #if cell in sentence, remove cell and reduce count
        if cell in self.cells:
            self.cells.remove(cell)
            return True

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
        # yeilds all cell values betwwen (i-1) and (j+2)
        #example cell is (6,6); yields all perumutations (i.e. product)
        # of (5,5), (5,6), (5,7); which is (5,5)(5,6),(5,7)(6,5)(6,6)(6,7),(7,5)(7,6)(7,7)
        for c in product(*(range(n-1, n+2) for n in cell)):
            print(c)
            #filters out c if c == cell and cell is within the board
            if c != cell and all(0 <= n < size for n in c):
                yield c

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
            if cell not in self.mines and cell not in self.safes and cell not in self.moves_made:
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
        unknown_neighbours = self.neighbours_unknown(cell)

        new_sentence = Sentence(unknown_neighbours,count)

        self.knowledge.append(new_sentence)

#If, based on any of the sentences in self.knowledge,
#new cells can be marked as safe or as mines, then the function should do so.


        safe_sub = set()
        mine_sub = set()

        for sentence in self.knowledge:
            #remove empy sentences
            if len(sentence.cells) == 0:
                self.knowledge.remove(sentence)

            else:
                for cell in self.safes:

                    #add any new discovered safe spaces
                    safes = sentence.known_safes()
                    mines = sentence.known_mines()

                    safe_sub |= safes
                    mine_sub |= mines


        for safe_cell in safe_sub:
            self.mark_safe(safe_cell)

    #add any new discovered mine spaces

        for mine_cell in mine_sub:
            self.mark_mine(mine_cell)

            #
            # for sentence in self.knowledge:
            #
            #     # if the count is zero, then mark all cells as safe
            #     if sentence.count == 0:
            #         for cell in sentence.cells:
            #             sentence.mark_safe(cell)
            #             #self.mark_safe(cell)
            #             #remove the sentence since we know all the values
            #             self.knowledge.remove(sentence)
            #
            # for sentence in self.knowledge:
            #     # if the count is eqaul to len(cells), then mark all cells as mines
            #     if len(sentence.cells) == sentence.count:
            #         for cell in sentence.cells:
            #             sentence.mark_mine(cell)
            #             #self.mark_mine(cell)
            #             #remove the sentence since we know all the values
            #             self.knowledge.remove(sentence)



        #update/add knowledge based subset method

        tknowledge = list(self.knowledge)

        print(f"knowledge: {tknowledge} \n")

        #current_sentence = next_sentence

        set1 = new_sentence.cells
        count1 = new_sentence.count
            # set1 = self.knowledge[0].cells
            # count1 = self.knowledge[0].count

        inferred_sentences = []


        for sentence in self.knowledge:
            print(f"set1: {set1} \n")
            print(f"count1: {count1} \n")
            if len(sentence.cells) ==  0:
                self.knowledge.remove(sentence)

            elif set1 == sentence.cells:
                break
            else:
                set2 = sentence.cells
                count2 = sentence.count
                print(f"set2: {set2} \n")
                print(f"count2: {count2} \n")
                if set1.issubset(set2):
                    new_sentence = Sentence((set2-set1), (count2 - count1))
                    print(f"new sentence: {new_sentence} \n")
                    inferred_sentences.append(new_sentence)
                    print(f"inffered sentences: {inferred_sentences} \n")

            set1 = sentence.cells
            count1 = sentence.count


        for sentence in inferred_sentences:
            self.knowledge.append(sentence)







        #raise NotImplementedError

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """



        safe_moves = self.safes - self.moves_made
        print(f"safe moves: {safe_moves} \n")
        print(f"known mines: {self.mines} \n")

        if len(safe_moves) > 0:

            safe_move = random.sample(safe_moves, k=1)
            print(f"safe move: {safe_move} \n")
            return safe_move[0]

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

        print(f"random moves: {random_moves} \n")

        if len(random_moves) > 0:

            random_move = random.sample(random_moves, k=1)
            print(f"random move: {random_move} \n")

            return random_move[0]

        if len(random_moves) <= 0:
            return None
