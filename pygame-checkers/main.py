from time import time
from functools import wraps
from random import choice
import pygame


# Constants
pygame.init()
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

BGBLACK = (0, 0, 0)
BLACK = (10, 10, 10)
BGWHITE = (255, 255, 255)
WHITE = (140, 140, 140)
BORDER_BLACK = (50, 50, 50)
BORDER_WHITE = (190, 190, 190)
GREEN = (56, 112, 28)
RED = (128, 0, 0)

FPS = 60
CLOCK = pygame.time.Clock()
CROWN_WHITE = pygame.transform.scale(pygame.image.load('images/crown_white.jpg'), (35, 35))
CROWN_BLACK = pygame.transform.scale(pygame.image.load('images/crown_black.jpg'), (35, 35))

FOUT = open('logs/last_game.txt', 'w')

NORMAL_FONT = pygame.font.SysFont('Helvetica', 32)
TITLE_FONT = pygame.font.SysFont('Helvetica', 64)
ERROR_FONT = pygame.font.SysFont('Helvetica', 20)
# # # # # #

def write_output(s):
    print(s)
    FOUT.write(s + '\n')

class BoardGame:
    def __init__(self, window, copy=False):
        '''
            Object used to store and draw a checkers board.\n
            Makes use of the Piece class for storing board state.
        '''
        self.window = window
        self.board = []
        self.black_remaining = self.white_remaining = 12
        self.black_kings = self.white_kings = 0
        self.selected_piece = None
        self.move_no = 0
        if not copy:
            self.start_time = pygame.time.get_ticks() // 1000
            self.create_board()
    
    def draw_squares(self, window):
        '''
            Draws the black and white grid of the checkers board.
        '''
        # draws the grid by drawing the white squares over a black surface
        # white squares are drawn starting at index 0 for even rows and index 1 for odd rows
        window.fill(BGBLACK)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(window, BGWHITE, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), border_radius=3)

    def create_board(self):
        '''
            Creates the starting board state with objects from the Piece class.
        '''
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == (row + 1) % 2:
                    if row < 3:
                        self.board[row].append(Piece(row, col, BLACK))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, WHITE))
                    else:
                        self.board[row].append(Piece(row, col))
                else:
                    self.board[row].append(Piece(row, col))
    
    def evaluate_score(self):
        '''
            Returns score based on the difference between the number of remaining pieces for each side.\n
            This way of calculating the score works because usually the side with more pieces has a higher chance to win.\n
            Kings are counted as being 2 pieces, so the AI is more likely to go for making a king piece.
        '''
        score = self.black_remaining - self.white_remaining + self.black_kings - self.white_kings
        if self.move_no % 2 == 1:
            score *= -1
        return score

    def game_over(self):
        '''
            Returns the winning color RGB tuple if the game is over, False otherwise.\n
            The game is over when there are 0 white or black pieces, or when one of the players can't make a move.
        '''
        if self.black_remaining == 0:
            return WHITE
        if self.white_remaining == 0:
            return BLACK
        black_moves = [self.generate_legal_moves(self.get_piece(i, j)) for i in range(ROWS) for j in range(COLS) if self.get_piece(i, j).color == BLACK]
        if len(black_moves) == 0:
            return WHITE
        white_moves = [self.generate_legal_moves(self.get_piece(i, j)) for i in range(ROWS) for j in range(COLS) if self.get_piece(i, j).color == WHITE]
        if len(white_moves) == 0:
            return BLACK
        return False

    def get_piece(self, row, col):
        def in_bounds(x, y):
            return x >= 0 and x < ROWS and y >= 0 and y < COLS
        return self.board[row][col] if in_bounds(row, col) else None
    
    def draw(self):
        '''
            First, this method draws the square grid, then it uses the draw method of the Piece class to draw the pieces.\n
            If any piece is currently selected, this method determines its legal moves and uses the draw method of the Piece class to highlight them.
        '''
        self.draw_squares(self.window)
        legal_moves = []
        # get a list of all legal moves of selected piece
        if self.selected_piece:
            legal_moves = list(map(lambda p : p[0], self.generate_legal_moves(self.selected_piece)))
            legal_moves.append((self.selected_piece.row, self.selected_piece.col))
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                # all legal moves are made to an empty square 
                # the piece.draw function treats the selected_piece and the empty destination squares separately, though both are passed with selected=True
                piece.draw(self.window, selected=True if (piece.row, piece.col) in legal_moves else False)
    
    def generate_legal_moves(self, piece):
        '''
            Returns a list of tuples where each tuple represents:\n
                ((move_square_x, move_square_y), 'notake' if piece doesn't capture else addr_captured_piece)
        '''
        moves = []
        can_take = False
        for x in piece.directions:
            for y in [-1, 1]:
                # diagonal square coordinates
                new_row = piece.row + x
                new_col = piece.col + y
                new_piece = self.get_piece(new_row, new_col)
                # If there's an empty square on a diagonal it gets added.
                if new_piece and new_piece.is_empty():
                    moves.append([(new_row, new_col), 'notake'])
                # If there's an occupied cell on the diagonal it checks if the piece can be captured.
                elif new_piece and not new_piece.is_empty():
                    # coordinates of final square, after capture
                    jump_row = new_row + x
                    jump_col = new_col + y
                    jump_piece = self.get_piece(jump_row, jump_col)
                    # if final square is empty and the inbetween piece is of a different color, then it can be captured
                    if jump_piece and jump_piece.is_empty() and piece.color != new_piece.color:
                        can_take = True
                        moves.append([(jump_row, jump_col), new_piece])
        # If any capture is possible remove all non-capture moves.
        if can_take:
            moves = list(filter(lambda move : True if move[1] != 'notake' else False, moves))     
        return moves
    
    def get_deepcopy(self):
        new_board = BoardGame(self.window, copy=True)
        for row in range(len(ROWS)):
            new_board.board.append([])
            for col in range(len(COLS)):
                new_board.board[row].append(self.board[row][col].get_deepcopy())
        new_board.black_remaining, new_board.white_remaining = self.black_remaining, self.white_remaining
        new_board.black_kings, new_board.white_kings = self.black_kings, self.white_kings
        if self.selected_piece:
            new_board.selected_piece = new_board.get_piece(self.selected_piece.row, self.selected_piece.col)
        new_board.move_no = self.move_no
        return new_board
    
    def remove_piece(self, piece):
        if piece.color == WHITE:
            if piece.king:
                self.white_kings -= 1
            self.white_remaining -= 1
        elif piece.color == BLACK:
            if piece.king:
                self.black_kings -= 1
            self.black_remaining -= 1
        piece.remove()
    
    def move(self, piece, row, col):
        '''
            If the move of piece to the square at (row, col) is valid, then it executes it.\n
            Return values:\n
                - 'invalid' if the move is invalid\n
                - 'turn-ending' if the move is turn-ending\n
                - 'non-turn-ending' if the move is a capture without making piece a king
        '''
        # all legal moves are made to an empty square, so it swaps the square with the piece and the empty square
        def swap_pieces(piece1, piece2):
            self.board[piece1.row][piece1.col], self.board[piece2.row][piece2.col] = self.board[piece2.row][piece2.col], self.board[piece1.row][piece1.col]
            piece1.row, piece2.row = piece2.row, piece1.row
            piece1.col, piece2.col = piece2.col, piece1.col
            piece1.calc_pos()
            piece2.calc_pos()
        
        if piece.row == row and piece.col == col:
            return 'invalid'

        # searches for the requested move in the list of legal moves of the given piece
        legal_moves = self.generate_legal_moves(piece)
        found = False
        capture = False
        for move in legal_moves:
            if move[0] == (row, col):
                found = True
                if move[1] != 'notake':
                    self.remove_piece(move[1])
                    capture = True
                break
        if not found:
            return 'invalid'
        
        swap_pieces(piece, self.board[row][col])
        write_output('\nMove number {} - {} played.\n'.format(self.move_no, 'black' if self.move_no % 2 == 0 else 'white'))
        write_output(str(self))
        if piece.king is False and (row == 0 or row == ROWS - 1):
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            elif piece.color == BLACK:
                self.black_kings += 1
            # making a king piece is a turn-ending move
            write_output('End of move number {}.'.format(self.move_no))
            self.move_no += 1
            return 'turn-ending'
        
        if not capture:
            # a non-capture move is a turn-ending move
            write_output('End of move number {}.'.format(self.move_no))
            self.move_no += 1
            return 'turn-ending'
        else:
            # checks if piece has any further capture moves
            legal_moves = self.generate_legal_moves(piece)
            for move in legal_moves:
                if move[1] != 'notake':
                    # if capture move is found, then current move is non-turn-ending
                    return 'non-turn-ending'
            # if no capture move is found, then current move is turn-ending
            write_output('End of move number {}.'.format(self.move_no))
            self.move_no += 1
            return 'turn-ending'
    
    def __str__(self):
        board = []
        board.append('\n   ')
        for i in range(COLS):
            board.append('{} '.format(i))
        board.append('\n\n')
        for i in range(ROWS):
            board.append('{}  '.format(i))
            for piece in self.board[i]:
                board.append('{} '.format(str(piece)))
            board.append('\n')
        board.append('\n')
        return ''.join(board)


