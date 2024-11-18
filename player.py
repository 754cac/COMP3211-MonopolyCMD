from random import randint
import vars


class Player:

    def __init__(self, name, gameboard_size, game_id):
        self.name = name
        self.id = vars.secure_random_string(9)
        self.location = vars.PLAYER_DEFAULT_PROPERTIES['location']
        self.money = vars.PLAYER_DEFAULT_PROPERTIES['money']
        self.owned_properties = [i for i in vars.PLAYER_DEFAULT_PROPERTIES['owned_properties']] # Directly assign will lead to pass by reference
        self.is_jailed = vars.PLAYER_DEFAULT_PROPERTIES['is_jailed']
        self.jailed_rounds_count_down = vars.PLAYER_DEFAULT_PROPERTIES['jailed_rounds_count_down']
        self.is_retired = vars.PLAYER_DEFAULT_PROPERTIES['is_retired']
        self.gameboard_size = gameboard_size
        self.game_id = game_id

    @staticmethod
    def roll_dice():
        return [randint(1, 4), randint(1, 4)]

    def move(self, steps):
        self.location += steps

    def buy_property(self, location, amount):
        self.money -= amount
        self.owned_properties.append(location)

    def adjust_location(self):
        if self.location >= (self.gameboard_size + 1):
            self.location = self.location % (self.gameboard_size + 1) + 1

    def jailed(self, jail_location):
        self.is_jailed = True
        self.location = jail_location

    def jailbreak(self, jailbreak_price):
        if self.is_jailed:
            if self.jailed_rounds_count_down == 3:
                print(f'{self.name} is jailed for the 1st round and can not make a move!')
                self.jailed_rounds_count_down -= 1

            else:
                if self.jailed_rounds_count_down <= 1:
                    if self.jailed_rounds_count_down == 1 and self.money > jailbreak_price:

                        print(f'{self.name} is jailed for the 3rd round if {self.name} is not paying jailbreak money and {self.name} can not make a double!')

                        selection = vars.handle_question_with_options(f'Pay ${jailbreak_price} to jailbreak immediately [Y / n] ? ', ['y', 'n', ''])

                        if selection.lower() == 'y' or selection.lower() == '':
                            self.money -= jailbreak_price
                            print(f'{self.name} jailbreak success by paying ${jailbreak_price}!')
                            self.is_jailed = False
                            self.jailed_rounds_count_down = 3
                            return self.roll_dice()

                    elif self.jailed_rounds_count_down == 1 and self.money <= jailbreak_price:
                        print(f'{self.name} is jailed for the 3rd round if {self.name} can not make a double!')

                [first_roll, second_roll] = self.roll_dice()
                if self.jailed_rounds_count_down == 2:
                    print(f'{self.name} is jailed for the 2nd round if {self.name} can not make a double!')
                print(f'{self.name} rolled 2 dice : [{first_roll}, {second_roll}]')
                if first_roll == second_roll:
                    print(f'{self.name} jailbreak success by luck!')
                    self.is_jailed = False
                    self.jailed_rounds_count_down = 3
                    return [first_roll, second_roll]
                elif self.jailed_rounds_count_down > 0:
                    print(f'{self.name} jailbreak failed!')
                    self.jailed_rounds_count_down -= 1
                else:
                    print(f'{self.name} is forced to pay ${jailbreak_price} for jailbreak!')
                    self.money -= jailbreak_price
                    self.is_jailed = False
                    self.jailed_rounds_count_down = 3
                    return self.roll_dice()

            return [None, None]
        else:
            return self.roll_dice()

    def retired(self):
        self.is_retired = True
        self.money = 0
        self.owned_properties = []

    def show_status(self):
        if self.is_retired:
            print(f'\nPlayer ID: {self.id}\nPlayer Name: {self.name}\nPlayer is retired: {self.is_retired}')
        elif not self.is_jailed:
            print(f'\nPlayer ID: {self.id}\nPlayer Name: {self.name}\nPlayer Location: {self.location}\nPlayer Money: {self.money}\nPlayer Owned Properties: {self.owned_properties}\nPlayer is jailed: {self.is_jailed}\n')
        else:
            print(f'\nPlayer ID: {self.id}\nPlayer Name: {self.name}\nPlayer Location: {self.location}\nPlayer Money: {self.money}\nPlayer Owned Properties: {self.owned_properties}\nPlayer is jailed: {self.is_jailed}\nRounds to stay in Jail: {self.jailed_rounds_count_down}\n')
