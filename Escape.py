from random import randint
from os import system, name


class Mob:
    def __init__(self):
        self.health = 10
        self.damage = 4
        self.max_health = 10

    def get_hit(self, enemy):
        self.health -= enemy.damage
        if self.health < 0:
            self.health = 0

    def attack(self, enemy, damage=0):
        enemy.health -= (self.damage - damage)
        if enemy.health < 0:
            enemy.health = 0


class Character(Mob):
    def __init__(self):
        self.health = 15
        self.max_health = 15
        self.bread = 0
        self.damage = 3
        self.have_sword = False
        self.have_shield = False
        self.have_help = False
        self.prison_corridor = False

    def char_interaction(self, choice):
        if "eat" in choice.lower():
            if self.bread > 0:
                self.bread -= 1
                self.health = self.max_health
                print(
                    f"You are now at max health.\n   *Bread remaining: [{player.bread}]")
            else:
                print("   *You don't have any bread!")
        elif "health" in choice.lower():
            print(f"   *Remaining health: [{player.health} | 15]")
        elif "food" in choice.lower():
            print(f"   *Bread remaining: [{player.bread}]")


class Scene(object):
    NEXT = "none"
    first_room = {
        "look_options": ["look", "inspect", "check", "lift", "search"],
        "room_options": ["room", "cell", "around", "tent"],
        "window_options": ["window", "bar"],
        "door_options": ["door", "lock"],
        "remove_options": ["break", "smash", "pull", "remove"],
        "window_remove_options": ["break", "climb", "crawl", "escape", "bust", "smash", "leave", "go"],
        "grab_options": ["pick", "grab", "take"],
        "cot": ["cot", "bed"],
        "file": ["file"],
        "bar": ["bar"],
        "pick": ["pick"],
        "door": ["door"],
        "lock": ["lock"],
        "leave": ["out", "back", "leave"],
        "sword": ["sword"],
        "shield": ["shield"],
        "bread": ["bread"],
        "use": ["unlock", "open", "use"],
    }
    char_interactions_words = {
        "word": ["health", "eat", "food"]
    }
    enemy_actions = [
        "The enemy slashes at you with his sword.",
        "The enemy lunges his sword towards you.",
        "In a sweeping motion, the enemy swings his sword at your head.",
        "The enemy plunges his sword at you.",
        "The enemy thrusts his sword."
    ]
    enemy_miss = [
        "You deflected the enemy's attack!",
        "The enemy's attack misses!",
        "You dodged the enemy's attack!",
        "The enemy's attack barely grazes you!",
        "Using your shield, you manage to block the enemy in time!",
        "You block the enemy's attack with your shield!"
    ]
    enemy_hit = [
        "The enemy lands an attack, striking your side.",
        "The enemy's attack lands, slicing your leg.",
        "The enemy manages to strike your leg.",
        "A swing of the sword from the enemy cuts your arm.",
        "The enemy manages to strike your arm."
    ]
    player_hit = [
        "You land an attack on the enemy!",
        "Your attack connects!",
        "You struck the enemy!",
        "Your attack hits the enemy!"
    ]
    player_miss = [
        "Your attack misses...",
        "You stumble and miss your attack...",
        "You hit nothing...",
        "Your sword just cuts air...",
    ]
    player_parry = [
        "<PARRY> With a swift swing, you manage to strike back the enemy!",
        "<PARRY> With quick reflexes, you parry the enemy and attack them back!",
        "<PARRY> You manage to sneak an attack through to the enemy!",
    ]
    snarky_woman = [
        "\"Just use the key to unlock the door. It's not that hard.\"",
        "\"I'm waiting for you to unlock the door.\"",
        "\"Do you want to unlock the door? Or stay until we die.\"",
        "\"I really don't have all day. Unlock. The. Door.\"",
        "\"Can you unlock the door? Or do I have to do it for you?\""
    ]

    def clear(self):
        if name == "nt":
            _ = system('cls')
        else:
            _ = system('clear')

    def enter(self):
        print("This scene is not yet configured.")
        exit(1)

    def choicecheck(self, room, list1, list2, choice):
        check1 = False
        check2 = False
        for i in room[list1]:
            if i in choice:
                check1 = True
        for j in room[list2]:
            if j in choice:
                check2 = True
        if check1 and check2 == True:
            return True

    def scene_char_check(self, room, list, choice):
        for i in room[list]:
            if i in choice:
                return True


