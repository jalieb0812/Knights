from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    #Implication(AKnight, Not(AKnave)),
    #Implication(AKnave, Not(AKnight)),
    #Not(And(AKnight, AKnave )),

    #structure of the problem
    # A is a night or a knave but not both
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),

    #Statment given
    #if A is a night then A is a knight and a Knave
    Implication(AKnight, And(AKnight, AKnave)),
    # if A is a knihgt and a knave, then a is a knight
    Implication(And(AKnight, AKnave), AKnight)# TODO
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    #structure of the problem
    # A is a night or a knave but not both
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),

    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),

    #statements given
    Biconditional(AKnight, And(AKnave, BKnave))

    #statements given
    #And(AKnave, BKnave)
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    #structure of the problem
    # A is a night or a knave but not both

    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    # B is a night or a knave but not both
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),

    # Since A and B cannot both be telling the truth, I know one is a Knave
    Or(AKnave, BKnave),

    #if A is the Knight, Then B also as to be a KNight, but I know one has to be a Knaves
    # so I know the A is the Knave
    Implication(AKnight, BKnight),

    #and if A is the Knave, then B is a Knight
    Implication(AKnave, BKnight),

    #statements given
    #A and B are knights if and only if A and B are not Knaves
        # Biconditional(And(AKnight, BKnight), And(Not(AKnave), Not(BKnave))),
        # Biconditional(And(AKnave, BKnave), And(Not(AKnight), Not(BKnight))),

        # Implication(Or(And(AKnight, BKnight), And(AKnave, BKnave)), Not(Or(AKnave, BKnave))),
    #Implication(Or(AKnight, BKnight), Not(AKnave)),
    # if a is a knight then B is a night

    #Implication(And(AKnight, Not(BKnight)), BKnave),


    #trying to see if can deduce info on C
        # Biconditional(CKnight, And(AKnight, BKnight)),
        # Biconditional(CKnave, And(AKnave, BKnave)),

)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    #structure of the problem
    # A is a night or a knave but not both

    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    # B is a night or a knave but not both
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),

    And(Or(CKnight, CKnave), Not(And(CKnight, CKnave))),


    #B must be a Knave since A cant say Im a Knave b/c a Knave can say that;


    # statements
    # if B is a Knave then C and A are Knights
    #Implication(BKnave, And(CKnight, AKnight)),

    #B is a Knave if and only if C and A are Knights
    Biconditional(BKnave, And(CKnight, AKnight)),

    # if B is a Knight, then C and A are Knaves
    Implication(BKnight, And(CKnave, AKnave )),

    # A and B are both Knights if and only if C is a Knave
    Biconditional(And(AKnight, BKnight), CKnave)



)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
