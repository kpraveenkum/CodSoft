import math
import time
from typing import List, Tuple, Optional
class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.win = None
    def print_board(self):
        print("\n")
        for i in range(0, 9, 3):
            row = self.board[i:i + 3]
            print(" | ".join(row))
            if i < 6:
                print("---------")
        print("\n")
    def print_board_positions(self):
        print("\nPosition reference (0-8):")
        for i in range(0, 9, 3):
            print(" | ".join(str(j) for j in range(i, i + 3)))
            if i < 6:
                print("---------")
        print("\n")
    def available_moves(self) -> List[int]:
        return [i for i, spot in enumerate(self.board) if spot == ' ']
    def empty_squares(self) -> bool:
        return ' ' in self.board
    def num_empty_squares(self) -> int:
        return self.board.count(' ')
    def make_move(self, position: int, letter: str) -> bool:
        if self.board[position] == ' ':
            self.board[position] = letter
            if self.check_win(position, letter):
                self.win = letter
            return True
        return False
    def check_win(self, position: int, letter: str) -> bool:
        row_index = position // 3
        row = self.board[row_index * 3:(row_index + 1) * 3]
        if all([spot == letter for spot in row]):
            return True
        col_index = position % 3
        column = [self.board[col_index + i * 3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True
        if position % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal2]):
                return True
        return False
class AIPlayer:
    def __init__(self, letter: str):
        self.letter = letter
        self.opponent = 'O' if letter == 'X' else 'X'
    def get_move(self, game: TicTacToe) -> int:
        if game.num_empty_squares() == 9:
            return 4
        _, best_move = self.search(
            game,
            self.letter,
            alpha=-math.inf,
            beta=math.inf
        )
        return best_move
    def search(self, game: TicTacToe, current: str, alpha: float, beta: float) -> Tuple[float, Optional[int]]:
        if game.win == self.letter:
            return (1, None)
        elif game.win == self.opponent:
            return (-1, None)
        elif not game.empty_squares():
            return (0, None)
        moves = game.available_moves()
        if current == self.letter:
            best_score = -math.inf
            best_move = None
            for move in moves:
                game.make_move(move, current)
                score, _ = self.search(game, self.opponent, alpha, beta)
                game.board[move] = ' '
                game.win = None
                if score > best_score:
                    best_score = score
                    best_move = move
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            return (best_score, best_move)
        else:
            best_score = math.inf
            best_move = None
            for move in moves:
                game.make_move(move, current)
                score, _ = self.search(game, self.letter, alpha, beta)
                game.board[move] = ' '
                game.win = None
                if score < best_score:
                    best_score = score
                    best_move = move
                beta = min(beta, score)
                if beta <= alpha:
                    break
            return (best_score, best_move)
class HumanPlayer:
    def __init__(self, letter: str):
        self.letter = letter
    def get_move(self, game: TicTacToe) -> int:
        good_move = False
        move = None
        while not good_move:
            try:
                move = int(input(f"Player {self.letter}, enter position (0-8): "))
                if move not in game.available_moves():
                    print("Invalid move! Position already taken or out of range. Try again.")
                else:
                    good_move = True
            except ValueError:
                print("Please enter a valid number (0 to 8)!")
        return move
