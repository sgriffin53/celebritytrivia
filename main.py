import wikipedia
import random


def newquestion(celebrities, numclues):

    randnum = random.randint(0, len(celebrities) - 1)
    origname = celebrities[randnum]
    page = wikipedia.page(origname, auto_suggest=False)
    lines = page.content.split("\n")

    clues, potential_clues = [], []
    censored_names = [name for name in origname.split() if len(name) > 1]

    for i, line in enumerate(lines):
        line = line.replace("Dr. ", "Dr ").replace("Mr. ", "Mr ").replace("Gen. ", "Gen ").replace("No. ", "No ").replace("U.S. ", "US ")
        sentences = line.split(". ")

        matches = [
            "== Awards", "== Legacy and awards", "== Titles",  "== External", "== Filmography",
            "== Discography", "== See also", "== Electoral history", "== Authored books", "== References"
        ]
        if any(match in line for match in matches):
            break

        if "==" in sentences[0]: continue
        if sentences[0] == "": continue
        if 1 < len(sentences[0]) <= 10:
            sentences[0] += "." + sentences[1]

        if i == 0:
            if len(sentences[0]) <= 10:
                sentences[0] += "." + sentences[1]
            name = sentences[0].split(" is ")[0]
            name = name.split(" was ")[0]
            name = name.split(" (born")[0]
            for namepiece in name.split(" "):
                censored_names.append(namepiece)
            censoredline = sentences[0]
            for word in censored_names:
                censoredline = censoredline.replace(word, "____")
            line = censoredline + "."
            continue

        censored_names = [name for name in censored_names if len(name) > 1]
        # censor celebrity's name
        censoredline = sentences[0]
        for word in censored_names:
            censoredline = censoredline.replace(word, "____")
        line = censoredline + "."

        potential_clues.append(line)

    for j, clue in enumerate(potential_clues):
        if len(clue) <= 7:
            potential_clues.pop(j)

    if len(potential_clues) < numclues:
        return (-1, -1)

    for i in range(numclues):
        randnum = random.randint(0, len(potential_clues) - 1)
        clue = potential_clues[randnum]
        potential_clues.pop(randnum)
        clues.append(clue)

    for i, clue in enumerate(clues, start=1):
        print(f"Clue {i}: {clue}\n")

    guess = input("Guess the celebrity: ")
    return guess, origname


def playGame(celebrities):

    numquestions, numclues = 12, 4
    print("Welcome to Celebrity Trivia\n")
    print(
        "For each question, you will be given five facts about a celebrity that have been taken from wikipedia and guess the celebrity.\n")
    input("Press enter to play")

    length = True
    while length:
        length = False
        print("Choose game length")
        print("1. Short (5 questions)")
        print("2. Medium (12 questions)")
        print("3. Long (20 questions)")
        choice = int(input("Enter choice: (1, 2 or 3): "))

        match choice:
            case 1: numquestions = 5
            case 2: numquestions = 12
            case 3: numquestions = 20
            case _: repeat = True

    difficulty = True
    while difficulty:
        difficulty = False
        print("\nChoose game difficulty")
        print("1. Easy (6 clues)")
        print("2. Medium (4 clues)")
        print("3. Hard (2 clues)")
        choice = int(input("Enter choice: (1, 2 or 3):"))

        match choice:
            case 1: numclues = 6
            case 2: numclues = 4
            case 3: numclues = 2
            case _: repeat = True

    print(f"\n{numquestions} questions - {numclues} clues\n")
    user_continues = input("Press enter to begin ")
    questionnum, correctanswers = 0, 0

    gameloop = True
    while gameloop:

        questionnum += 1
        print(f"Question {questionnum}")

        validquestion = False
        while not validquestion:
            validquestion = True
            guess, answer = newquestion(celebrities, numclues)
            if guess == -1 or answer == -1:
                validquestion = False

        if guess.lower() == answer.lower():
            print("Correct!")
            correctanswers += 1

        # For debugging
        if guess.lower() == "debug":
            print(f"Debugging. The celebrity is {answer}")
            correctanswers += 1

        else:
            print(f"Incorrect. The celebrity was {answer}")

        if questionnum == numquestions:
            gameloop = False
            break

        user_continue = input("Press enter for next question.")

    percentage = correctanswers * 100 / numquestions
    print(f"You scored {round(percentage, 1)} % ({correctanswers}/{numquestions})\nThanks for playing.")


with open('celebs.txt', 'r') as ff:
    celebrities = [line.split('\n')[0] for line in ff.readlines()]

playGame(celebrities)