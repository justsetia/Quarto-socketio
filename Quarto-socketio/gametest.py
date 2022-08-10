def give_peice():
    peice = ['1)TWSE', '2)TWSF', '3)TWCF', '4)TWCE', '5)TBSF', '6)TBSE', '7)TBCF', '8)TBCE',
             '9)KWSE', '10)KWSF', '11)KWCF', '12)KWCE', '13)KBSF', '14)KBSE', '15)KBCF', '16)KBCE']
    return peice


def board():
    board = [' ║', ' 1 1', ' 1 2', ' 1 3', ' 1 4', ' ║', ' 2 1',  ' 2 2', ' 2 3',
             ' 2 4', ' ║', ' 3 1',  ' 3 2', ' 3 3', ' 3 4', ' ║', ' 4 1',  ' 4 2', ' 4 3', ' 4 4']
    return board


def fix(chosen_peice, board, chosen_place, peice):
    chosen_place = ' '+chosen_place
    n = board.index(chosen_place)
    m = int(chosen_peice)-1
    chosen_peice = peice[m]
    if len(chosen_peice) > 6:
        board = board[:n:] + [chosen_peice[3::]] + board[n+1::]
    else:
        board = board[:n:] + [chosen_peice[2::]] + board[n+1::]
    peice = peice[:m:]+[' ×× ']+peice[m+1::]
    tie = ''
    for i in board:
        if i != ' ║':
            tie += i
    tie = tie.split()
    tie_check = ''
    for i in tie:
        tie_check += i
    if tie_check.isalpha():
        return 'tie', peice
    else:
        return board, peice


def quarto_check(send):
    board = send[1]
    for n in range(1, 17, 5):
        check = ''
        for i in board[n: n+5:]:
            check += i
        if check.count('W') == 4 or check.count('B') == 4:
            return 'yes'
        elif check.count('T') == 4 or check.count('K') == 4:
            return 'yes'
        elif check.count('S') == 4 or check.count('C') == 4:
            return 'yes'
        elif check.count('F') == 4 or check.count('E') == 4:
            return 'yes'
    for n in range(1, 5,):
        check = ''
        for i in board[n::5]:
            check += i
        if check.count('W') == 4 or check.count('B') == 4:
            return 'yes'
        elif check.count('T') == 4 or check.count('K') == 4:
            return 'yes'
        elif check.count('S') == 4 or check.count('C') == 4:
            return 'yes'
        elif check.count('F') == 4 or check.count('E') == 4:
            return 'yes'
    check = ''
    for i in board[1::6]:
        check += i
        if check.count('W') == 4 or check.count('B') == 4:
            return 'yes'
        elif check.count('T') == 4 or check.count('K') == 4:
            return 'yes'
        elif check.count('S') == 4 or check.count('C') == 4:
            return 'yes'
        elif check.count('F') == 4 or check.count('E') == 4:
            return 'yes'
    check = ''
    for i in board[4::4]:
        check += i
        if check.count('W') == 4 or check.count('B') == 4:
            return 'yes'
        elif check.count('T') == 4 or check.count('K') == 4:
            return 'yes'
        elif check.count('S') == 4 or check.count('C') == 4:
            return 'yes'
        elif check.count('F') == 4 or check.count('E') == 4:
            return 'yes'

    return 'no'
