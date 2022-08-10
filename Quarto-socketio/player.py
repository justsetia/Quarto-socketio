in_game = []


def player_info(name):
    name = name+'\n'
    with open('id_player.txt', 'r') as f:
        for i in f:
            if name == i:
                if name in in_game:
                    return 'in_game'
                else:
                    in_game.append(name)
                return 'right'
        return'wrong'


def rep_account(name):
    user = ''
    for i in name:
        if i == ':':
            break
        else:
            user += i
    with open('id_player.txt', 'r') as f:
        for i in f:
            if i != '\n':
                if user == i[:i.index(':'):]:
                    return 'wrong'
        return'right'


def add_info(username):
    res = rep_account(username)
    if res == 'wrong':
        return 'repeat'

    else:
        with open('id_player.txt', 'a') as f:
            f.write(username+'\n')
            with open('score_player', 'r+') as F:
                F.read()
                F.write(username + ' ')
                F.write('0' + ' ' + '0' + ' ' + '0' + ' ')
            return 'added'


def score_winer(name):
    file = ''
    with open('score_player', 'r+') as f:
        for i in f:
            file += i
        file = file.split()
        score = file[file.index(name)+1:file.index(name)+2:]
        file = file[:file.index(name)+1:] + \
            [str(int(score[0])+1)] + file[file.index(name)+2::]
    with open('score_player', 'w') as F:
        for i in file:
            F.write(i+' ')
        return file


def score_loser(name):
    file = ''
    with open('score_player', 'r+') as f:
        for i in f:
            file += i
        file = file.split()
        score = file[file.index(name)+2:file.index(name)+3:]
        file = file[:file.index(name)+2:] + \
            [str(int(score[0])+1)] + file[file.index(name)+3::]
    with open('score_player', 'w') as F:
        for i in file:
            F.write(i+' ')
        return file


def score_tie(name):
    file = ''
    with open('score_player', 'r+') as f:
        for i in f:
            file += i
        file = file.split()
        score = file[file.index(name)+3:file.index(name)+4:]
        file = file[:file.index(name)+3:] + \
            [str(int(score[0])+1)] + file[file.index(name)+4::]
    with open('score_player', 'w') as F:
        for i in file:
            F.write(i+' ')
        return file
