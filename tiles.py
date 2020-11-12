import items
import enemies


class MapTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def intro_text(self):
        raise NotImplementedError()

    def modify_player(self, player):
        raise NotImplementedError()


class StartingRoom(MapTile):
    def intro_text(self):
        return """
        You awake in an empty cave.
        The sounds of dripping water echo around you.
        The only light comes from a single torch flickering dimly on the wall.
        Looking around, you notice there are paths going in each direction, each as dark and ominous as the first.
        What do you do?
        """

    def modify_player(self, player):
        pass


class LootRoom(MapTile):
    def __init__(self, x, y, item):
        self.item = item
        super().__init__(x, y)

    def add_loot(self, player):
        player.inventory.append(self.item)

    def modify_player(self, player):
        self.add_loot(player)


class EnemyRoom(MapTile):
    def __init__(self, x, y, enemy):
        self.enemy = enemy
        super().__init__(x, y)

    def modify_player(self, the_player):
        if self.enemy.is_alive():
            the_player.hp = the_player.hp - self.enemy.damage
            print(f"Enemy does {self.enemy.damage} damage. You have {the_player.hp} HP remaining.")


class EmptyCavePath(MapTile):
    def intro_text(self):
        return """
        There's nothing to catch your interest here.
        Keep moving.
        """

    def modify_player(self, player):
        pass


class GiantSpiderRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.GiantSpider())

    def intro_text(self):
        if self.enemy.is_alive():
            return """
            You enter a room similar to the one before.
            Something has changed!
            You hear the click of mandibles and many legs tapping the floor.
            In the dim light you think you see something.
            The outline of a giant spider!
            It attacks.
            """
        else:
            return """
            The corpse of a dead spider rots on the ground.
            """


class OgreRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.Ogre())

    def intro_text(self):
        if self.enemy.is_alive():
            return """
            An ogre is seen in the corner of the room.
            He's bent over a rotting corpse picking the meat from the fly covered cadaver.
            His mangled nose twitches as he sniffs at the air.
            Prepare yourself, he's noticed you!
            """
        else:
            return """
            The corpse of an ogre rots on the ground.
            """


class FindDaggerRoom(LootRoom):
    def __init__(self, x, y):
        super().__init__(x, y, items.Dagger())

    def intro_text(self):
        return """
        You come into another part of the cave.
        In the corner of the room you see the remnants of a body, a hole to the outside is in the roof.
        Through the hole, a beam of moonlight illuminates the remnants of another adventure.
        Nothing but bones remains, but a glint of the light attracts your attention to the dagger.
        You pick it up.
        """


class Find5GoldRoom(LootRoom):
    def __init__(self, x, y):
        super().__init__(x, y, items.Gold(5))

    def intro_text(self):
        return """
        Scattered about the area is gold.
        You gather it into your satchel.
        """
