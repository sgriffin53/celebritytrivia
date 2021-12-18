import wikipedia
import random

def newquestion(celebrities, numclues):
    randnum = random.randint(0, len(celebrities) - 1)
    origname = celebrities[randnum]
    page = wikipedia.page(origname, auto_suggest=False)
    lines = page.content.split("\n")

    clues = []
    potentialclues = []
    censorednames = []
    for namepiece in origname.split(" "):
        censorednames.append(namepiece)
    j = -1
    for namepiece in censorednames:
        j += 1
        if len(namepiece) <= 1: censorednames.pop(j)
    i = -1
    for line in lines:
        i += 1
        line = line.replace("Dr. ", "Dr ").replace("Mr. ", "Mr ").replace("Gen. ", "Gen ").replace("No. ", "No ").replace("U.S. ", "US ")
        sentences = line.split(". ")
        if "== Awards" in line or "== Legacy and awards" in line or "== Titles" in line or "== External" in line or "== Filmography" in line or "== Discography" in line\
                or "== See also" in line or "== Electoral history" in line or "== Authored books" in line\
                or "== References" in line:
            break
        if "==" in sentences[0]: continue
        if sentences[0] == "": continue
        if len(sentences[0]) <= 10 and len(sentences) > 1:
            sentences[0] += "." + sentences[1]
        if i == 0:
            if len(sentences[0]) <= 10:
                sentences[0] += "." + sentences[1]
            name = sentences[0].split(" is ")[0]
            name = name.split(" was ")[0]
            name = name.split(" (born")[0]
            for namepiece in name.split(" "):
                censorednames.append(namepiece)
            censoredline = sentences[0]
            for word in censorednames:
                censoredline = censoredline.replace(word, "XXX")
            line = censoredline + "."
            continue
        j = -1
        for namepiece in censorednames:
            j += 1
            if len(namepiece) <= 1: censorednames.pop(j)

        # censor celebrity's name

        censoredline = sentences[0]
        for word in censorednames:
            censoredline = censoredline.replace(word, "XXX")
        line = censoredline + "."

        potentialclues.append(line)

    j = -1
    for clue in potentialclues:
        j += 1
        if len(clue) <= 7:
            potentialclues.pop(j)

    if len(potentialclues) < numclues:
        return (-1, -1)
    for i in range(numclues):
        randnum = random.randint(0, len(potentialclues) - 1)
        clue = potentialclues[randnum]
        potentialclues.pop(randnum)
        clues.append(clue)

    i = 0
    for clue in clues:
        i += 1
        print("Clue " + str(i) + ": " + clue)
        print("")

    guess = input("Guess the celebrity: ")
    answer = origname
    return (guess, answer)

def playGame(celebrities):
    numquestions = 12
    numclues = 4
    print("Welcome to Celebrity Trivia")
    print("")
    print(
        "For each question, you will be given five facts about a celebrity that have been taken from wikipedia and guess the celebrity.")
    print("")
    input("Press enter to play")
    repeat = True
    while repeat:
        repeat = False
        print("Choose game length")
        print("1. Short (5 questions)")
        print("2. Medium (12 questions)")
        print("3. Long (20 questions)")
        choice = int(input("Enter choice: (1, 2 or 3):"))
        if choice not in [1, 2, 3]:
            repeat = True
        if choice == 1:
            numquestions = 5
        elif choice == 2:
            numquestions = 12
        else:
            numquestions = 20
    print("")
    repeat = True
    while repeat:
        repeat = False
        print("Choose game difficulty")
        print("1. Easy (6 clues)")
        print("2. Medium (4 clues)")
        print("3. Hard (2 clues)")
        choice = int(input("Enter choice: (1, 2 or 3):"))
        if choice not in [1, 2, 3]:
            repeat = True
        if choice == 1:
            numclues = 6
        elif choice == 2:
            numclues = 4
        else:
            numclues = 2
    print("")
    print(str(numquestions) + " questions - " + str(numclues) + " clues")
    print("")
    x = input("Press enter to begin")
    repeat = True
    questionnum = 0
    correctanswers = 0
    while repeat:
        questionnum += 1
        print("Question " + str(questionnum))
        validquestion = False
        while not validquestion:
            validquestion = True
            (guess, answer) = newquestion(celebrities, numclues)
            if guess == -1 or answer == -1:
                validquestion = False
        if guess.lower() == answer.lower():
            print("Correct!")
            correctanswers += 1
        else:
            print("Incorrect. The celebrity was " + answer)
        if questionnum == numquestions:
            repeat = False
            break
        x = input("Press enter for next question.")
    percentage = correctanswers * 100 / numquestions
    print("You scored " + str(round(percentage,1)) + "% (" + str(correctanswers) + "/" + str(numquestions) + ")")
    print("Thanks for playing.")
    x = input("")


celebrities = []
ff = open('celebs.txt','r')
totlines = 0
for line in ff.readlines():
    totlines+=1
    celebrities.append(line.split('\n')[0])
ff.close()

playGame(celebrities)