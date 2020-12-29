

class Player:
    """
    Represents a Player of the game Focus with player name and player piece attributes.
    Two Player objects will be created inside of the FocusGame class representing the two
    players of the game so that Player data members can be accessed and reserve/captured
    amounts can be altered. The FocusGame class will also pass the created Player objects
    when calling methods of Move class objects for use in various validation and piece
    movement functions within the Move class.
    """

    def __init__(self, player_name, player_piece):
        """
        Creates a Player object with a given name and piece and
        initializes reserve and captured counters to 0.
        :param player_name: name of player
        :param player_piece: game piece used by player
        """
        self._player_name = player_name
        self._player_piece = player_piece
        self._reserve = 0
        self._captured = 0

    def get_name(self):
        """
        Returns the Player's name
        :return: player name
        """
        return self._player_name

    def get_piece(self):
        """
        Returns the Player's game piece
        :return: game piece
        """
        return self._player_piece

    def get_reserve(self):
        """
        Returns the number of the Player's reserve pieces
        :return: reserve pieces
        """
        return self._reserve

    def inc_reserve(self):
        """
        Increases the Player's reserve pieces count by 1
        """
        self._reserve += 1

    def dec_reserve(self):
        """
        Decreases the Player's reserve pieces count by 1
        """
        self._reserve -= 1

    def get_captured(self):
        """
        Returns the number of the Player's captured pieces
        :return: captured pieces
        """
        return self._captured

    def inc_captured(self):
        """
        Increases the Player's captured pieces count by 1
        """
        self._captured += 1


class Move:
    """
    Represents a move in the game Focus with player name, and piece or stack origin,
    piece or stack destination, number of pieces being moved, and board attributes.
    A move object is created each time a player calls the move_piece function which
    resides in the FocusGame class. This class performs move validation and piece/stack
    movement operations through the use of its various functions, and receives previously
    created Player objects from FocusGame in order to access these objects' methods.
    """

    def __init__(self, player_name, origin, destination, num_pieces, board):
        """
        Creates a Move object with a given player name, origin, destination, number of
        pieces moved, and board. Also initializes origin and destination rows, columns
        and the value inside of the provided origin and destination.
        :param player_name: name of player
        :param origin: piece/stack origin coordinates on board
        :param destination: piece/stack destination coordinates on board
        :param num_pieces: number of pieces that are being moved from origin to destination
        :param board: game board
        """
        self._player_name = player_name
        self._origin = origin
        self._destination = destination
        self._num_pieces = num_pieces
        self._board = board
        self._destination_row = destination[0]
        self._destination_column = destination[1]
        self._destination_val = board[self._destination_row][self._destination_column]
        if origin != ():  # () is used as special reserved move origin value
            self._origin_row = origin[0]
            self._origin_column = origin[1]
            self._origin_val = board[self._origin_row][self._origin_column]
            self._top_piece = self._origin_val[-1]

    def validate_move(self, current_turn, player_a, player_b):
        """
        Called by move_piece function inside FocusGame class, validates various scenarios
        through the use of calls to specific validate functions and directly validates that
        the piece on the top of the stack or piece itself if single piece belongs to the
        player who is attempting the move.
        :param current_turn: player name whose turn it currently is
        :param player_a: first player object
        :param player_b: second player object
        :return: False or None
        """
        if self.validate_num_pieces() is not None:
            return self.validate_num_pieces()

        # checks if the piece on the top of the stack belongs to the appropriate player
        if current_turn == player_a.get_name():
            if self._top_piece != player_a.get_piece():
                return False
        else:
            if self._top_piece != player_b.get_piece():
                return False

        if self.validate_direction() is not None:
            return self.validate_direction()

        if self.validate_move_length() is not None:
            return self.validate_move_length()

    def validate_num_pieces(self):
        """
        Called by validate_move, checks that the provided number of pieces is in
        range and that the player is not moving more pieces than the number in
        origin
        :return: False or None
        """
        # validates number of pieces range
        if self._num_pieces < 1 or self._num_pieces > 5:
            return False

        # validates that player is not moving more pieces than is possible
        if self._num_pieces > len(self._origin_val):
            return False

    def validate_direction(self):
        """
        Called by validate_move, checks for illegal diagonal move
        :return: False or None
        """
        if self._origin[0] != self._destination[0] and self._origin[1] != self._destination[1]:
            return False

    def validate_move_length(self):
        """
        Called by validate_move, checks for valid move length which must
        be equal to num_pieces for it to be a valid move
        :return: False or None
        """
        if self._origin_row == self._destination_row:
            if abs(self._origin_column - self._destination_column) != self._num_pieces:
                return False
        else:
            if abs(self._origin_row - self._destination_row) != self._num_pieces:
                return False

    def move_stack(self, player_a, player_b):
        """
        Called by move_piece in FocusGame class, changes origin and destination values
        based on type of move (single piece/full stack, partial stack, reserve)
        :param player_a: first player object
        :param player_b: second player object
        :return: None
        """
        if self._origin != ():  # () is used as special reserved move origin value
            # single piece or full stack move
            if len(self._origin_val) == self._num_pieces:  # checks if full stack will be moved
                for piece in self._origin_val:
                    self._destination_val.append(piece)
                self._origin_val.clear()

            # partial stack move
            else:
                leave_behind = len(self._origin_val) - self._num_pieces
                for piece in self._origin_val[leave_behind:]:
                    self._destination_val.append(piece)
                del self._origin_val[leave_behind:]

        else:
            # reserve move
            if player_a.get_name() == self._player_name:
                self._destination_val.append(player_a.get_piece())
            else:
                self._destination_val.append(player_b.get_piece())

    def adjust_stack(self, player_a, player_b):
        """
        Called by move_piece in FocusGame class, handles case where destination
        stack has more than 5 pieces after move, removes the bottom pieces and
        adds to player's reserved or captured count depending on game piece
        :param player_a: first player object
        :param player_b: second player object
        :return: None
        """

        if len(self._destination_val) > 5:
            over_5_count = len(self._destination_val) - 5  # Subtracts 5 from total pieces in destination stack
            for piece in self._destination_val[:over_5_count]:  # for each additional piece over 5 in destination
                # increases appropriate player's reserve or captured count accordingly
                if player_a.get_name() == self._player_name:
                    if player_a.get_piece() == piece:
                        player_a.inc_reserve()
                    else:
                        player_a.inc_captured()
                else:
                    if player_a.get_piece() == piece:
                        player_b.inc_captured()
                    else:
                        player_b.inc_reserve()
                self._destination_val.remove(piece)

    def check_win(self, player_a, player_b):
        """
        Called by move_piece in FocusGame class, checks for win condition
        (a player's captured piece count is greater than 5)
        :param player_a: first player object
        :param player_b: second player object
        :return: None
        """
        if player_a.get_captured() > 5:
            return player_a.get_name() + " wins!"
        elif player_b.get_captured() > 5:
            return player_b.get_name() + " wins!"


