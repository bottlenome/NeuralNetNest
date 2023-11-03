import random
import time

class Dice:
     def throw(self):
         return random.randint(1,6)

class Player:
    def __init__(self, name):
        self.name = name
        self.dice = Dice()
        self.score = 0

    def play_turn(self):
        score = self.dice.throw()
        print(f"{self.name} rolled {score}")
        self.score += score
        return score

    def get_score(self):
        return self.score

if __name__ == "__main__":
    print("Welcome to the dice game!")
    player_names = ["Player 1", "Player 2"]
    players = [Player(name) for name in player_names]
    turn = 0
    start_time = time.time()
    while True:
        score = players[turn].play_turn()
        if time.time() - start_time >= 5 or score == 6 or players[turn].get_score() >= 30:
            print(f"{players[turn].name} wins with a score of {players[turn].get_score()}")
            break
        turn = (turn + 1) % len(players) # cycle between players
    print("Game over!")