class Engine(object):

    def __init__(self, scene_map):
        self.scene_map = scene_map

    def play(self):
        current_scene = self.scene_map.opening_scene()
        last_scene = self.scene_map.next_scene('final scene')

        while current_scene != last_scene:
            next_scene_name = current_scene.enter()
            current_scene = self.scene_map.next_scene(next_scene_name)

        current_scene.enter()


class TitleScreen(Scene):

    def enter(self):
        print("   *** Welcome to Escape! ***\n Try to get out of the prison. Input your actions as if you were the character.\n")
        return 'cell'


class Cell(Scene):  # DONE
    def __init__(self):
        self.door_checked = False
        self.have_file = False
        self.bar1_remove = False
        self.bar2_remove = False
        self.bar3_remove = False

    def enter(self):
        print("You awaken in a concrete cell. Moonlight shines through the window.\nThe only entrance seems to be a metal door.")

        choice = input("> ").lower()

        while True:
            if Scene.choicecheck(self, Scene.first_room,
                                 "look_options", "room_options", choice):
                if not self.have_file:
                    print(
                        "You just see a small metal filer on the ground next to your cot.")
                if not self.door_checked:
                    print("The metal door looks quite sturdy.")
                elif self.door_checked:
                    print("The metal door is locked.")
                if not self.bar3_remove:
                    print("A barred window shines slight moonlight into the room.")
                elif self.bar3_remove:
                    print("Moonlight shines through a now bar-less window.")
            # doorcheck
            elif Scene.choicecheck(self, Scene.first_room, "look_options", "door_options", choice):
                print("The door is locked. Doesn't look like you can leave this way.")
                self.door_checked = True
            elif Scene.choicecheck(self, Scene.first_room, "window_remove_options", "door_options", choice):
                print("The door is locked. Doesn't look like you can leave this way.")
                self.door_checked = True
            # cotcheck
            elif Scene.choicecheck(self, Scene.first_room, "look_options", "cot", choice):
                print(
                    "It's just a dusty old cot. Useful for sleeping in, but nothing else. You don't find anything of value.")
            # windowcheck
            elif Scene.choicecheck(self, Scene.first_room, "window_options", "look_options", choice):
                if not self.bar3_remove:
                    print(
                        "The window seems to be boarded up by three small bars. Maybe you can remove these somehow.")
                elif self.bar3_remove:
                    print(
                        "All the bars are remove. You can now break through the window!")
            # Barcheck
            elif Scene.choicecheck(self, Scene.first_room, "bar", "remove_options", choice):
                print("They're too tough to remove through brute force.")
            # havefile
            elif Scene.choicecheck(self, Scene.first_room, "file", "grab_options", choice):
                if not self.have_file:
                    print("You now have the file.")
                    self.have_file = True
                elif self.have_file:
                    print("You already have the file.")
            # pickdoor
            elif Scene.choicecheck(self, Scene.first_room, "pick", "door_options", choice):
                if self.have_file:
                    print(
                        "You try but to no avail. Maybe you should use it for what it's actually for. Filing metal.")
                elif not self.have_file:
                    print("You don't have a file on you. Maybe try picking it up?")
            elif Scene.choicecheck(self, Scene.first_room, "file", "lock", choice):  # filelock
                if self.have_file:
                    print(
                        "How can you file a lock? You can't. Try filing something else.")
                elif not self.have_file:
                    print("You don't have a file on you. Maybe try picking it up?")
            elif Scene.choicecheck(self, Scene.first_room, "file", "door", choice):  # filedoor
                if self.have_file:
                    print("This is made of solid metal. You can't do that.")
                elif not self.have_file:
                    print("You don't have a file on you. Maybe try picking it up?")
            elif Scene.choicecheck(self, Scene.first_room, "file", "bar", choice):  # barfile
                if not self.have_file:
                    print("You don't have a file on you. Maybe try picking it up?")
                elif self.have_file and not self.bar1_remove and not self.bar2_remove and not self.bar3_remove:
                    print("You managed to remove one of the bars. There's two left.")
                    self.bar1_remove = True
                elif self.have_file and self.bar1_remove and not self.bar2_remove and not self.bar3_remove:
                    print("Your fingers start to ache but the second bar comes loose.")
                    self.bar2_remove = True
                elif self.have_file and self.bar1_remove and self.bar2_remove and not self.bar3_remove:
                    print(
                        "It takes some time, but after a few minutes you're left with a bar-less window and some very sore fingers.")
                    self.bar3_remove = True
                elif self.have_file and self.bar1_remove and self.bar2_remove and self.bar3_remove:
                    print(
                        "There's nothing left to file. Good thing too, because your fingers wouldn't be able to handle another one.")
            # escapecheck
            elif Scene.choicecheck(self, Scene.first_room, "window_options", "window_remove_options", choice):
                if not self.bar3_remove:
                    print(
                        "The bars are in your way. Doing this is pointless until you can remove them somehow.")
                elif self.bar3_remove:
                    print("You manage to escape.")

                    input("[PRESS RETURN] ")
                    Scene.clear(self)

                    return 'outside'
            else:
                print("I'm not sure what you mean by this.")
            choice = input("> ").lower()


