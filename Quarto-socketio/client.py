from socketio import *


client = Client()
client.connect("http://127.0.0.1:5000")


@client.event
def connect():
    print('connected')


@client.event
def connect_error():
    print('disconnected')


@client.on('turn_play')
def turn_play(list):
    peice = list[0]
    board = list[1]
    print(' ╔══════╦══════╦══════╦══════╗')
    print(board[0], end='')
    for times in range(1, 20,):
        if times % 5 != 0:
            print(board[times], end='  ║')
        else:
            print()
            print(' ╠══════╬══════╬══════╬══════╣')
            print(board[times], end='')
    print()
    print(' ╚══════╩══════╩══════╩══════╝')
    special_peice = peice[int(list[2])-1]
    if len(special_peice) == 7:
        special_peice = special_peice[1::]
    print('\n'+'Your peice is = '+special_peice[2::])
    chosen_place = input('\nChoose a place : ')
    list.append(chosen_place)
    is_quarto = input('\nIs it quarto ? 1)Yes  2) NO : ')
    if is_quarto == '1':
        list.append('win')
    return list


@client.on('turn_choose')
def turn_choose(data):
    send = data
    peice = send[0]
    board = send[1]

    for times in range(0, 16,):
        if times % 4 != 0:
            print(peice[times], end='  ')
        else:
            print('\n\n')
            print(peice[times], end='  ')
    print()
    chosen_peice = input('\nChoose one peice...: ')
    send.append(chosen_peice)
    return send


@client.on('print_file')
def print_file(file):

    while file != []:
        name = file[0:1:][0]
        name = name[:name.index(':'):]
        print(name + ' =   win : ' + file[1: 2:][0] +
              ' lose : '+file[2:3:][0] + ' tie : ' + file[3: 4:][0]+'\n')
        file = file[4::]

    answer = input('Do you want to play again? 1)Yes  2)No : ')
    if answer == '2':
        print(' Ok bye see you later \U0001F44B ... ')
        client.disconnect()
    else:
        print("Awsome Let's have fun ...")
        client.emit('id_giving', data='reset', callback=start_after)


@client.on('player_tie_id')
def player_tie_id(x):
    print('\n No winer No loser \U0001F642 \n')
    return user


@client.on('player_win')
def player_win(res):
    print('\n\nCongratulation You won \U0001F929 \n\n')
    import player
    player.score_winer(user)
    return res


@client.on('player_lose')
def player_lose(x):
    print('\n Oops You lost \U0001F615 \n\n')
    import player
    file = player.score_loser(user)
    return file


def start(perm):
    print("\nGreat let's play \U0001F92A ")
    if input('Do you know how to play 1)yes 2)no ?') == '2':
        f = open('rule.txt', 'r')
        print(f.read())
    client.emit('id_giving', data='1', callback=start_after)


def start_after(sid):
    input('\nAre you ready \U0001F4AA  ? 1) YES  : ')

    if len(sid) == 2:
        client.emit('prepare', data='1')


def right_account(res):
    if res == 'in_game':
        chance = input(
            'You are in game \U0001F610 : \n 1)Sorry i try another account : ')
        if chance == '1':
            have_account()
    if res == 'wrong':
        chance = input(
            'Wrong password or username \U0001F62C : 1) try again  2)create an account = ')
        if chance == '1':
            have_account()
        else:
            create_account()

    elif res == 'repeat':
        print('\n \U0001F4A2 This username is taken ... try again \n')
        create_account()

    else:
        global user
        user = res[1]
        start('done')


def have_account():
    user_pass = input('Enter your username : ')
    user_pass = user_pass + ':'+str(input('Enter your password \U0001F441 : '))
    client.emit('getting_info', data=user_pass, callback=right_account)


def create_account():
    user_pass = str(input('Enter username : '))
    user_pass = user_pass + ':'+str(input('Enter a password \U0001F441 : '))
    client.emit('creating_account', data=user_pass, callback=right_account)


user = ''
is_account = input(
    '\n Hello Welcome \U0001F497 \n Do you have an account? 1)Yes  2)No \n : ')
if is_account == '1':
    have_account()
else:
    create_account()
