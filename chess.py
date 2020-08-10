# your code goes here
import string
import random
import os
import sys
import time
# from IPython.display import clear_output
import numpy as np
from random import randint
from copy import copy

chess_board = []
start = True

random_test = []


# you can add/change the input parameters for each function
# you can change the function names and also add more functions if needed


def ChessBoardSetup():
    global chess_board, start
    start = True
    # resets to blank
    chess_board = []
    # initialize and return a chess board - create a 2D 8x8 array that has the value for each cell
    # USE the following characters for the chess pieces - lower-case for BLACK and upper-case for WHITE
    # . for empty board cell
    # p/P for pawn
    # r/R for rook
    # t/T for knight
    # b/B for bishop
    # q/Q for queen
    # k/K for king
    # chess_board=[]
    chess_board += [['r', 't', 'b', 'q', 'k', 'b', 't', 'r']]
    chess_board += [['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p']]
    chess_board += [['.', '.', '.', '.', '.', '.', '.', '.']]
    chess_board += [['.', '.', '.', '.', '.', '.', '.', '.']]
    chess_board += [['.', '.', '.', '.', '.', '.', '.', '.']]
    chess_board += [['.', '.', '.', '.', '.', '.', '.', '.']]
    chess_board += [['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P']]
    chess_board += [['R', 'T', 'B', 'Q', 'K', 'B', 'T', 'R']]


def DrawBoard():
    global chess_board
    # write code to print the board - following is one print example
    # r t b q k b t r
    # p p p p p p p p
    # . . . . . . . .
    # . . . . . . . .
    # . . . . . . . .
    # . . . . . . . .
    # P P P P P P P P
    # R T B Q K B T R
    for p in range(8):
        row = chess_board[p]
        temp_str = ''
        for a in range(8):
            temp_str = temp_str + str(row[a]) + " "
        print(temp_str)
    print("")


def draw_hypo_board(board):
    for p in range(8):
        row = board[p]
        temp_str = ''
        for a in range(8):
            temp_str = temp_str + str(row[a]) + " "
        print(temp_str)
    print("")


# x y format origina is top left
# input is list containing xy coordinate
def MovePiece(origin, destination, ref_board):
    new_board = []
    # create new board completly seperate
    # for c in range(len(ref_board)):
    #   new_board += [ref_board[c]]
    y_origin = origin[1]
    x_origin = origin[0]

    y_destination = destination[1]
    x_destination = destination[0]
    # write code to move the one chess piece
    # you do not have to worry about the validity of the move - this will be done before calling this function
    # this function will at least take the move (from-peice and to-piece) as input and return the new board layout
    # get the character from the origian coordinate
    piece = ref_board[y_origin][x_origin]
    # blank out the original position of the piece
    # new_board[origin[1]][origin[0]] = '.'
    # place piece in destination
    # new_board[destination[1]][destination[0]] = piece
    # reconstruct new board from scratch to keep original board intact
    for y in range(8):
        temp = []
        orignal_temp = ref_board[y]
        for x in range(8):
            if x == x_origin and y == y_origin:
                temp += ["."]
            elif x == x_destination and y == y_destination:
                temp += [piece]
            else:
                temp += [orignal_temp[x]]
        new_board += [temp]

    return new_board


def IsMoveLegal():
    # return True if a move (from-piece and to-piece) is legal, else False
    # this is the KEY function which contains the rules for each piece type
    p = 0


# check for move duplicates and remove them
def check_duplicate_moves(move_list):
    m_list = []
    output = []
    for i in range(len(move_list)):
        move_1 = move_list[i]
        for j in range(len(move_list)):
            move_2 = move_list[j]
            # find if vectors are the same
            ans = move_1 - move_2
            ans = np.dot(ans, ans)
            if ans == 0 and i != j:
                move_list[j] = np.array([-1, -1])

    for k in range(len(move_list)):
        move_3 = move_list[k]
        ans = move_3 - np.array([-1, -1])
        ans = np.dot(ans, ans)
        if ans != 0:
            output += [move_3]
    p = 0
    return output