class Outside(Scene):
    Scene.NEXT = 'prison corridor'

    def __init__(self):
        self.tent_checked = False

    def enter(self):
        if not self.tent_checked:
            print(
                "\n     ***COMBAT INTRODUCED***\n   *Battle is now possible*\n   *Type [HEALTH] to check health.\n   *Type [EAT] to replenish health.\n   *Type [FOOD] to check food supply.*\n\nYou make your way outside.\nStraight ahead you see an unguarded tent.\nTo your left is another extension of the prison with a guard standing post.\nWith no visible exit in sight, you're left with these two options.")

            choice = input("> ").lower()

            while True:
                # print(Scene.NEXT)
                if Scene.scene_char_check(self, Scene.char_interactions_words, "word", choice):
                    player.char_interaction(choice)
                elif ("straight" in choice) or ("tent" in choice):
                    self.tent_checked = True

                    input("[PRESS RETURN] ")
                    Scene.clear(self)

                    return 'tent first'
                elif ("left" in choice) or ("prison" in choice):
                    print(
                        "You make your way towards the prison corridor.\n\nAs you approach, the guard standing post sees you and charges.\n\nWith no equipment other than a metal filer to protect you, you're left defenseless!\nThe guard attacks you freely while you do your best to scratch him with your file.\n\nYou did the best you could but your file was no match for his sword.\n\n   *** YOU DIED. ***\n\n")

                    input("[PRESS RETURN] ")
                    Scene.clear(self)

                    return 'death'
                else:
                    print(
                        "You can only go LEFT towards the prison or STRAIGHT towards the tent.")
                choice = input("> ").lower()

        elif self.tent_checked:
            print(
                "Exiting the tent, only the entrance to another part of the prison to your right remains.")

            choice = input("> ").lower()

            while True:
                if Scene.scene_char_check(self, Scene.char_interactions_words,
                                          "word", choice):
                    player.char_interaction(choice)
                elif ("right" in choice) or ("prison" in choice):
                    print(
                        "You make your way towards the prison corridor.\nAs you approach, the guard standing post sees you and charges.")
                    return 'battle'
                else:
                    print("You can only go RIGHT towards the prison.")
                choice = input("> ").lower()


