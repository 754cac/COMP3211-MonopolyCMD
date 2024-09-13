import random

# Constants
NUM_SQUARES = 20
STARTING_MONEY = 1500
NUM_ROUNDS = 100


class Player:
    def __init__(self, player_id, name):
        self.player_id = player_id
        self.name = name
        self.money = 1500  # Starting money
        self.position = 0  # Starting position on the board

    def __str__(self):
        return f"Player ID: {self.player_id}, Name: {self.name}, Money: ${self.money}, Position: {self.position}"


class Board:
    def __init__(self):
        self.squares = self.create_board()

    def create_board(self):
        """Create and return the game board."""
        return [
            "Go",
            "Property 1",
            "Chance",
            "Property 2",
            "Income Tax",
            "Property 3",
            "Free Parking",
            "Property 4",
            "Chance",
            "Property 5",
            "Go to Jail",
            "Property 6",
            "Free Parking",
            "Property 7",
            "Chance",
            "Property 8",
            "Income Tax",
            "Property 9",
            "Free Parking",
            "Property 10",
            "Go",
        ]

    def __str__(self):
        return "\n".join(f"{i + 1}: {square}" for i, square in enumerate(self.squares))


def create_player(player_id):
    """Create a player with a unique ID and prompt for their name."""
    while True:
        try:
            name = input(f"Enter name for Player {player_id + 1}: ").strip()
            if not name:
                raise ValueError("Name cannot be empty.")
            return Player(player_id, name)
        except ValueError as e:
            print(e)


def create_player(player_id):
    """Create a player with a unique ID and prompt for their name."""
    while True:
        try:
            name = input(f"Enter name for Player {player_id + 1}: ").strip()
            if not name:
                raise ValueError("Name cannot be empty.")
            return {"id": player_id, "name": name, "money": 1500, "position": 0}
        except ValueError as e:
            print(e)


def init_game():
    """Initialize the game by asking for the number of players and their names."""
    while True:
        try:
            player_num = int(input("Input number of players (2-6): "))
            if player_num < 2 or player_num > 6:
                raise ValueError("Number of players must be between 2 and 6.")

            players = []
            for i in range(player_num):
                player = create_player(i)
                players.append(player)

            return players  # Return the list of players

        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")


# Roll dice
def roll_dice():
    die1 = random.randint(1, 4)
    die2 = random.randint(1, 4)
    return die1 + die2, isDouble(die1, die2)


def isDouble(die1, die2):
    return die1 == die2

# Example of how to use the classes
if __name__ == "__main__":
    board = Board()  # Create the game board
    print("Game Board:")
    print(board)  # Display the board

    players = init_game()  # Initialize players
    print("\nPlayers initialized:")
    for player in players:
        print(player)  # Display player information