#!/usr/bin/env python3

import random
import time

"""This program plays a game of Rock, Paper, Scissors between two Players,
and reports both Player's scores each round."""

moves = ['rock', 'paper', 'scissors']

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


class RandomPlayer(Player):
    def __init__(self):
        super().__init__()

    def move(self, mode):
        return random.choice(moves)


class ReflectPlayer(Player):
    def __init__(self):
        super().__init__()

    def move(self, game_round):
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



class CyclePlayer(Player):
    def __init__(self):
        super().__init__()

    def prior(self):
        self.prior_moves = []

    def cycle(self, prior_moves):
        self.cycle_move = random.choice(moves)
        if self.cycle_move not in self.prior_moves:
            self.prior_moves.append(self.move)
            return self.cycle_move
        else:
            self.cycle(self.prior_moves)

    def move(self, game_round):
        if game_round == 0:
            self.prior()
            self.cycle_move = random.choice(moves)
            self.prior_moves.append(self.cycle_move)
            return self.cycle_move
        else:
            self.compare = set(moves).difference(self.prior_moves)
            if len(self.compare) == 0:
                self.prior_moves.clear()
            self.cycle_move = self.cycle(self.prior_moves)
            return self.cycle_move


class HumanPlayer(Player):
    def move(self, mode):
        print_pause("What's your move?")
        human_move = input("rock, paper or scissors\n")
        if human_move not in moves:
            print_pause("I don't understand. Please try again.")
            self.move(mode)
        else:
            return human_move


""" class Winner(Player):
    def __init__(self):
        super().__init__() """


class set_mode():
    def __init__(self):
        super().__init__()

    def mode(self):
        print_pause("Please enter the mode you "
                    "would like to play:")
        mode = input("1. Human vs Computer\n"
                     "2. Computer vs Computer (random)\n"
                     "3. Computer vs Computer (reflect)\n"
                     "4. Computer vs Computer (cycle)\n")
        if mode not in ['1', '2', '3', '4']:
            print_pause("I don't understand. Please try again.")
            set_mode.mode(self)
        elif mode == '1':
            game = Game(HumanPlayer(), RandomPlayer())
            game.play_game(mode)
        elif mode == '2':
            game = Game(RandomPlayer(), RandomPlayer())
            game.play_game(mode)
        elif mode == '3':
            game = Game(ReflectPlayer(), ReflectPlayer())
            game.play_game(mode)
        elif mode == '4':
            game = Game(CyclePlayer(), CyclePlayer())
            game.play_game(mode)


""" def random_move(self):
    return random.choice(moves) """


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
        if mode in ('1', '2'):
            move1 = self.p1.move(mode)
            move2 = self.p2.move(mode)
        elif mode == '3':
            move1 = self.p1.move(game_round)
            move2 = self.p2.move(game_round)
            self.p1.learn(move1, move2)
            self.p2.learn(move2, move1)
            # on the first round make a random move
            # and store the moves in instance variables
            """ if game_round == 0:
                move1 = random.choice(moves)
                move2 = random.choice(moves)
                self.p1.learn(move1, move2)
                self.p2.learn(move1, move2)
            # on subsequent rounds
            else:
                # use the opponent's last move
                move1 = self.p1.last_move2
                move2 = self.p2.last_move1
                # reset the game last_move variables for the next round
                self.p1.learn(move1, move2)
                self.p2.learn(move1, move1) """
        elif mode == '4':
            move1 = self.p1.move(game_round)
            move2 = self.p2.move(game_round)
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
    self = ''
    set_mode.mode(self)