class TentFirst(Scene):  # DONE

    def enter(self):
        print("You make your way to the tent.\nNo one is inside. Luckily.\nKnick-knacks are scattered around.")

        choice = input("> ").lower()
        bread_taken = False

        while True:
            if Scene.scene_char_check(self, Scene.char_interactions_words,
                                      "word", choice):
                player.char_interaction(choice)
            elif Scene.choicecheck(self, Scene.first_room,
                                   "leave", "leave", choice):
                if not player.have_shield:
                    print(
                        "A shield sits in the corner of the tent.\nYou should take that before you go.")
                if not player.have_sword:
                    print(
                        "A sword sits by the table.\nYou should take it. Who knows when it could come in handy.")
                if player.have_sword and player.have_shield:

                    input("[PRESS RETURN] ")
                    Scene.clear(self)

                    return 'outside'
            elif Scene.choicecheck(self, Scene.first_room,
                                   "grab_options", "sword", choice):
                if not player.have_sword:
                    print(
                        "You picked up the sword. \nYou don't know how to use it, but you're going to have to learn quick.")
                    player.have_sword = True
                elif player.have_sword:
                    print("You already have the sword.")
            elif Scene.choicecheck(self, Scene.first_room,
                                   "grab_options", "shield", choice):
                if not player.have_shield:
                    print("You take the shield on your arm.\nIt feels quite sturdy.")
                    player.have_shield = True
                elif player.have_shield:
                    print("You already have the shield.")
            elif Scene.choicecheck(self, Scene.first_room, "grab_options", "bread", choice):
                if not bread_taken:
                    print(
                        "You only see 3 pieces of bread that are even edible. You take them anyways.\nThese can be used to recover health.")
                    bread_taken = True
                    player.bread += 3
                    print(
                        f"You now have {player.bread} pieces of bread.\n   *To check food count, input [FOOD]\n   *To check health, input [health]")
                elif bread_taken:
                    print("You already took all the edible pieces that were left.")
            elif Scene.choicecheck(self, Scene.first_room, "look_options", "room_options", choice):
                print(
                    "You look around the tent. A word is scrawled on the table.\n\n\t\t[PICKLE]\n\nYou're not sure what that means, but you think you should memorize it.")
                if not bread_taken:
                    print(
                        "A few pieces of bread lie on the table. Some appear to be edible.")
                if not player.have_shield:
                    print("You notice a shield lying in the corner of the tent.")
                if not player.have_sword:
                    print(
                        "A lone sword sits perched on the mantle. It could come in handy.")
                if bread_taken and player.have_shield and player.have_sword:
                    print("You see nothing else of value.")
            else:
                print("You can't do that right now!")

            choice = input("> ").lower()


class PrisonCorridor(Scene):  # ADD NEW PATHS

    def enter(self):
        # print(
        # f"PLAYER CORRIDOR SHOULD BE TRUE SENCOND {player.prison_corridor}")
        if not player.prison_corridor:
            player.prison_corridor = True
            print("You make your way past the guard into the prison corridor.\nAs you enter, you see a woman in ragged clothes subduing another guard.\n\n\"Oh hey. I see you're trying to break out as well.\" she says.\n\"I'm looking for a key to the main entrance. It's the only way out.\"\n\"Want to help?\"")

            choice = input("\n\t[YES] [NO]\n> ").lower()
            while True:
                if Scene.scene_char_check(self, Scene.char_interactions_words,
                                          "word", choice):
                    player.char_interaction(choice)
                elif "yes" in choice.lower():
                    player.have_help = True
                    print("A guard enters the corridor behind you and spots you.\nWith inhuman speed, the woman whips out a knife and hurls it at the guard, instantly killing them.\n\n\"Now look. To get through the main entrance, \nwe need a key that's in the prison's control room to your left.\nIt's locked away in a mechanism I'm not familiar with.\nGo there and try to unlock it. Meet me at the main entrance when you have it.\"\n\nShe then darts to the door on the right.\n")

                    input("[PRESS RETURN] ")
                    Scene.clear(self)

                    return 'prison puzzle'
                elif "no" in choice.lower():
                    Scene.NEXT = 'prison corridor'

                    print(
                        "Another guard enters the corridor behind you and spots you.\n\n\"Well,\" she says. \"Looks like you got this covered then.\"\n\nShe runs off to the door to your right.\nDistaught at losing their comrade, the enemy attempts to engage in combat.\nDo you want to heal first?  [YES] [NO]")

                    choice = input("> ").lower()

                    while True:
                        if 'yes' in choice:
                            if player.bread > 0:
                                player.bread -= 1
                                player.health = player.max_health
                                print(
                                    f"You are now at max health.\n   *Bread remaining: [{player.bread}]")
                                return 'battle'
                            else:
                                print("   *You don't have any bread!")
                                return 'battle'
                        elif 'no' in choice:
                            return 'battle'
                        else:
                            print("Choose [YES] or [NO].")

                        choice = input("> ").lower()

                else:
                    print("Choose [YES] or [NO].")

                choice = input("\t[YES] [NO]\n> ").lower()
        elif player.prison_corridor:
            Scene.NEXT = 'prison puzzle'
            print(
                "Now alone with two dead bodies, you see two doors. \nOne to your left and one to your right.\n")

            choice = input("> ").lower()

            while True:
                if 'right' in choice:
                    print(
                        "The door is locked.\nThe strange woman must have locked it behind her.")
                elif 'left' in choice:

                    input("[PRESS RETURN] ")
                    Scene.clear(self)

                    return 'prison puzzle'
                else:
                    print("Choose [LEFT] or [RIGHT]")
                choice = input("> ").lower()


