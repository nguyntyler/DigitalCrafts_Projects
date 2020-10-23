from random import randint


class Mob:
    def __init__(self):
        self.health = 10
        self.attack = 4

    def get_hit(self, enemy):
        self.health -= enemy.attack

    def attack(self, enemy):
        enemy.get_hit(self.attack)


class Character(Mob):
    def __init__(self):
        self.health = 15
        self.max_health = 15
        self.bread = 0
        self.attack = 2


class Scene(object):
    NEXT = "None"
    ENEMY = "None"
    first_room = {
        "look_options": ["look", "inspect", "check", "lift"],
        "room_options": ["room", "cell", "around"],
        "window_options": ["window", "bar"],
        "door_options": ["door", "lock"],
        "remove_options": ["break", "smash", "pull", "remove"],
        "window_remove_options": ["break", "climb", "crawl", "escape", "bust", "smash", "leave", "go"],
        "grab_options": ["pick", "grab", "take"],
        "cot": ["cot"],
        "file": ["file"],
        "bar": ["bar"],
        "pick": ["pick"],
        "door": ["door"],
        "lock": ["lock"]
    }
    enemy_actions = [
        "The enemy slashes at you with his sword.",
        "The enemy lunges his sword towards you.",
        "In a sweeping motion, the enemy swings his sword at your head.",
        "The enemy plunges his sword at you."
    ]
    enemy_miss = [
        "You deflected the attack!",
        "The attack misses!",
        "You dodged the attack!",
        "You parry the enemy!",
        "The attack barely grazes you!",
        "Using your shield, you manage to block in time!",
        "You block the attack with your shield!"
    ]
    enemy_hit = [
        "The enemy lands an attack, striking your side.",
        "The enemy's attack lands, slicing your leg.",
        "The enemy manages to strike your leg.",
        ""
    ]
    player_hit = [
        "You land an attack on the enemy!",
        "Your attack connects!",
    ]
    player_miss = [
        "Your attack misses...",
        "You miss..."
    ]

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
        print("   *** Welcome to Escape! Try to get out of the prison. Input your actions as if you were the character. ***")
        return 'cell'


class Cell(Scene):
    def __init__(self):
        self.door_checked = False
        self.have_file = False
        self.bar1_remove = False
        self.bar2_remove = False
        self.bar3_remove = True  # CHANGE BACK

    def enter(self):
        print("You awaken in a concrete cell. Moonlight shines through the window.\nThe only entrance seems to be a metal door.")

        choice = input("> ")

        while True:
            if Scene.choicecheck(self, Scene.first_room,
                                 "look_options", "room_options", choice):
                print("You just see a small metal filer on the ground next to your cot.")
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
            # cotcheck
            elif Scene.choicecheck(self, Scene.first_room, "look_options", "cot", choice):
                print(
                    "It's just a dusty old cot. Useful for sleeping in, but nothing else. You don't find anything of value.")
            # windowcheck
            elif Scene.choicecheck(self, Scene.first_room, "window_options", "look_options", choice):
                print(
                    "The window seems to be boarded up by three small bars. Maybe you can remove these somehow.")
            # Barcheck
            elif Scene.choicecheck(self, Scene.first_room, "bar", "remove_options", choice):
                print("They're too tough to remove through brute force.")
            # havefile
            elif Scene.choicecheck(self, Scene.first_room, "file", "grab_options", choice):
                print("You now have the file.")
                self.have_file = True
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
                    return 'outside'
            else:
                print("I'm not sure what you mean by this.")
            choice = input("> ")


class Outside(Scene):
    Scene.NEXT = "prison corridor"
    Scene.ENEMY = "enemy1"

    def __init__(self):
        self.tent_checked = False

    def enter(self):
        if not self.tent_checked:
            print("\n     ***COMBAT INTRODUCED***\n  ** Battle is now possible **\n   *It's killed or be killed*\n\nAs you make your way outside, you see a tent straight ahead. To your left is another extension of the prison.\nYou can make out a guard on standing watch by the left entrance. \nWith no visible exit in sight, you're left with these two options.")

            choice = input("> ")

            while True:
                if ("straight" in choice) or ("tent" in choice):
                    self.tent_checked = True
                    return 'tent first'
                elif ("left" in choice) or ("prison" in choice):
                    print(
                        "You make your way towards the prison corridor.\nAs you approach, the guard standing post sees you and charges.")
                    return 'battle'
                else:
                    print(
                        "You can only go LEFT towards the prison or RIGHT towards the tent.")
                choice = input("> ")

        elif self.tent_checked:
            print(
                "Exiting the tent, only the entrance to another part of the prison to your right remains.")

            choice = input("> ")

            # while True:

        # print(f"You have {player.health} health.")
        # player.health -= 4
        # print(f"You have {player.health} health left.")
        # exit()


class TentFirst(Outside):
    def enter(self):
        print("yay")
        exit()


# class PrisonCorridor():
#     exit()


class Battle(Scene):
    #   MAKE SCENE.ENEMY INTO AVRIABLE.
    def enter(self):
        print("\n   *** BATTLE ***")

        choice = ""

        while True:
            print(f"\t[HP:{player.health}] [EnemyHP:{Scene.ENEMY.health}")
            print(f"\n * {Scene.enemy_actions[randint(0, 3)]} *\n")
            choice = input("\t[ATTACK] [DEFEND]\n> ").lower()
            if choice == "attack":
                roll = randint(1, 10)
                if roll > 5:
                    print(
                        f"\n * {Scene.player_hit[randint(0, len(Scene.player_hit) - 1)]} *")
                elif roll <= 5:
                    print(
                        f"\n * {Scene.player_miss[randint(0, len(Scene.player_miss) - 1)]} *")


class FinalScene(Scene):

    def enter(self):
        print("the end")
        exit()


class Map(object):

    scenes = {
        'title screen': TitleScreen(),
        'cell': Cell(),
        'outside': Outside(),
        'tent first': TentFirst(),
        'battle': Battle(),
        # 'prison corridor': PrisonCorridor(),
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
enemy1 = Mob()
a_map = Map('battle')
a_game = Engine(a_map)
a_game.play()
