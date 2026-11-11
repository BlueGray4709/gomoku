def is_empty(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] != " ":
                return False
    return True
    
def is_bounded(board, y_end, x_end, length, d_y, d_x):
    board_size = len(board)

    x_before = x_end - length * d_x
    y_before = y_end - length * d_y

    x_after = x_end + d_x
    y_after = y_end + d_y

    before_free = False
    after_free = False

    if 0 <= x_before < board_size and 0 <= y_before < board_size: 
        if board[y_before][x_before] == " ":
            before_free = True

    if 0 <= x_after < board_size and 0 <= y_after < board_size:
        if board[y_after][x_after] == " ":
            after_free = True

    if before_free and after_free:
        return "OPEN"
    elif before_free or after_free:
        return "SEMIOPEN"
    else:
        return "CLOSED"
    
def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    board_size = len(board)
    open_seq_count = 0
    semi_open_seq_count = 0
    run_length = 0 

    y, x = y_start, x_start

    while 0 <= y < board_size and 0 <= x < board_size: #within board
        if board[y][x] == col: #if the square is the same color as col 
            run_length += 1 

            next_y = y + d_y
            next_x = x + d_x

            at_end = not ( #at_end = True means run has not reached edge of board
                0 <= next_y < board_size and
                0 <= next_x < board_size
            )

            if at_end or board[next_y][next_x] != col: #run has ended, now we check
                if run_length == length: #matches length we look for
                    bounded = is_bounded( 
                        board, y, x, length, d_y, d_x
                    )

                    if bounded == "OPEN":
                        open_seq_count += 1
                    elif bounded == "SEMIOPEN":
                        semi_open_seq_count += 1

                run_length = 0 #clear run length for next while loop iteration

        else:
            run_length = 0 

        y += d_y #shift search
        x += d_x #shift search

    return open_seq_count, semi_open_seq_count
    
def detect_rows(board, col, length):
    board_size = len(board) 
    open_seq_count, semi_open_seq_count = 0, 0

    for d_y, d_x in [(0,1), (1,0), (1,1), (1,-1)]: #all possible move directions
        for y in range(board_size):
            for x in range(board_size):
                prev_y = y - d_y #iff at edge, prev_y < 0 
                prev_x = x - d_x #iff at edge, prev_x < 0

                if not(0 <= prev_y < board_size and 0 <= prev_x < board_size): #if spot being checked is along the edge of the board
                    open_count, semi_count = detect_row(board, col, y, x, length, d_y, d_x) #call detect_row

                    open_seq_count += open_count #augment
                    semi_open_seq_count += semi_count #augment
    return open_seq_count, semi_open_seq_count
    
def search_max(board):
    best_score = float("-inf") #smallest possible number 
    move_y, move_x = -1, -1  #placeholder values for move_y and move_x

    for y in range(len(board)): 
        for x in range(len(board)): 
            if board[y][x] == " ":
                board[y][x] = "b" #modifies board  
                current_score = score(board) #checks hypothetical score
                board[y][x] = " " #modifies board back

                if current_score > best_score: #compares hypothetical score with best score
                    best_score = current_score 
                    move_y, move_x = y, x
    
    return move_y, move_x
    
def score(board):
    MAX_SCORE = 100000
    
    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}
    
    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)
        
    
    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE
    
    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE
        
    return (-10000 * (open_w[4] + semi_open_w[4])+ 
            500  * open_b[4]                     + 
            50   * semi_open_b[4]                + 
            -100  * open_w[3]                    + 
            -30   * semi_open_w[3]               + 
            50   * open_b[3]                     + 
            10   * semi_open_b[3]                +  
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])
    
def is_win(board):
    board_size = len(board)

    for y in range(board_size):
        for x in range(board_size):
            col = board[y][x]

            if col == " ": #if space is empty
                continue #no point searching, find another (y, x)

            for d_y, d_x in [(0,1), (1,0), (1,1), (1,-1)]:
                prev_y = y - d_y
                prev_x = x - d_x

                #skip stones that are not the start of a run
                if 0 <= prev_y < board_size and 0 <= prev_x < board_size and board[prev_y][prev_x] == col:
                    continue 

                run_length = 0
                next_y, next_x = y, x

                while 0 <= next_y < board_size and 0 <= next_x < board_size and board[next_y][next_x] == col: #while stone is within dimension of board, and all stones of 1 color are consecutive
                    run_length += 1 
                    next_y += d_y #shift search
                    next_x += d_x #shift search

                if run_length == 5:
                    if col == "b": #stone in sequence of 5 is black
                        return "Black won"
                    return "White won"

    for row in board: 
        if " " in row: #if any spaces on board are empty
            return "Continue playing"

    return "Draw" #if all of board is full

def print_board(board):
    
    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"
    
    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1]) 
    
        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"
    
    print(s)

def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board

def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))
    
def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])
    
    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)
            
        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res
        
        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res

def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col        
        y += d_y
        x += d_x

def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")

def test_is_bounded():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    
    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")

def test_detect_row():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0,x,length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")

def test_detect_rows():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col,length) == (1,0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")

def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()

def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)
    
    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    
    y = 3; x = 5; d_x = -1; d_y = 1; length = 2
    
    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)
    
    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #     
    
    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)
    
    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #        
    #        
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0

if __name__ == '__main__':
    easy_testset_for_main_functions()
    play_gomoku(8)