class PrisonPuzzle(Scene):

    def enter(self):
        print("You enter what looks to be the control room. In there you notice the key locked behind a glass door.\nIn front of it lies a keypad.")

        passcode = "pickle"
        choice = input("What do you type in?\n> ").lower()

        errors = 0

        while True:
            Scene.clear(self)
            if choice == passcode:
                Scene.NEXT = 'main entrance'
                print(
                    "The glass door opens revealing the key.\nYou take it.\nA guard spots you.\nYou prepare for battle. Do you want to heal first?  [YES] [NO]")

                choice = input("> ").lower()

                while True:
                    if 'yes' in choice:
                        if player.bread > 0:
                            player.bread -= 1
                            player.health = player.max_health
                            print(
                                f"You are now at max health.\n   *Bread remaining: [{player.bread}]")
                            return 'battle'
                        else:
                            print("   *You don't have any bread!")
                            return 'battle'
                    elif 'no' in choice:
                        return 'battle'
                    else:
                        print("Choose [YES] or [NO].")

                return 'main entrance'
            else:
                Scene.NEXT = 'main entrance'
                if errors < 2:
                    errors += 1
                    print(f"\t\t\t*** ERROR [{errors} | 3] ***\n")
                elif errors == 2:
                    enemy.health = 15
                    print(
                        "Upon the last error, siren blares and a guard enters the control room.\nThis one seems a bit tougher. You should be careful.\nYou prepare for battle. Do you want to heal first?  [YES] [NO]")

                    choice = input("> ").lower()

                    while True:
                        if 'yes' in choice:
                            if player.bread > 0:
                                player.bread -= 1
                                player.health = player.max_health
                                print(
                                    f"You are now at max health.\n   *Bread remaining: [{player.bread}]")
                                return 'battle'
                            else:
                                print("   *You don't have any bread!")
                                return 'battle'
                        elif 'no' in choice:
                            return 'battle'
                        else:
                            print("Choose [YES] or [NO].")

                        choice = input("> ").lower()

            choice = input("What do you type in?\n> ").lower()


class MainEntrance(Scene):

    def enter(self):
        if player.have_help:
            Scene.NEXT = 'final scene'
            print("You somehow find your way to the main entrance.\nThe woman is standing by the exit door.\n\n\"Took you long enough.\" she says.\n\"Now unlock the door with the key.\"")

            choice = input("> ").lower()

            while True:
                if Scene.choicecheck(self, Scene.first_room, "use", "door_options", choice):
                    print(
                        "The door opens up to a shocked guard. He reaches for his sword.\nDo you want to heal first?  [YES] [NO]")

                    choice = input("> ").lower()

                    while True:
                        if 'yes' in choice:
                            if player.bread > 0:
                                player.bread -= 1
                                player.health = player.max_health
                                print(
                                    f"You are now at max health.\n   *Bread remaining: [{player.bread}]")
                                return 'battle'
                            else:
                                print("   *You don't have any bread!")
                                return 'battle'
                        elif 'no' in choice:
                            return 'battle'
                        else:
                            print("Choose [YES] or [NO].")

                        choice = input("> ").lower()
                else:
                    print(
                        f"\n\n{Scene.snarky_woman[randint(0, len(Scene.snarky_woman) - 1)]}\n\n")
                choice = input("> ").lower()
                Scene.clear(self)
        elif not player.have_help:
            Scene.NEXT = 'final scene'
            print("You somehow find your way to the main entrance. As you approach the door, you notice the woman from before show up.\n\n\"HEY! Is that the key?\nUse it on the door!\"\n\n")

            choice = input("> ").lower()

            while True:
                if Scene.choicecheck(self, Scene.first_room, "use", "door_options", choice):
                    print(
                        "The door opens up to a shocked guard. He reaches for his sword.\nDo you want to heal first?  [YES] [NO]")

                    choice = input("> ").lower()

                    while True:
                        if 'yes' in choice:
                            if player.bread > 0:
                                player.bread -= 1
                                player.health = player.max_health
                                print(
                                    f"You are now at max health.\n   *Bread remaining: [{player.bread}]")
                                return 'battle'
                            else:
                                print("   *You don't have any bread!")
                                return 'battle'
                        elif 'no' in choice:
                            return 'battle'
                        else:
                            print("Choose [YES] or [NO].")

                        choice = input("> ").lower()
                else:
                    print(
                        f"\n\n{Scene.snarky_woman[randint(0, len(Scene.snarky_woman) - 1)]}\n\n")
                choice = input("> ").lower()
                Scene.clear(self)