class GameController:
    def __init__(self):
        self.game = TicTacToe()
        self.human = None
        self.ai = None
        self.turn = None
    def pick_letter(self):
        print("WELCOME TO TIC-TAC-TOE - UNBEATABLE AI")
        while True:
            choice = input("\nDo you want to be X or O? (X goes first): ").upper().strip()
            if choice in ['X', 'O']:
                return choice
            print("Invalid choice! Please enter X or O.")
    def play_game(self):
        human_letter = self.pick_letter()
        ai_letter = 'O' if human_letter == 'X' else 'X'
        self.human = HumanPlayer(human_letter)
        self.ai = AIPlayer(ai_letter)
        if human_letter == 'X':
            self.turn = self.human
            print("You go first! (X)")
        else:
            self.turn = self.ai
            print(" AI goes first! (O)")
        self.game.print_board_positions()
        game_done = False
        start = time.time()
        moves_made = 0
        while not game_done:
            print(f"\n{'-' * 30}")
            if isinstance(self.turn, HumanPlayer):
                print("Your turn:")
            else:
                print("AI is thinking...")
                time.sleep(0.5)
            move = self.turn.get_move(self.game)
            moves_made += 1
            self.game.make_move(move, self.turn.letter)
            self.game.print_board()
            if self.game.win:
                if isinstance(self.turn, HumanPlayer):
                    print(f" well done u won! You won in {moves_made} moves!")
                else:
                    print(f" I wins! Better luck next time! ")
                game_done = True
                break
            if not self.game.empty_squares():
                print(" drow! Well played!")
                game_done = True
                break
            self.turn = self.ai if self.turn == self.human else self.human
        elapsed = time.time() - start
        print("gamee States")
        print(f"Total moves: {moves_made}")
        print(f"Game duration: {elapsed:.2f} seconds")
        print(f"aI algorithm: Minimax with Alpha-Beta Pruning")
        print(f"qI difficulty: Unbeatable")
        self.play_again()
    def play_again(self):
        while True:
            choice = input("\nDo you want to play again? (yes/no): ").lower().strip()
            if choice in ['yes', 'y']:
                self.game = TicTacToe()
                self.play_game()
                break
            elif choice in ['no', 'n']:
                print("thanks for playing! Goodbye!")
                break
            else:
                print("olease enter 'yes' or 'no'")
class SimpleAIPlayer:
    def __init__(self, letter: str):
        self.letter = letter
        self.opponent = 'O' if letter == 'X' else 'X'
    def get_move(self, game: TicTacToe) -> int:
        if game.num_empty_squares() == 9:
            return 4
        _, best_move = self.think(game, self.letter)
        return best_move
    def think(self, game: TicTacToe, current: str) -> Tuple[float, Optional[int]]:
        if game.win == self.letter:
            return (1, None)
        elif game.win == self.opponent:
            return (-1, None)
        elif not game.empty_squares():
            return (0, None)
        moves = game.available_moves()
        if current == self.letter:
            best_score = -math.inf
            best_move = None
            for move in moves:
                game.make_move(move, current)
                score, _ = self.think(game, self.opponent)
                game.board[move] = ' '
                game.win = None
                if score > best_score:
                    best_score = score
                    best_move = move
            return (best_score, best_move)
        else:
            best_score = math.inf
            best_move = None
            for move in moves:
                game.make_move(move, current)
                score, _ = self.think(game, self.letter)
                game.board[move] = ' '
                game.win = None
                if score < best_score:
                    best_score = score
                    best_move = move
            return (best_score, best_move)
if __name__ == "__main__":
    print("TIC-TAC-TOE AI - UNBEATABLE CHALLENGE ")
    print("\nChoose AI version:")
    print("1. optimized AI (Minimax with Alpha-Beta Pruning - Faster)")
    print("2. simple AI (Basic Minimax - Slower but same strategy)")
    choice = input("\nEnter choice (1 or 2): ").strip()
    if choice == "2":
        print("\nstarting game with basic minimax AI...")
        class SimpleGameController(GameController):
            def play_game(self):
                human_letter = self.pick_letter()
                ai_letter = 'O' if human_letter == 'X' else 'X'
                self.human = HumanPlayer(human_letter)
                self.ai = SimpleAIPlayer(ai_letter)
                if human_letter == 'X':
                    self.turn = self.human
                    print("\nYou  first! (X)")
                else:
                    self.turn = self.ai
                    print("\nai goes first! (O)")
                self.game.print_board_positions()
                game_done = False
                moves_made = 0
                while not game_done:
                    print(f"\n{'-' * 30}")
                    move = self.turn.get_move(self.game)
                    moves_made += 1
                    self.game.make_move(move, self.turn.letter)
                    self.game.print_board()
                    if self.game.win:
                        if isinstance(self.turn, HumanPlayer):
                            print("well donee! You won! ")
                        else:
                            print(" I won! Better luck next time! ")
                        break
                    if not self.game.empty_squares():
                        print("it's Drow !")
                        break
                    self.turn = self.ai if self.turn == self.human else self.human
                self.play_again()
        game = SimpleGameController()
        game.play_game()
    else:
        game = GameController()
        game.play_game()