class Piece:
    PADDING = 16
    OUTLINE = 4

    def __init__(self, row, col, color=None):
        '''
            Object used for storing and drawing a checkers piece.\n
            Can be used to create an empty square by using the color default parameter.\n
            Is used inside the Board class to store and draw the board state.
        '''
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.directions = []
        if self.color == WHITE:
            self.directions.append(-1)
        elif self.color == BLACK:
            self.directions.append(1)
        # center coordinates of the square are needed for drawing the visuals of the piece
        self.center_x = 0
        self.center_y = 0
        self.calc_pos()
    
    def get_deepcopy(self):
        new_piece = Piece(self.row, self.col, self.color)
        if self.king:
            new_piece.make_king()
        return new_piece
    
    def calc_pos(self):
        self.center_x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.center_y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_king(self):
        self.king = True
        self.directions = [-1, 1]

    def is_empty(self):
        return self.color is None
    
    def remove(self):
        self.color = None
        self.king = False
        self.directions = []
    
    def draw(self, window, selected=False):
        if self.color == None:
            # draws the indicator for a legal move
            if selected:
                pygame.draw.circle(window, GREEN, (self.center_x, self.center_y), SQUARE_SIZE // 2 - self.PADDING - 25)
            return
        radius = SQUARE_SIZE // 2 - self.PADDING
        if selected:
            pygame.draw.rect(window, GREEN, (self.col * SQUARE_SIZE, self.row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), border_radius=3)
        pygame.draw.circle(window, BORDER_BLACK if self.color == BLACK else BORDER_WHITE, (self.center_x, self.center_y), radius + self.OUTLINE)
        pygame.draw.circle(window, self.color, (self.center_x, self.center_y), radius)
        if self.king:
            CROWN = CROWN_WHITE if self.color == WHITE else CROWN_BLACK
            window.blit(CROWN, (self.center_x - CROWN.get_width()//2, self.center_y - CROWN.get_height()//2))
            
    def __str__(self):
        if self.color == BLACK:
            if self.king:
                return 'B'
            return 'b'
        elif self.color == WHITE:
            if self.king:
                return 'W'
            return 'w'
        elif self.color is None:
            return '#'


def timing(f):
    '''
        Decorator which prints the execution time of a function using the time package.\n
        The wraps decorator ensures that the decorated function does not take the definition of the wrap(*args, **kwargs) function.\n
        https://stackoverflow.com/questions/308999/what-does-functools-wraps-do
    '''
    @wraps(f)
    def wrap(*args, **kwargs):
        time_start = time()
        result = f(*args, **kwargs)
        time_end = time()
        write_output('\nComputer using algorithm {} took {} seconds.'.format(f.__name__, time_end - time_start))
        return result
    return wrap

@timing
def stupid_algorithm(board, pieces):
    '''
        Returns a random move from all available moves. If capture moves are available, it removes any non-capture moves.
    '''
    available_pieces = [board.get_piece(i, j) for i in range(ROWS) for j in range(COLS) if board.get_piece(i, j).color == pieces]
    all_piece_moves = [board.generate_legal_moves(piece) for piece in available_pieces]
    capture_moves = [piece_moves for piece_moves in all_piece_moves for move in piece_moves if move[1] != 'notake']
    if len(capture_moves) > 0:
        new_available_pieces = []
        for i in range(len(available_pieces)):
            if all_piece_moves[i] in capture_moves:
                new_available_pieces.append(available_pieces[i])
        available_pieces = new_available_pieces
        all_piece_moves = capture_moves
    start_end_pairs = list(zip(available_pieces, all_piece_moves))
    start_end_pairs = list(filter(lambda pair : True if len(pair[1]) > 0 else False, start_end_pairs))
    start_end_pairs = list(map(lambda pair : (pair[0], choice(pair[1])[0]), start_end_pairs))
    return choice(start_end_pairs)

@timing
def min_max(board, pieces):
    raise Exception('Function min_max not yet implemented.')

@timing
def alpha_beta(board, pieces):
    raise Exception('Function alpha_beta not yet implemented.')

MOVE_FUNCTIONS = [(stupid_algorithm, 'Bogo-move'), (min_max, 'Min-max'), (alpha_beta, 'Alpha-beta')]

class Player:
    def __init__(self, pieces):
        self.pieces = pieces

    def move(self, board):
        mouse_pos = pygame.mouse.get_pos()
        row, col = mouse_pos[1] // 100, mouse_pos[0] // 100
        if board.selected_piece is None:
            piece = board.get_piece(row, col)
            if not piece.is_empty() and piece.color == self.pieces:
                board.selected_piece = piece
        else:
            # if chosen move is a consecutive capture move, get user input for next capture until it becomes a single capture
            while board.move(board.selected_piece, row, col) == 'non-turn-ending':
                write_output('Consecutive capture move.')
                board.draw()
                pygame.display.update()
                run = True
                while run:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            run = False
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = pygame.mouse.get_pos()
                            row, col = mouse_pos[1] // 100, mouse_pos[0] // 100
                            run = False
            board.selected_piece = None

class Computer:
    def __init__(self, pieces, algorithm=stupid_algorithm):
        self.pieces = pieces
        self.algorithm = algorithm
    
    def move(self, board):
        chosen_move = self.algorithm(board, self.pieces)
        if (not isinstance(chosen_move, tuple) or len(chosen_move) != 2 or
            not isinstance(chosen_move[0], Piece) or not isinstance(chosen_move[1], tuple) or len(chosen_move[1]) != 2):
            raise Exception('Move choice algorithm needs to return tuple = (start_piece_addr, tuple = (move_square_x, move_square_y))')
        piece, target = chosen_move[0], chosen_move[1]
        # if the chosen move is a consecutive capture move, generate moves until the start piece matches the original piece and execute when found
        # the while statement guarantees that all generated moves of original piece will be capture moves, until it can't capture anymore
        while board.move(piece, target[0], target[1]) == 'non-turn-ending':
            write_output('Consecutive capture move.')
            board.draw()
            pygame.display.update()
            chosen_move = self.algorithm(board, self.pieces)
            while chosen_move[0] != piece:
                chosen_move = self.algorithm(board, self.pieces)
            target = chosen_move[1]
            # delay between drawing the consecutive moves so they can be seen by the user
            pygame.time.wait(750)

class Text:
    def __init__(self, left, top, value, font, color):
        '''
            Object used for storing and drawing plain text.
        '''
        self.left = left
        self.top = top
        self.value = value
        self.font = font
        self.color = color
        self.width, self.height = pygame.font.Font.size(self.font, self.value)

    def get_value(self):
        return self.value
    
    def center(self, window):
        self.left = window.get_width() // 2 - self.width // 2
    
    def draw(self, window):
        text_surface = self.font.render(self.value, True, self.color)
        window.blit(text_surface, (self.left, self.top))

class Button:
    PADDING = 20
    BORDER = 3

    def __init__(self, left, top, value, font, color, selected=False):
        '''
            Object used for storing and drawing a button.\n
            Makes use of the Text class for storing the text inside the button.\n
            Has fixed-size PADDING and BORDER(can be modified inside class definition).\n
        '''
        self.text = Text(left, top, value, font, color)
        self.selected = selected

    def get_value(self):
        return self.text.value
    
    def draw(self, window):
        pygame.draw.rect(
            window,
            BORDER_BLACK,
            (self.text.left - self.PADDING//2, self.text.top - self.PADDING//2, self.text.width + self.PADDING + self.BORDER, self.text.height + self.PADDING + self.BORDER)
        )
        pygame.draw.rect(
            window,
            BLACK if not self.selected else GREEN,
            (self.text.left - self.PADDING//2, self.text.top - self.PADDING//2, self.text.width + self.PADDING, self.text.height + self.PADDING)
        )
        self.text.draw(window)
    
    def clicked_on(self, x, y):
        '''
            Takes the (x, y) coordinates of a mouse click.\n
            Returns True if (x, y) are inside the button, False otherwise.
        '''
        return (x >= self.text.left - self.PADDING - self.BORDER and x <= self.text.left + self.text.width + self.PADDING + self.BORDER and
                y >= self.text.top - self.PADDING - self.BORDER and y <= self.text.top + self.text.height + self.PADDING + self.BORDER)


class MainMenu:
    def __init__(self, window):
        '''
            Object used for storing display objects and drawing them as menu.\n
            If you want to modify the menu layout, go to self.create_menu().
        '''
        self.window = window
        # self.menu = 
        # [
        #          [Text],              --> Title - Checkers
        #   [Text, Button, Button],     --> Player choice for Black pieces
        #   [Text, Button, Button],     --> Player choice for White pieces
        #   [Button, Button, Button],   --> Algorithm choice
        #           [Button]            --> Start button
        # ]
        self.menu = []
        self.create_menu()
    
    def create_menu(self):
        '''
            Creates the objects which will be displayed on the screen.\n
            If you want to modify the menu layout then you need to modify this function.
        '''
        # row 0
        title = Text(0, 50, 'Checkers', TITLE_FONT, WHITE)
        title.center(self.window)
        self.menu.append([title])

        # rows 1 and 2
        for mul1, label_txt in enumerate(['Black', 'White']):
            self.menu.append([])
            label = Text(0, title.top * 2 + 100 * (mul1 + 1), label_txt, NORMAL_FONT, WHITE)
            label.center(self.window)
            label.left -= WIDTH // 4 + label.width // 2
            self.menu[-1].append(label)
            for mul2, user in enumerate(['Human', 'Computer']):
                self.menu[-1].append(Button(label.left + (WIDTH//4)*(mul2 + 1), label.top, user, NORMAL_FONT, WHITE, True if (mul1 + mul2) % 2 == 0 else False))

        # row 3
        self.menu.append([])
        for idx, button_txt in enumerate(['Min-max', 'Alpha-beta', 'Bogo-move']):
            self.menu[-1].append(Button(0, self.menu[-2][0].top + 150, button_txt, NORMAL_FONT, WHITE, True if idx == 2 else False))
            self.menu[-1][-1].text.center(self.window)
        self.menu[-1][0].text.left -= WIDTH // 4 + self.menu[-1][0].text.width // 2
        self.menu[-1][2].text.left += WIDTH // 4 + self.menu[-1][2].text.width // 2

        # row 4
        self.menu.append([Button(0, HEIGHT - 200, 'START', TITLE_FONT, WHITE)])
        self.menu[-1][-1].text.center(self.window)

    def draw(self):
        self.window.fill(BGBLACK)
        for row in self.menu:
            for object in row:
                object.draw(self.window)
    
    def get_button(self, x, y):
        for row in self.menu:
            for object in row:
                if (isinstance(object, Button) and object.clicked_on(x, y)):
                    return object
        return None
    
    def handle_click(self, x, y):
        '''
            Gets the button at coordinates (x, y) and selects it if possible.\n
            Return values:\n
                - None if there isn't any button at coordinates (x, y)\n
                - 'choice' if the button clicked wasn't the START button\n
                - 'start' if the button clicked was the START button\n
            Also displays the appropiate error messages and does unselections when needed.
        '''
        chosen_button = self.get_button(x, y)
        
        # didn't click on a button
        if chosen_button is None:
            return None

        # clicked on player choices
        for i in [1, 2]:
            for object in self.menu[i]:
                if (isinstance(object, Button) and
                      chosen_button in self.menu[i] and
                      object != chosen_button):
                    object.selected = False
                    chosen_button.selected = True
                    # reset algorithm choices
                    for button in self.menu[3]:
                        button.selected = False
                    return 'choice'

        # clicked on algorithm choices
        # calculates how many algorithms are currently selected and makes sure that the user can't select more than available
        selected_algorithm_no = sum([1 for button in self.menu[3] if button.selected == True])
        algorithm_choice_no = sum([1 for i in [1, 2] for object in self.menu[i] if object.get_value() == 'Computer' and object.selected])
        # if user clicks on an unselected algorithm while the number of selected algorithms is maximum displays an error message
        if selected_algorithm_no == algorithm_choice_no and chosen_button in self.menu[3] and chosen_button.selected == False:
            text = 'You must unselect one algorithm in order to add another.' if algorithm_choice_no != 0 else 'No Computers are selected'
            help_message = Text(0, chosen_button.text.top + chosen_button.text.height + 50, text, ERROR_FONT, RED)
            help_message.center(self.window)
            help_message.draw(self.window)
            pygame.display.update()
            pygame.time.wait(2000)
        for button in self.menu[3]:
            if button == chosen_button:
                if selected_algorithm_no < algorithm_choice_no:
                    button.selected = False if button.selected == True else True
                elif selected_algorithm_no == algorithm_choice_no:
                    button.selected = False
                return 'choice'
        
        # clicked on start
        # checks if the correct number of algorithms are selected and returns the string 'start' which will be used in the menu loop to start the game
        if chosen_button == self.menu[4][0]:
            # if the correct number of algorithms is not selected displays an error message
            # 1 selected algorithm for 2 computers is a vallid combination
            if selected_algorithm_no != algorithm_choice_no and selected_algorithm_no != 1 and algorithm_choice_no != 2:
                error_message = Text(0, chosen_button.text.top - chosen_button.PADDING - 50, 'Number of algorithms chosen must be equal to number of Computers chosen.', ERROR_FONT, RED)
                error_message.center(self.window)
                error_message.draw(self.window)
                pygame.display.update()
                pygame.time.wait(3000)
            elif selected_algorithm_no == algorithm_choice_no or (selected_algorithm_no == 1 and algorithm_choice_no == 2):
                return 'start'
        
        return None
    
    def get_selected_data(self, algorithms):
        '''
            algorithms = list of tuples (algorithm_function : function, algorithm_name : str)\n
            Returns [Object, Object] where Object can be a Player or a Computer with a selected algorithm.\n
            Gets all selected buttons in self.menu list of the class and constructs the needed list.
        '''
        selected_buttons = [(button, i) for i in range(len(self.menu)) for button in self.menu[i] if isinstance(button, Button) and button.selected]
        selected_algorithms = [pair[0].get_value() for pair in selected_buttons if pair[1] == 3]
        # for two computers with the same algorithm
        if len(selected_algorithms) == 1:
            selected_algorithms.append(selected_algorithms[-1])
        # # # # # # # # # # # # # # # # # # # # # #
        for i in range(len(selected_algorithms)):
            for pair in algorithms:
                if selected_algorithms[i] == pair[1]:
                    selected_algorithms[i] = pair[0]
        data = []
        for i, color in enumerate([BLACK, WHITE]):
            if selected_buttons[i][0].get_value() == 'Human':
                data.append(Player(color))
            elif selected_buttons[i][0].get_value() == 'Computer':
                data.append(Computer(color, selected_algorithms.pop()))
        return data


def game_loop(players):
    '''
        players = list of the 2 players in all 4 configurations (HH, HC, CH, CC)\n
        Runs the game loop and returns the winning players' color RGB tuple or False if the game was quit before anyone won.
    '''
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    run = True
    board = BoardGame(window)
    game_over = False
    # if user clicked the close window button on main menu, skip directly to end screen
    if players is None:
        return False
    # write the player for both colors, for logging purposes
    write_output('Black is played by a {}. White is played by a {}.'.format(
        'human' if isinstance(players[0], Player) else 'computer',
        'human' if isinstance(players[1], Player) else 'computer',
        )
    )

    while run:
        CLOCK.tick(FPS)
        pygame.display.set_caption('{} to move'.format('Black' if board.move_no % 2 == 0 else 'White'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                players[board.move_no % 2].move(board)
                game_over = board.game_over()
                if game_over:
                    run = False
        board.draw()
        pygame.display.update()
    else:
        write_output('\nThe game ran for {} seconds.'.format(pygame.time.get_ticks() // 1000 - board.start_time))
        pygame.time.wait(2000)

    return game_over

def menu_loop():
    '''
        Takes no arguments.\n
        Returns a list of two objects of class Player or Computer, depending on what the user selected.
    '''
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Brihac Andrei\'s Checkers')
    run = True
    menu = MainMenu(window)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                row, col = mouse_pos[0], mouse_pos[1]
                click = menu.handle_click(row, col)
                if click == 'start':
                    return menu.get_selected_data(MOVE_FUNCTIONS)
        menu.draw()
        pygame.display.update()
    
    return None

def endscreen_loop(winner):
    '''
        winner = False if the game was cancelled before anyone won, otherwise the RGB tuple of the winning color\n
        Returns True if the user clicked the 'PLAY AGAIN' button, False if the user clicked the 'EXIT' button or the close window button.
    '''
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    window.fill(BGBLACK)
    pygame.display.set_caption('End screen')
    run = True
    play_again = False

    # Create and draw endscreen text and buttons.
    endscreen_text = None
    if winner == False:
        endscreen_text = Text(0, HEIGHT//2, 'Game was cancelled before anyone won.', NORMAL_FONT, WHITE)
    else:
        endscreen_text = Text(0, HEIGHT//2, '{} has won the game.'.format('Black' if winner == BLACK else 'White'), TITLE_FONT, WHITE)
    endscreen_text.center(window)
    endscreen_text.top -= endscreen_text.height // 2 + 75

    play_again_button = Button(0, endscreen_text.top + 100, 'PLAY AGAIN', NORMAL_FONT, WHITE)
    play_again_button.text.center(window)

    exit_button = Button(0, play_again_button.text.top + 100, 'EXIT', NORMAL_FONT, WHITE)
    exit_button.text.center(window)

    endscreen_text.draw(window)
    play_again_button.draw(window)
    exit_button.draw(window)
    pygame.display.update()
    # # # # # # # # # # # # # # # # # # # # # # 

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                row, col = mouse_pos[0], mouse_pos[1]
                if play_again_button.clicked_on(row, col):
                    run = False
                    play_again = True
                if exit_button.clicked_on(row, col):
                    run = False
    
    return play_again

if __name__ == '__main__':
    while endscreen_loop(game_loop(menu_loop())):
        continue
    pygame.quit()