class Battle(Scene):  # DONE
    def enter(self):
        print(
            "\n   *** BATTLE ***   * INPUT [1] TO ATTACK OR [2] DEFEND *\n")
        # print(f"\n * {Scene.enemy_actions[randint(0, 3)]} *\n")
        input("[PRESS RETURN]")
        Scene.clear(self)
        choice = ""

        while True:
            # Scene.clear(self)

            if player.health == 0:
                print("The enemy has slain you..\n\n   *** YOU DIED. ***\n\n")
                return 'death'
            if enemy.health == 0:
                print("\t*VICTORY*\n*You defeated the enemy!*\n")
                enemy.health = enemy.max_health
                return str(Scene.NEXT)

            print(f"\n * {Scene.enemy_actions[randint(0, 3)]} *\n")
            print(f"\t[HP:{player.health}] [EnemyHP:{enemy.health}]\n")
            choice = input("\t[ATTACK] [DEFEND]\n> ").lower()

            if enemy.health != 0 and player.health != 0:
                if choice == "1":
                    roll = randint(1, 10)
                    # roll = 2
                    if roll > 5:
                        print(
                            f"\n * {Scene.player_hit[randint(0, len(Scene.player_hit) - 1)]} *")
                        player.attack(enemy)
                    elif roll <= 5:
                        roll = randint(1, 10)
                        # roll = 7
                        print(
                            f"\n * {Scene.player_miss[randint(0, len(Scene.player_miss) - 1)]} *")
                        if roll > 3:
                            print(
                                f"\n * {Scene.enemy_hit[randint(0, len(Scene.enemy_hit) - 1)]} *")
                            enemy.attack(player)
                        elif roll <= 3:
                            print(
                                f"\n * {Scene.enemy_miss[randint(0, len(Scene.enemy_miss) - 1)]} *")
                elif choice == "2":
                    roll = randint(1, 10)
                    # roll = 2
                    if roll < 3:
                        print(
                            f"\n * {Scene.enemy_hit[randint(0, len(Scene.enemy_hit) - 1)]} *")
                        enemy.attack(player)
                    elif roll >= 3:
                        roll = randint(1, 10)
                        # roll = 7
                        print(
                            f"\n * {Scene.enemy_miss[randint(0, len(Scene.enemy_miss) - 1)]} *")
                        if roll > 5:
                            print(
                                f"\n * {Scene.player_parry[randint(0, len(Scene.player_parry) - 1)]} *")
                            player.attack(enemy, 1)

                else:
                    print("   * Input [1] to attack or [2] to defend *\n")
            print(f"\t[HP:{player.health}] [EnemyHP:{enemy.health}]\n")
            input("\t[PRESS RETURN] ")
            Scene.clear(self)


class FinalScene(Scene):

    def enter(self):
        print("\n\t** You made it out alive! **\n\t\t* You win! *\n")
        exit()


class Death(Scene):

    def enter(self):
        print("*** That was a good try. Do better next time. ***\n")
        exit(1)


class Map(object):

    scenes = {
        'title screen': TitleScreen(),
        'cell': Cell(),
        'outside': Outside(),
        'tent first': TentFirst(),
        'battle': Battle(),
        'death': Death(),
        'prison corridor': PrisonCorridor(),
        'prison puzzle': PrisonPuzzle(),
        'main entrance': MainEntrance(),
        'final scene': FinalScene()
    }

    def __init__(self, start_scene):
        self.start_scene = start_scene

    def next_scene(self, scene_name):
        val = Map.scenes.get(scene_name)
        return val

    def opening_scene(self):
        return self.next_scene(self.start_scene)


player = Character()
enemy = Mob()
a_map = Map('main entrance')
a_game = Engine(a_map)
a_game.play()
