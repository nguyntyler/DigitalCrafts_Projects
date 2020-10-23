from random import randint

opponent_elements = ["water", "fire", "earth"]


def rps(opponent):
    choice = input("Choose an element (Fire, Water, or Earth):\n> ")
    rounds = 0
    while rounds < 3:
        if choice == "water":
            if opponent == "fire":
                print("They chose fire. You win the round.")
                rounds += 1
                print(f"   ***Win {rounds} of 3.***")
            elif opponent == "water":
                print("You both chose water. They cancel each other out.")
            elif opponent == "earth":
                print(f"Your opponent chose earth. You get pummeled with rocks.")
        elif choice == "earth":
            if opponent == "water":
                print("They chose water. You win the round.")
                rounds += 1
                print(f"   ***Win {rounds} of 3.***")
            elif opponent == "earth":
                print("You both chose earth. They cancel each other out.")
            elif opponent == "fire":
                print(f"Your opponent chose fire. You get burned.")
        elif choice == "fire":
            if opponent == "earth":
                print("They chose earth. You win the round.")
                rounds += 1
                print(f"   ***Win {rounds} of 3.***")
            elif opponent == "fire":
                print("You both chose fire. They cancel each other out.")
            elif opponent == "water":
                print(f"Your opponent chose water. You get doused.")
        if rounds < 3:
            choice = input("Choose another element.\n> ")
            opponent = opponent_elements[randint(0, 2)]


rps(opponent_elements[randint(0, 2)])


print("You win the game")