class FocusGame:
    """
    Represents the game Focus/Domination with two players. Creates two Player objects
    and a move object each time the move_piece function is called, which uses various
    methods in the Move class to validate and perform normal game moves as well as
    reserve moves. Passes Player objects to certain Move object methods and some methods
    retrieve Player object data using methods defined in the Player class. Also provides
    some additional validation without the use of the Move class and stores/changes the
    player turn accordingly.
    """

    def __init__(self, player_1, player_2):
        """
        Creates a FocusGame object with two given players. Creates two Player class objects
        based on the provided input, initializes the turn value to a blank string, and creates
        the game board which consists of lists of lists and pieces that are retrieved by calling
        the get_piece method of the Player objects.

        :param player_1: first player
        :param player_2: second player
        """

        self._player_a = Player(player_1[0], player_1[1])
        self._player_b = Player(player_2[0], player_2[1])

        self._turn = ""  # contains name of player whose turn it is

        self._board = \
            [[[self._player_a.get_piece()], [self._player_a.get_piece()], [self._player_b.get_piece()],
              [self._player_b.get_piece()], [self._player_a.get_piece()], [self._player_a.get_piece()]],
             [[self._player_b.get_piece()], [self._player_b.get_piece()], [self._player_a.get_piece()],
              [self._player_a.get_piece()], [self._player_b.get_piece()], [self._player_b.get_piece()]],
             [[self._player_a.get_piece()], [self._player_a.get_piece()], [self._player_b.get_piece()],
              [self._player_b.get_piece()], [self._player_a.get_piece()], [self._player_a.get_piece()]],
             [[self._player_b.get_piece()], [self._player_b.get_piece()], [self._player_a.get_piece()],
              [self._player_a.get_piece()], [self._player_b.get_piece()], [self._player_b.get_piece()]],
             [[self._player_a.get_piece()], [self._player_a.get_piece()], [self._player_b.get_piece()],
              [self._player_b.get_piece()], [self._player_a.get_piece()], [self._player_a.get_piece()]],
             [[self._player_b.get_piece()], [self._player_b.get_piece()], [self._player_a.get_piece()],
              [self._player_a.get_piece()], [self._player_b.get_piece()], [self._player_b.get_piece()]]]

    def move_piece(self, player_name, origin, destination, num_pieces):
        """
        Creates Move class object using provided input parameters and performs various function
        calls on that object in order to validate and perform movement of game pieces. Also makes
        calls to methods defined in this class for additional validation, to check for win conditions,
        and to change the value of current_turn to the appropriate player name.
        :param player_name: name of player
        :param origin: piece/stack origin coordinates on board
        :param destination: piece/stack destination coordinates on board
        :param num_pieces: number of pieces that are being moved from origin to destination
        :return: "successfully moved" if move is valid, otherwise one of various invalid move messages
        """

        if self.validate_range(origin, destination) is not None:
            return self.validate_range(origin, destination)

        make_move = Move(player_name, origin, destination, num_pieces, self._board)

        if self.validate_player_turn(player_name) is not None:
            return self.validate_player_turn(player_name)

        if make_move.validate_move(self._turn, self._player_a, self._player_b) is not None:
            return make_move.validate_move(self._turn, self._player_a, self._player_b)

        make_move.move_stack(self._player_a, self._player_b)

        make_move.adjust_stack(self._player_a, self._player_b)

        if make_move.check_win(self._player_a, self._player_b) is not None:
            return make_move.check_win(self._player_a, self._player_b)

        return self.change_player_turn()

    def validate_range(self, origin, destination):
        """
        Checks for invalid location range for source or destination
        :param origin: piece/stack origin coordinates on board
        :param destination: piece/stack destination coordinates on board
        :return: False or None
        """
        if origin != ():  # () is used as special reserved move origin value
            if (origin[0] or origin[1] or destination[0] or destination[1]) < 0:
                return False
            elif (origin[0] or origin[1] or destination[0] or destination[1]) > 5:
                return False
            elif not self._board[origin[0]][origin[1]]:  # checks for empty origin space
                return False

        else:
            if (destination[0] or destination[1]) < 0:
                return False
            elif (destination[0] or destination[1]) > 5:
                return False

    def validate_player_turn(self, player_name):
        """
        Checks for incorrect player trying to make a move out of turn
        :param player_name: name of player
        :return: False or None
        """
        if player_name != self._turn:
            if self._turn == "":
                self._turn = player_name
            else:
                return False

    def change_player_turn(self):
        """
        Changes which player's turn it is after move is made by changing value
        in self._turn to correct player name
        :return: "successfully moved"
        """
        if self._turn == self._player_a.get_name():
            self._turn = self._player_b.get_name()
        else:
            self._turn = self._player_a.get_name()
        return "successfully moved"

    def show_pieces(self, location):
        """
        Returns a list of the game pieces at a specific provided location
        :param location: coordinates showing a position on board
        :return: list showing the pieces at that location
        """
        coord_1 = location[0]
        coord_2 = location[1]
        return self._board[coord_1][coord_2]

    def show_reserve(self, player_name):
        """
        Returns the provided player's reserve value or
        "invalid player name" if invalid name is provided
        :param player_name: name of player
        :return: Reserve value of player or False
        """
        if player_name == self._player_a.get_name():
            return self._player_a.get_reserve()
        elif player_name == self._player_b.get_name():
            return self._player_b.get_reserve()
        else:
            return False

    def show_captured(self, player_name):
        """
        Returns the provided player's captured value or
        "invalid player name" if invalid name is provided
        :param player_name: name of player
        :return: Captured value of player or False
        """
        if player_name == self._player_a.get_name():
            return self._player_a.get_captured()
        elif player_name == self._player_b.get_name():
            return self._player_b.get_captured()
        else:
            return False

    def reserved_move(self, player_name, destination):
        """
        Creates a Move class object and calls Move validation and piece movement
        methods on the object, but only those that are applicable to a reserved
        move. Also calls some validation methods from this FocusGame class. The
        empty tuple () is used as origin coordinates and the value 1 as num_pieces.
        Theorigin value of () is handled through the use of conditional statements
        in some of the called methods that prevent it from triggering any invalid
        move messages.
        :param player_name: name of player
        :param destination: reserve destination coordinates on board
        :return: False or None
        """

        if self.show_reserve(player_name) == 0:
            return False
        else:
            if self.validate_range((), destination) is not None:
                return self.validate_range((), destination)

            res_move = Move(player_name, (), destination, 1, self._board)

            if self.validate_player_turn(player_name) is not None:
                return self.validate_player_turn(player_name)

            res_move.move_stack(self._player_a, self._player_b)

            res_move.adjust_stack(self._player_a, self._player_b)

            if res_move.check_win(self._player_a, self._player_b) is not None:
                return res_move.check_win(self._player_a, self._player_b)

            if self._player_a.get_name() == player_name:
                self._player_a.dec_reserve()
            else:
                self._player_b.dec_reserve()

        return self.change_player_turn()

    def print_board(self):
        """
        Prints FocusGame board
        :return: None
        """
        for i in self._board:
            print(i)

game = FocusGame(('PlayerA', 'R'), ('PlayerB','G'))
game.move_piece('PlayerA',(0,0), (0,1), 1)  #Returns message "successfully moved"
game.show_pieces((0,1)) #Returns ['R','R']
game.show_captured('PlayerA') # Returns 0
game.reserved_move('PlayerA', (0,0)) # Returns message "No pieces in reserve"
game.show_reserve('PlayerA') # Returns 0