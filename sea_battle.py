from random import randrange

class Ships:
    def __init__(self, player):
        self.player = player
        self.amount_max = {1: 4, 2: 2, 3: 1}
        self.reset()

    @property
    def all(self):
        return self._ships

    def reset(self):
        self._ships = []
        self.amount_ships = {1: 0, 2: 0, 3: 0}
        self.lives = 7

    def creating_finished(self):
        for t in self.amount_ships.keys():
            if not self.amount_ships[t] == self.amount_max[t]:
                return False
        return True

    def are_killed(self):
        return self.lives <= 0

    def create(self, inp):
        type = int(inp[0])
        try:
            if type in self.amount_ships.keys():
                if(self.amount_ships[type] < self.amount_max[type]):
                    if len(inp[1:]) == type:
                        ship = {}
                        cells = list(map(int, inp[1:]))
                        if type > 1:
                            rows = [int(i) // 10 for i in cells]
                            columns = [int(i) % 10 for i in cells]
                            rows.sort()
                            columns.sort()
                            for i in range(type - 1, 0, -1):
                                if (rows[i] - rows[i - 1] == 0) and (not columns[i] - columns[i - 1] == 1) and (not columns[i] - columns[i - 1] == -1) or \
                                   (not rows[i] - rows[i - 1] == 1) and (not rows[i] - rows[i - 1] == -1) and (columns[i] - columns[i - 1] == 0) or \
                                   (not rows[i] - rows[i - 1] == 0) and (not columns[i] - columns[i - 1] == 0) or \
                                   (cells[i] == cells[i - 1]):
                                    raise ValueError(f"Incorrect cells: {inp[1:]}")
                        self.amount_ships[type] = self.amount_ships[type] + 1
                        for n in inp[1:]:
                            ship[n] = '+'
                        self._ships.append(ship)
                        if self.player: print(f"Amount ships type {type}: {self.amount_ships[type]}")
                        return True
                    else:
                        raise ValueError("Incorrect amount cells")
                else:
                    raise ValueError(f"Ships type {type} are already created")
            else:
                raise ValueError("Incorrect type")
        except ValueError as e:
            if self.player: print(e)
            return False
            
class Field:
    def __init__(self, player):
        self.player = player
        self._cells = {}
        self.reset()

    @property
    def cells(self):
        return self._cells

    @cells.setter
    def cells(self, inp):
        self._cells.update(inp)

    def reset(self):
         for i in range(1, 7, 1):
             for j in range(1, 7, 1):
                 self._cells[str(i)+str(j)] = ' '

    def check_ship(self, inp):
        for n in inp:
            row_min = max(1, int(n[0])-1)
            row_max = min(6+1, int(n[0])+1+1)
            column_min = max(1, int(n[1])-1)
            column_max = min(6+1, int(n[1])+1+1)
            for r in range(row_min, row_max):
                for c in range(column_min, column_max):
                    cell = str(r) + str(c)
                    if (not cell in self._cells.keys()) or (not self._cells[cell] == ' '):
                        if self.player: print(f"Incorrect cells: {inp}\n")
                        return False
        return True

    def around(self, ship):
        for n in ship.keys():
            row_min = max(1, int(n[0])-1)
            row_max = min(6+1, int(n[0])+1+1)
            column_min = max(1, int(n[1])-1)
            column_max = min(6+1, int(n[1])+1+1)
            for r in range(row_min, row_max):
                for c in range(column_min, column_max):
                    if not (str(r) + str(c)) in ship.keys():
                        self._cells.update({str(r) + str(c): '.'})

class Players:
    def __init__(self, name, field, ships):
        self.name = name
        self.field = field
        self.ships = ships

    def reset(self):
        self.field.reset()
        self.ships.reset()

    def create(self, inp):
        if not self.ships.creating_finished():
            if self.field.check_ship(inp[1:]):
                if self.ships.create(inp):
                    self.field.cells = self.ships.all[len(self.ships.all) - 1]
        if self.ships.creating_finished():
            print(self.name + " is ready")
            return True
        else:
            return False

    def shoot(self, c):
        if not self.field.cells[c] == '.' and not self.field.cells[c] == 'X':
            for i in range(len(self.ships.all)):
                if c in self.ships.all[i].keys():
                    self.ships.all[i].update({c: 'X'})
                    self.field.cells = {c: 'X'}
                    for v in self.ships.all[i].values():
                        if not v == 'X':
                            print("Hit!")
                            return True
                    print("Kill!")
                    self.field.around(self.ships.all[i])
                    self.ships.lives -= 1
                    return True
            print("Lose!")
            self.field.cells = {c: '.'}
            return False
        else:
            if not self.name == "Player": print("Cell have already choosed")
            return None

class Game:
    help_creating = """Ship creating example: t m1n1 m2n2 m3n3\n""" \
                    """t - type (range from 1 to 3)\n""" \
                    """mx - row (range from 1 to 6)\n""" \
                    """nx - column (range from 1 to 6)\n""" \
                    """Input 'restart' for reset\n"""

    help_shooting = """Shoot example: mn\n""" \
                    """m - row (range from 1 to 6)\n""" \
                    """n - column (range from 1 to 6)\n"""

    def draw(self, fpl, fpc):
        print(f"   {Player.name}          {PC.name}\n"\
              "|1|2|3|4|5|6|   |1|2|3|4|5|6|")
        for i in range(1, 7, 1):
            field_player = ""
            field_pc = ""
            for j in range(1, 7, 1):
                c = fpc[str(i)+str(j)]
                if c == '+':
                    c = ' '
                field_player += "|" + fpl[str(i)+str(j)]
                field_pc += "|" + c
            print(field_player + "| " + str(i) + " " + field_pc + "|")
        print("")

    def check(self, inp):
        for i in range(len(inp)):
            if not inp[i].isdigit():
                print("Incorrect input")
                return False
        return True

    def create(self, pl):
        count = 0
        while(True):
            if pl.name == 'Player':
                self.draw(Player.field.cells, PC.field.cells)
                inp = input("Input ship:")
                if inp == "restart":
                    return inp
                else:
                    inp = list(inp.split())
                    if self.check(inp):
                        if pl.create(inp): break
            else:
                count += 1
                if count > 2000:
                    return "restart"
                r = randrange(1, 4, 1)
                inp = str(r)
                for i in range(1, r + 1, 1):
                    inp += ' ' + str(randrange(1, 7, 1)) + str(randrange(1, 7, 1))
                inp = list(inp.split())
                if (pl.create(inp)): break

    def shoot(self, pl1, pl2):
        while (True):
            print(f"{pl1.name} is shooting...")
            if pl1.name == "Player":
                inp = input("Input shoot:")
            else:
                inp = str(randrange(1, 7, 1)) + str(randrange(1, 7, 1))
            if self.check(inp):
                r = pl2.shoot(inp)
                if r == True:
                    self.draw(Player.field.cells, PC.field.cells)
                    if pl2.ships.are_killed():
                        print(f"{pl1.name} won!")
                        return True
                elif r == False:
                    self.draw(Player.field.cells, PC.field.cells)
                    return False

    def process(self):
        while(True):
            new = input("New game Y/N?")
            if new == 'Y' or new == 'y':
                while(True):
                    PC.reset()
                    if self.create(PC) == "restart": continue
                    else: break
                print(self.help_creating)
                Player.reset()
                if self.create(Player) == "restart": continue
                self.draw(Player.field.cells, PC.field.cells)
                print("Let's start!")
                print(self.help_shooting)
                while(True):
                    if self.shoot(Player, PC): break
                    if self.shoot(PC, Player): break
            elif new == 'N' or new == 'n':
                return

Player = Players("Player", Field(True), Ships(True))
PC = Players("Computer", Field(False), Ships(False))

Game = Game()
Game.process()
