#!/usr/bin/env python3

import random
import time

"""This program plays a game of Rock, Paper, Scissors between two Players,
and reports both Player's scores each round."""

moves = ['rock', 'paper', 'scissors']

def mode():
    print_pause("You're going to play against the computer.\n"
                "How should the computer play?")
    mode = input("1. Rock On! - always plays 'rock'\n"
                    "2. Random - chooses its moves randomly\n"
                    "3. Learn - remembers and imitates your previous move\n"
                    "4. Cycle - cycles through the three moves\n")
    if mode not in ['1', '2', '3', '4']:
        print_pause("I don't understand. Please try again.")
        mode()
    elif mode == '1':
        game = Game(HumanPlayer(), RockPlayer())
        game.play_game(mode)
    elif mode == '2':
        game = Game(HumanPlayer(), RandomPlayer())
        game.play_game(mode)
    elif mode == '3':
        game = Game(HumanPlayer(), ReflectPlayer())
        game.play_game(mode)
    elif mode == '4':
        game = Game(HumanPlayer(), CyclePlayer())
        game.play_game(mode)


"""The Player class is the parent class for all of the Players
in this game"""

def print_pause(message_to_print):
    print(message_to_print)
    time.sleep(1)


class Player():
    def move(self):
        pass

    def learn(self, move1, move2):
        pass


class RockPlayer(Player):
    def __init__(self):
        super().__init__()

    def move(self, mode, game_round):
        return 'rock'

    def learn(self, move1, move2):
        pass


class RandomPlayer(Player):
    def __init__(self):
        super().__init__()

    def move(self, mode, game_round):
        return random.choice(moves)

    def learn(self, move1, move2):
        pass
        # set prior_move to the second variable,
        # passed into the method, which is always
        # the opponent's last move
        #self.prior_move = move2


class ReflectPlayer(Player):
    def __init__(self):
        super().__init__()

    def move(self, mode, game_round):
        # on first round
        if game_round == 0:
            # do a random move
            self.myMove = random.choice(moves)
            return self.myMove
        # on subsequent rounds
        else:
            # use the opponent's prior move
            # which is set by the ReflectPlayer.learn()
            # method in the Game.play_round() method
            self.myMove = self.prior_move
            return self.myMove

    def learn(self, move1, move2):
        # set prior_move to the second variable,
        # passed into the method, which is always
        # the opponent's last move
        self.prior_move = move2


# todo simplify and fix "none"
class CyclePlayer(Player):
    def __init__(self):
        super().__init__()

    prior_moves = []

    def move(self, mode, game_round):
        # when list is full
        while len(self.prior_moves) == len(moves):
            # empty the list
            self.prior_moves.clear()
        # when the list isn't full
        while len(self.prior_moves) <= len(moves):
            # random move
            self.myMove = random.choice(moves)
            # when random move isn't in the list
            if self.myMove not in self.prior_moves:
                # add it to the list
                self.prior_moves.append(self.myMove)
                # return the value
                return self.myMove
            # continue in the loop with another random move
            # until the count of items in the list equals the
            # total number of possible moves

    def learn(self, move1, move2):
        pass
        # set prior_move to the second variable,
        # passed into the method, which is always
        # the opponent's last move
        # self.prior_move = move2


class HumanPlayer(Player):
    def move(self, mode, game_round):
        print_pause("What's your move?")
        human_move = input("rock, paper or scissors\n")
        if human_move not in moves:
            print_pause("I don't understand. Please try again.")
            self.move(mode, game_round)
        else:
            return human_move
    
    def learn(self, move1, move2):
        pass
        # set prior_move to the second variable,
        # passed into the method, which is always
        # the opponent's last move
        # self.prior_move = move2


class Game:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def round_winner(self, move1, move2, game_round):
        if self.beats(move1, move2) is True:
            print_pause("Player 1 won round " + str(game_round + 1))
            self.score1 += 1
        elif self.ties(move1, move2) is True:
            print_pause("Round " + str(game_round + 1) + " is a tie")
        else:
            print_pause("Player 2 won round " + str(game_round + 1))
            self.score2 += 1
        self.print_score(self.score1, self.score2)

    def play_round(self, mode, game_round):
        move1 = self.p1.move(mode, game_round)
        move2 = self.p2.move(mode, game_round)
        self.p1.learn(move1, move2)
        self.p2.learn(move2, move1)
        print_pause(f"Player 1: {move1}  Player 2: {move2}")
        self.round_winner(move1, move2, game_round)

    def play_game(self, mode):
        self.score1 = 0
        self.score2 = 0
        self.game_round = 0
        rounds = int(input("How many rounds would you like to play?\n"))
        print_pause("Game start!")
        for game_round in range(rounds):
            print_pause(f"Round {str(game_round + 1)}:")
            self.play_round(mode, game_round)
        print_pause("Game over!")
        print_pause("Final ")
        self.overall_winner(self.score1, self.score2)

    def beats(self, one, two):
        return ((one == 'rock' and two == 'scissors') or
                (one == 'scissors' and two == 'paper') or
                (one == 'paper' and two == 'rock'))

    def ties(self, one, two):
        return ((one == 'rock' and two == 'rock') or
                (one == 'paper' and two == 'paper') or
                (one == 'scissors' and two == 'scissors'))

    def print_score(self, score1, score2):
        print_pause(f"Score: {self.score1} to {self.score2}")

    def overall_winner(self, score1, score2):
        if self.score1 > self.score2:
            print_pause("Winner: Player 1")
        elif self.score1 == self.score2:
            print_pause("It's a tie")
        else:
            print_pause("Winner: Player 2")
        self.print_score(score1, score2)


if __name__ == '__main__':
    mode()
