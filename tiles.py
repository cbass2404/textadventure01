import items
import enemies
import actions
import world


class MapTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def intro_text(self):
        raise NotImplementedError()

    def modify_player(self, player):
        raise NotImplementedError()

    def adjacent_moves(self):
        moves = []
        if world.tile_exists(self.x + 1, self.y):
            moves.append(actions.MoveEast())
        if world.tile_exists(self.x - 1, self.y):
            moves.append(actions.MoveWest())
        if world.tile_exists(self.x, self.y - 1):
            moves.append(actions.MoveNorth())
        if world.tile_exists(self.x, self.y + 1):
            moves.append(actions.MoveSouth())
        return moves

    def available_actions(self):
        moves = self.adjacent_moves()
        moves.append(actions.ViewInventory())

        return moves


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


class ExitCaveRoom(MapTile):
    def intro_text(self):
        return """
        You exit the mouth of the cave, the fresh air is a pleasant change from the putrid stench in the ogre lair.
        Freedom is seen in every direction, you pick the direction of smoke, jingling with your new found wealth.
        Hopefully a bath and fresh food can be found there!
        (To be continued)
        """

    def modify_player(self, player):
        player.victory = True


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

    def available_actions(self):
        if self.enemy.is_alive():
            return [actions.Flee(tile=self), actions.Attack(enemy=self.enemy)]
        else:
            return self.adjacent_moves()


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


class SnakeRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.Snake())

    def intro_text(self):
        if self.enemy.is_alive():
            return """
            As you enter the new room, you hear a soft hissing above the soft whistle of wind in the cracks of the cave.
            Curious about what it is, you light the torch on the nearby wall.
            Just in time!
            A snake slithers it's way towards you!
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
        Scattered about this section of the cave is 5 gold.
        You gather it into your satchel.
        """


class Find100GoldRoom(LootRoom):
    def __init__(self, x, y):
        super().__init__(x, y, items.Gold(100))

    def intro_text(self):
        return """
        Scattered about this section of the cave is 100 gold!
        The bones of the ogres victims lay about as his trophies
        You gather your spoils into your satchel.
        Light lies to the north, the light of a sunrise.
        """
