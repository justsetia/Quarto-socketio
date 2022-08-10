from gevent import pywsgi
from gevent.server import DatagramServer
from socketio import *


server = Server(async_mode='gevent')
playerid = []
n = 0


@server.event
def connect(sid, environ, auth):
    playerid.append(sid)
    #print(sid, "connected!")


@server.on('getting_info')
def getting_info(sid, data):
    user_pass = data
    import player
    res = player.player_info(data)
    if res == 'in_game':
        return 'in_game'
    if res == 'right':
        return [res, user_pass]
    else:
        return 'wrong'


@server.on('id_giving')
def id_giving(sid, x):
    global playerid
    global n
    if x == 'reset':
        if len(playerid) == 4:
            playerid = []
            n = 0
        playerid.append(sid)
    playerid.append([sid])
    return playerid


@server.on('creating_account')
def creating_account(sid, data):
    user_pass = data
    import player
    isrepeat = player.add_info(data)
    if isrepeat == 'repeat':
        return 'repeat'

    else:
        return ['done', user_pass]


# _________________________________________________________________________________


@server.on('prepare')
def prepare(sid, data):
    global n
    send = []
    import gametest
    peice = gametest.give_peice()
    board = gametest.board()
    send.append(peice)
    send.append(board)
    player(send, n)


def loser(x):
    server.emit('player_lose', data='no', callback=print, room=playerid[0])


def print(file):
    server.emit('print_file', data=file)


def quarto_check(quarto):
    import gametest
    res = gametest.quarto_check(quarto)
    return res


def player(send, n):
    n += 1
    global playerid
    playerid = playerid+playerid[:2:]
    playerid = playerid[2::]
    if n % 2 == 0:
        send = player1(send, playerid[0])
    else:
        send = player1(send, playerid[1])


def player1(send, sid):
    server.emit('turn_choose', data=send,
                callback=player2, room=sid)


def player2(send):
    global n
    if n % 2 == 0:
        sid = playerid[2]
        server.emit('turn_play', data=send, callback=fix, room=sid)
    else:
        sid = playerid[0]
        server.emit('turn_play', data=send, callback=fix, room=sid)


def tie(user):
    import player
    player.score_tie(user)
    server.emit('player_tie_id', data='tie', callback=tie_2, room=playerid[2])


def tie_2(user):
    import player
    file = player.score_tie(user)
    server.emit('print_file', data=file)


def fix(send):
    pre_send = send
    peice = send[0]
    board = send[1]
    chosen_peice = send[2]
    chosen_place = send[3]
    import gametest
    board, peice = gametest.fix(
        chosen_peice, board, chosen_place, peice)

    if board == 'tie':
        server.emit('player_tie_id', data='tie',
                    callback=tie, room=playerid[0])
    else:
        send = []
        send.append(peice)
        send.append(board)
        if len(pre_send) > 4:
            res = quarto_check(send)
            if res == 'yes':
                server.emit('player_win', data='yes',
                            callback=loser, room=playerid[2])
            else:
                send = send[:3:]
                player(send, n+1)
        else:
            player(send, n+1)

    # _________________________________________________________________


app = WSGIApp(server)
pywsgi.WSGIServer(("127.0.0.1", 5000), app).serve_forever()


#emit(event, data=None, to=None, room=None, skip_sid=None, namespace=None, callback=None, **kwargs)