def get_king(player, board):
    # player either 0 or 1
    if player == 0:
        target = 'k'
    elif player == 1:
        target = 'K'
    else:
        print("error in get king function")
        return []
    for x in range(8):
        for y in range(8):
            temp = board[y][x]
            if temp == target:
                return [x, y]
    return []


def occupied(piece, piece_on_move):
    own_piece = (piece.islower() and piece_on_move.islower()) or (piece.isupper() and piece_on_move.isupper())
    opposing_piece = (piece.islower() and piece_on_move.isupper()) or (piece.isupper() and piece_on_move.islower())

    if piece_on_move == '.':
        return 0
    elif opposing_piece:
        return 1
    elif own_piece:
        return 2
    else:
        print("problem with occupid function")
        return 0


# gets the x y coordinate of the piece
# player is player
# 0 or 1
def GetListOfLegalMoves(piece_origin, board):
    global start
    t = start
    # blank spaces has no moves
    piece = board[piece_origin[1]][piece_origin[0]]
    if piece.islower():
        player = 0
    else:
        player = 1
    # coord=np.array(piece_origin)
    if piece == '.':
        return []
    # gets a list of legal moves for a given piece

    # get the type of moves available to each piece
    # [up,down,left,right,topleft,topright, bottomleft,bottomright,knight specific,pawn specific]
    move_dict = {
        "r": [8, 8, 8, 8, 0, 0, 0, 0, 0, 0],
        "t": [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        "b": [0, 0, 0, 0, 8, 8, 8, 8, 0, 0],
        "q": [8, 8, 8, 8, 8, 8, 8, 8, 0, 0],
        "k": [1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
        "p": [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        "R": [8, 8, 8, 8, 0, 0, 0, 0, 0, 0],
        "T": [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        "B": [0, 0, 0, 0, 8, 8, 8, 8, 0, 0],
        "Q": [8, 8, 8, 8, 8, 8, 8, 8, 0, 0],
        "K": [1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
        "P": [0, 0, 0, 0, 0, 0, 0, 0, 0, 1], }
    options = move_dict[piece]
    moves_list = []

    move = np.array(piece_origin)
    test = options[0]
    for m in range(options[0]):
        # up
        move += np.array([0, -1])
        out_bounds = move[0] < 0 or move[0] > 7 or move[1] < 0 or move[1] > 7
        if out_bounds:
            break
        piece_on_move = board[move[1]][move[0]]
        occ = occupied(piece, piece_on_move)
        if occ == 0:
            moves_list += [np.array(move)]
            p = 0
        elif occ == 1:
            moves_list += [np.array(move)]
            break
        elif occ == 2:
            break
        else:
            print("move error from occupied functions")

    move = np.array(piece_origin)
    for m in range(options[1]):
        # down
        move += np.array([0, 1])
        out_bounds = move[0] < 0 or move[0] > 7 or move[1] < 0 or move[1] > 7
        if out_bounds:
            break
        piece_on_move = board[move[1]][move[0]]
        occ = occupied(piece, piece_on_move)
        if occ == 0:
            moves_list += [np.array(move)]
        elif occ == 1:
            moves_list += [np.array(move)]
            break
        elif occ == 2:
            break
        else:
            print("move error from occupied functions")

    move = np.array(piece_origin)
    for m in range(options[2]):
        # left
        move += np.array([-1, 0])
        out_bounds = move[0] < 0 or move[0] > 7 or move[1] < 0 or move[1] > 7
        if out_bounds:
            break
        piece_on_move = board[move[1]][move[0]]
        occ = occupied(piece, piece_on_move)
        if occ == 0:
            moves_list += [np.array(move)]
        elif occ == 1:
            moves_list += [np.array(move)]
            break
        elif occ == 2:
            break
        else:
            print("move error from occupied functions")

    move = np.array(piece_origin)
    for m in range(options[3]):
        # right
        move += np.array([1, 0])
        out_bounds = move[0] < 0 or move[0] > 7 or move[1] < 0 or move[1] > 7
        if out_bounds:
            break
        piece_on_move = board[move[1]][move[0]]
        occ = occupied(piece, piece_on_move)
        if occ == 0:
            moves_list += [np.array(move)]
        elif occ == 1:
            moves_list += [np.array(move)]
            break
        elif occ == 2:
            break
        else:
            print("move error from occupied functions")

    move = np.array(piece_origin)
    for m in range(options[4]):
        # top left
        move += np.array([-1, -1])
        out_bounds = move[0] < 0 or move[0] > 7 or move[1] < 0 or move[1] > 7
        if out_bounds:
            break
        piece_on_move = board[move[1]][move[0]]
        occ = occupied(piece, piece_on_move)
        if occ == 0:
            moves_list += [np.array(move)]
        elif occ == 1:
            moves_list += [np.array(move)]
            break
        elif occ == 2:
            break
        else:
            print("move error from occupied functions")

    move = np.array(piece_origin)
    for m in range(options[5]):
        # top right
        move += np.array([1, -1])
        out_bounds = move[0] < 0 or move[0] > 7 or move[1] < 0 or move[1] > 7
        if out_bounds:
            break
        piece_on_move = board[move[1]][move[0]]
        occ = occupied(piece, piece_on_move)
        if occ == 0:
            moves_list += [np.array(move)]
        elif occ == 1:
            moves_list += [np.array(move)]
            break
        elif occ == 2:
            break
        else:
            print("move error from occupied functions")

    move = np.array(piece_origin)
    for m in range(options[6]):
        # bottom left
        move += np.array([-1, 1])
        out_bounds = move[0] < 0 or move[0] > 7 or move[1] < 0 or move[1] > 7
        if out_bounds:
            break
        piece_on_move = board[move[1]][move[0]]
        occ = occupied(piece, piece_on_move)
        if occ == 0:
            moves_list += [np.array(move)]
        elif occ == 1:
            moves_list += [np.array(move)]
            break
        elif occ == 2:
            break
        else:
            print("move error from occupied functions")
    move = np.array(piece_origin)
    for m in range(options[7]):
        # bottom right
        move += np.array([1, 1])
        out_bounds = move[0] < 0 or move[0] > 7 or move[1] < 0 or move[1] > 7
        if out_bounds:
            break
        piece_on_move = board[move[1]][move[0]]
        occ = occupied(piece, piece_on_move)
        if occ == 0:
            moves_list += [np.array(move)]
        elif occ == 1:
            moves_list += [np.array(move)]
            break
        elif occ == 2:
            break
        else:
            print("move error from occupied functions")

    knight_moves = [[-1, -2], [-1, 2], [1, -2], [1, 2],
                    [-2, -1], [2, -1], [-2, 1], [2, 1]
                    ]
    if options[8] == 1:
        for m in range(8):
            move = np.array(piece_origin)
            move += np.array(knight_moves[m])
            out_bounds = move[0] < 0 or move[0] > 7 or move[1] < 0 or move[1] > 7
            if out_bounds:
                continue
            piece_on_move = board[move[1]][move[0]]
            occ = occupied(piece, piece_on_move)
            if occ == 0:
                moves_list += [np.array(move)]
            elif occ == 1:
                moves_list += [np.array(move)]
                continue
            elif occ == 2:
                continue
            else:
                print("move error from occupied functions")
    # take advantage of certain pawn traits
    if options[9] == 1:
        if player == 0:
            if start:
                move = np.array(piece_origin)
                move += np.array([0, 2])
                out_bounds = move[0] < 0 or move[0] > 7 or move[1] < 0 or move[1] > 7
                if not out_bounds:
                    piece_on_move = board[move[1]][move[0]]
                    occ = occupied(piece, piece_on_move)
                    if occ == 0:
                        moves_list += [np.array(move)]
                    p = 0

            move = np.array(piece_origin)
            opt_1 = move + np.array([-1, 1])
            out_bounds = opt_1[0] < 0 or opt_1[0] > 7 or opt_1[1] < 0 or opt_1[1] > 7
            if not out_bounds:
                piece_on_move_1 = board[opt_1[1]][opt_1[0]]
                occ_1 = occupied(piece, piece_on_move_1)
                if occ_1 == 0 or occ_1 == 1:
                    moves_list += [np.array(opt_1)]
            opt_2 = move + np.array([1, 1])
            out_bounds = opt_2[0] < 0 or opt_2[0] > 7 or opt_2[1] < 0 or opt_2[1] > 7
            if not out_bounds:
                piece_on_move_2 = board[opt_2[1]][opt_2[0]]
                occ_2 = occupied(piece, piece_on_move_2)
                if occ_2 == 0 or occ_2 == 1:
                    moves_list += [np.array(opt_2)]
            opt_3 = move + np.array([0, 1])
            out_bounds = opt_3[0] < 0 or opt_3[0] > 7 or opt_3[1] < 0 or opt_3[1] > 7
            if not out_bounds:
                piece_on_move_3 = board[opt_3[1]][opt_3[0]]
                occ_3 = occupied(piece, piece_on_move_3)
                if occ_3 == 0:
                    moves_list += [np.array(opt_3)]

        elif player == 1:
            if start:
                move = np.array(piece_origin)
                move += np.array([0, -2])
                out_bounds = move[0] < 0 or move[0] > 7 or move[1] < 0 or move[1] > 7
                if not out_bounds:
                    piece_on_move = board[move[1]][move[0]]
                    occ = occupied(piece, piece_on_move)
                    if occ == 0:
                        moves_list += [np.array(move)]
            move = np.array(piece_origin)
            opt_1 = move + np.array([-1, -1])
            out_bounds = opt_1[0] < 0 or opt_1[0] > 7 or opt_1[1] < 0 or opt_1[1] > 7
            if not out_bounds:
                piece_on_move_1 = board[opt_1[1]][opt_1[0]]
                occ_1 = occupied(piece, piece_on_move_1)
                if occ_1 == 0 or occ_1 == 1:
                    moves_list += [np.array(opt_1)]
            opt_2 = move + np.array([1, -1])
            out_bounds = opt_2[0] < 0 or opt_2[0] > 7 or opt_2[1] < 0 or opt_2[1] > 7
            if not out_bounds:
                piece_on_move_2 = board[opt_2[1]][opt_2[0]]
                occ_2 = occupied(piece, piece_on_move_2)
                if occ_2 == 0 or occ_2 == 1:
                    moves_list += [np.array(opt_2)]
            opt_3 = move + np.array([0, -1])
            out_bounds = opt_3[0] < 0 or opt_3[0] > 7 or opt_3[1] < 0 or opt_3[1] > 7
            if not out_bounds:
                piece_on_move_3 = board[opt_3[1]][opt_3[0]]
                occ_3 = occupied(piece, piece_on_move_3)
                if occ_3 == 0:
                    moves_list += [np.array(opt_3)]
    moves_list = check_duplicate_moves(moves_list)
    # moves_list=np.unique(moves_list)
    # handle the situation with the king

    return moves_list


# relies on GetListOfLegalMoves
# king is handled seperatly
# check and check mate is handled within this function
def GetPiecesWithLegalMoves(player, board, hypo=3):
    global random_test
    # gets a list of all pieces for the current player that have legal moves
    # a piece can be denoted just by (row, col)
    # have to take into accoun all the legal moves from each player
    player_0_moves = []
    player_1_moves = []

    # first get the raw move list from both players
    player_0_raw = []
    player_1_raw = []

    # keep track of move origin
    player_0 = []
    player_1 = []

    king_0 = []
    king_1 = []
    for i in range(8):
        for j in range(8):
            origin = np.array([j, i])
            temp = board[i][j]
            # get kings
            if temp == '.':
                continue
            elif temp.islower():
                GetList = GetListOfLegalMoves([j, i], board)
                if len(GetList) > 0:
                    player_0_raw.extend(GetList)
                    for a0 in range(len(GetList)):
                        player_0 += [[[j, i], GetList[a0]]]
                if len(GetList) == 0:
                    p = 0
            elif temp.isupper():
                GetList = GetListOfLegalMoves([j, i], board)
                if len(GetList) > 0:
                    player_1_raw.extend(GetList)
                    for a1 in range(len(GetList)):
                        player_1 += [[[j, i], GetList[a1]]]
                    if len(GetList) == 0:
                        p = 0
            else:
                print("error determining which player character entered is", str(temp))
    if hypo == 0:
        return player_0
    elif hypo == 1:
        return player_1

    legal_moves = []
    # determin which moves would not lead to a check and only keep the moves that dont out the player in check
    # be doing this check mate can be infered by having a list of legal moves be empty
    # if player == 0:
    #    for r in range(len(player_0)):
    #        # create the hypothetical board if takeing move
    #        hypo_move = player_0[r]
    #        hypo_board = MovePiece(np.array(hypo_move[0]), np.array(hypo_move[1]), board)
    #        king_loc = get_king(0, hypo_board)
    #        if len(king_loc) == 0:
    #            print("problem")
    #            exit(0)
    #        ischeck = IsInCheck(0, hypo_board)
    #        if not ischeck:
    #            legal_moves += [hypo_move]
    # elif player == 1:
    #    for r in range(len(player_1)):
    #        # create the hypothetical board if takeing move
    #        hypo_move = player_1[r]
    #        hypo_board = MovePiece(np.array(hypo_move[0]), np.array(hypo_move[1]), board)
    #        king_loc = get_king(1, hypo_board)
    #
    #        if len(king_loc) == 0:
    #            print("problem")
    #            exit(0)
    #        ischeck = IsInCheck(1, hypo_board)
    #        if not ischeck:
    #            legal_moves += [hypo_move]
    # else:
    #    print("error in choosing player with getpiece with legal moves function")

    p_moves = []
    p_boards = []
    p_king_lob = []
    if player == 0:
        for i in range(len(player_0)):
            mover = player_0[i]
            boarder = MovePiece(mover[0], mover[1], board)
            kinger = get_king(0, boarder)
            opposing = []
            for y in range(8):
                for x in range(8):
                    temp = boarder[y][x]
            ran = IsInCheck(0, boarder)
            if not ran:
                legal_moves += [mover]
        return legal_moves
    elif player == 1:
        for i in range(len(player_1)):
            mover = player_1[i]
            boarder = MovePiece(mover[0], mover[1], board)
            kinger = get_king(1, boarder)
            opposing = []
            ran = IsInCheck(1, boarder)
            if not ran:
                legal_moves += [mover]
    else:
        return legal_moves

    return legal_moves


# check is a current coordinate is with range
def check_if_within_range(coord, move_list):
    for i in range(len(move_list)):
        A = np.array(coord)
        B = np.array(move_list[i])
        C = A - B
        D = np.dot(C, C)
        if D == 0:
            return True
    return False


def IsCheckmate(player, board):
    legal = GetPiecesWithLegalMoves(0, board)
    if len(legal) <= 0:
        return True
    return False


def IsInCheck(player, board):
    # returns True if a given player is in Check state
    # One way to check:
    #   find given player's King
    #   check if any enemy player's piece has a legal move to the given player's King
    #   return True if there is any legal move

    opposing_moves = []

    player_0_ = []
    player_1_ = []

    king = get_king(player, board)
    if len(king) == 0:
        print("problem with king")

    for i in range(8):
        for j in range(8):
            origin = np.array([j, i])
            temp = board[i][j]
            # get kings
            if temp == '.':
                continue
            elif temp.islower():
                if temp == 'q':
                    p = 0
                GetList = GetListOfLegalMoves([j, i], board)
                if len(GetList) > 0:
                    player_0_.extend(GetList)
            elif temp.isupper():
                GetList = GetListOfLegalMoves([j, i], board)
                if len(GetList) > 0:
                    player_1_.extend(GetList)
            else:
                print("error")
                continue
    if player == 0:
        check = check_if_within_range(king, player_1_)
    elif player == 1:
        check = check_if_within_range(king, player_0_)
    else:
        print("error")
        return

    check_test_1 = check_if_within_range(king, player_1_)
    check_test_2 = check_if_within_range(king, player_0_)

    return check


def DoesMovePutPlayerInCheck():
    # makes a hypothetical move (from-piece and to-piece)
    # returns True if it puts current player into check
    p = 0


# ChessBoardSetup()


# DrawBoard()


def evl(player, board):
    # this function will calculate the score on the board, if a move is performed
    # give score for each of piece and calculate the score for the chess board
    if player == 0:
        mult = 1
    elif player == 1:
        mult = -1
    else:
        mult = 0
    score = 0
    score_dict = {
        '.': 0,
        "r": 50,
        "t": 30,
        "b": 30,
        "q": 90,
        "k": 900,
        "p": 10,
        "R": -50,
        "T": -30,
        "B": -30,
        "Q": -90,
        "K": -900,
        "P": -10, }
    for i in range(8):
        for j in range(8):
            temp = board[i][j]
            add = score_dict[temp]
            score += (add * mult)
    return score


def GetRandomMove(player, board):
    # pick a random piece and a random legal move for that piece
    moves = GetPiecesWithLegalMoves(player, board)
    if len(moves) <= 0:
        return 0, 0, True

    rand = randint(0, len(moves) - 1)
    move = moves[rand]
    origin = move[0]
    destination = move[1]
    return origin, destination, False


def scoredMove(player, board):
    board = list(chess_board)
    available_moves_max = GetPiecesWithLegalMoves(0, board)
    if len(available_moves_max) <= 0:
        return 0, 0, True

    score = []
    potential = []
    for i in range(len(available_moves_max)):
        move_layer_0 = available_moves_max[i]
        # create hypothetical board
        board_layer_0 = MovePiece(move_layer_0[0], move_layer_0[1], chess_board)
        score += [evl(0, board_layer_0)]
        potential += [move_layer_0]
    highest = np.argmax(score)
    chosen_move = potential[highest]

    return chosen_move[0], chosen_move[1], False


def GetMinMaxMove(player, board):
    # return the best move for the current player using the MinMax strategy
    # to get the allocated 50 points, searching should be 2-ply (one Max and one Min)
    # player 0 will be using minmax move
    alpha = float('-inf')
    beta = float('-inf')

    checkmate = False
    available_moves_max = GetPiecesWithLegalMoves(0, board)
    if len(available_moves_max) == 0:
        return 0, 0, True
    scores_layer_0 = []
    layer_0_scores = []
    layer_1_scores = []

    moves_layer_0 = []
    moves_layer_1 = []

    max_scores = []
    min_scores = []
    for i in range(len(available_moves_max)):
        # create hypothetical board for this move
        move = available_moves_max[i]
        new_board = MovePiece(move[0], move[1], board)
        # score the value of this board
        max_scores += [evl(0, board)]
        # find the available moves from the other player from this hypothetical board
        available_moves_min = GetPiecesWithLegalMoves(1, new_board)
        # if this moves puts it in checkmate
        if len(available_moves_min) == 0:
            min_scores += [9999]
        else:
            min_scores_2 = []
            # find the scores from the minimum layer
            for j in range(len(available_moves_min)):
                move = available_moves_max[i]
                # get hypothetical board
                new_board_2 = MovePiece(move[0], move[1], new_board)
                # get score of the move
                score = evl(0, new_board_2)
                if score <= alpha:
                    #pruning
                    break
                min_scores_2 += [score]
            if score <= alpha:
                continue
            min_score = min_but_random(min_scores_2)
            alpha = max(min_score, alpha)
            min_scores += [min_score]
    best_score_index = arg_max_but_random(min_scores)
    best_move = available_moves_max[best_score_index]

    return best_move[0], best_move[1], False


# pick minimum but choose randomly if there are multiple chooices.
def min_but_random(arr_list):
    minimum = min(arr_list)
    new_list = []
    if len(arr_list) <= 1:
        return minimum
    for i in range(len(arr_list)):
        if minimum == arr_list[i]:
            new_list += [arr_list[i]]
    # pick random from choice
    choose = random.choice(new_list)
    return choose


# pick maximum but choose randomly if there or multiples of the same max
def arg_max_but_random(arr_list):
    maximum = max(arr_list)
    arg_maximum = np.argmax(arr_list)
    new_list = []
    if len(arr_list) <= 1:
        return arg_maximum
    for i in range(len(arr_list)):
        if maximum == arr_list[i]:
            new_list += [i]
    # pick random from choice
    choose = random.choice(new_list)
    return choose


# GetMinMaxMove()

# return the best move for the current player using the MinMax strategy
# to get the allocated 50 points, searching should be 2-ply (one Max and one Min)


# initialize and setup the board
# player assignment and counter initializations
ChessBoardSetup()
# DrawBoard()

# main game loop - while a player is not in checkmate or stalemate (<N turns)
# below is the rough looping strategy
N = 300
turns = 0
checkmate = False
start = True


# to manually configure chess board for testing
def ChessBoardTest():
    global chess_board, start
    start = True
    chess_board = []

    # chess_board += [['.', '.', '.', '.', '.', 'b', 'r', '.']]
    # chess_board += [['p', 'k', 'p', 'p', 'p', 'p', 'p', 'p']]
    # chess_board += [['p', '.', 'q', '.', '.', 't', '.', '.']]
    # chess_board += [['.', '.', '.', '.', '.', '.', 'K', '.']]
    # chess_board += [['.', '.', '.', '.', '.', '.', '.', '.']]
    # chess_board += [['.', '.', '.', '.', '.', 'b', '.', '.']]
    # chess_board += [['.', '.', '.', '.', '.', '.', '.', '.']]
    # chess_board += [['.', '.', '.', '.', '.', '.', '.', '.']]

    chess_board += [['r', 't', 'b', 'q', 'k', 'b', 't', 'r']]
    chess_board += [['q', 'q', 'q', 'p', 'q', 'q', 'q', 'q']]
    chess_board += [['.', '.', '.', '.', '.', '.', '.', '.']]
    chess_board += [['.', '.', '.', '.', '.', '.', '.', '.']]
    chess_board += [['.', '.', '.', '.', '.', '.', '.', '.']]
    chess_board += [['.', '.', '.', '.', '.', '.', '.', '.']]
    chess_board += [['.', '.', '.', '.', '.', '.', '.', '.']]
    chess_board += [['.', '.', '.', 'K', '.', '.', '.', '.']]


# ChessBoardTest()
ChessBoardSetup()
DrawBoard()

che = IsInCheck(1, chess_board)
P = 0
while not checkmate and turns < N:
    # clear_output()
    # DrawBoard()
    # write code to take turns and move the pieces
    # player 0 move

    # origin, destination,checkmate = GetRandomMove(0, chess_board)
    # origin, destination, checkmate = scoredMove(0, chess_board)
    origin, destination, checkmate = GetMinMaxMove(0, chess_board)
    if checkmate:
        print("player 0 has lost")
        DrawBoard()
        break
    chess_board = MovePiece(origin, destination, chess_board)
    print(origin, "moved to", destination)
    DrawBoard()

    # player 1 move.
    origin, destination, checkmate = GetRandomMove(1, chess_board)
    if checkmate:
        print("player 1 has lost")
        origin, destination, checkmate = GetRandomMove(1, chess_board)
        DrawBoard()
        break
    chess_board = MovePiece(origin, destination, chess_board)
    print(origin, "moved to", destination)

    DrawBoard()
    start = False
    time.sleep(0.01)
    turns += 1
    print("turn", str(turns))
# check and print - Stalemate or Checkmate
print(str(turns))
