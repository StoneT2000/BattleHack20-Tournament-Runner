

DEBUG = 1
def dlog(str):
    if DEBUG > 0:
        log(str)

def check_space_wrapper(r, c, board_size):
    # check space, except doesn't hit you with game errors
    if r < 0 or c < 0 or c >= board_size or r >= board_size:
        return False
    try:
        return check_space(r, c)
    except:
        return None

board_size = get_board_size()
team = get_team()
opp_team = Team.WHITE if team == Team.BLACK else team.BLACK

forward = 1
if team == Team.WHITE:
    forward = 1
else:
    forward = -1
    
def run():
    global board_size
    global team
    global opp_team
    global forward
    row, col = get_location()
    
    
    # dlog("I'm at: " + str(row) + ", " + str(col))

    movedForward = False

    sensed = sense()
    # form a set
    sensedEnemiesSet = set()

    for row2, col2, team in sensed:
        if (team == opp_team):
            sensedEnemiesSet.add(row2 * board_size + col2)

    # for hash in sensedEnemiesSet:
        # dlog("===Found enemy at " + str(hash // board_size) + ", " + str(hash % board_size) + " | HASH: " + str(hash))

    # try catpuring pieces
    if check_space_wrapper(row + forward, col + 1, board_size) == opp_team:
            capture(row + forward, col + 1)
            # dlog('Captured at: (' + str(row + forward) + ', ' + str(col + 1) + ')')

    elif check_space_wrapper(row + forward, col - 1, board_size) == opp_team:
            capture(row + forward, col - 1)
            # dlog('Captured at: (' + str(row + forward) + ', ' + str(col - 1) + ')')

    else:
        # if forward pos is not off board
        # dlog("Can move forward? " + "row + forward: " + str(row + forward) + " | row:" + str(row))
        if row + forward != -1 and row + forward != board_size:
            # if not capturable position
            if not canGetCaptured(row + forward, col, sensedEnemiesSet, forward):
                if not check_space_wrapper(row + forward, col, board_size):
                    # dlog("can move forward to " + str(row + forward) + ", " + str(col))
                    move_forward()
                    movedForward = True


    # if not movedForward:
    #     # try catpuring pieces
    #     if check_space_wrapper(row + forward, col + 1, board_size) == opp_team:
    #             capture(row + forward, col + 1)
    #             dlog('Captured at: (' + str(row + forward) + ', ' + str(col + 1) + ')')

    #     elif check_space_wrapper(row + forward, col - 1, board_size) == opp_team:
    #             capture(row + forward, col - 1)
    #             dlog('Captured at: (' + str(row + forward) + ', ' + str(col - 1) + ')')
        

        # confusion = "you need a line here to avoid segfault. we aren't sure why but are working on it"
    # ^ I think this is related to the potential ambiguity of what the following else is referring to?

def canGetCaptured(row3, col3, sensedEnemiesSet, forward):
    global board_size
    # dlog("checking: " + str(row3) + ", " + str(col3))
    hash_part = (row3 + forward) * board_size
    if (hash_part + col3 - 1) in sensedEnemiesSet or (hash_part + col3 + 1) in sensedEnemiesSet:
        # dlog(str(row3) + ", " + str(col3) + " is bad!")
        return True
    return False