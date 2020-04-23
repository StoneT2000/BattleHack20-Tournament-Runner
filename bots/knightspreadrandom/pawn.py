

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
index = 0
endIndex = board_size - 1   
if team == Team.WHITE:
    forward = 1
    index = 0
    endIndex = board_size - 1
else:
    forward = -1
    index = board_size - 1
    endIndex = 0


# TODO:
# Make pawns stop at 2nd to last row, maximize capturing for weaker bots
#   Means we need to make overlord consider pawns at 2nd to last row to be ones that reach end already
#
def run():
    global team, endIndex, index, board_size, opp_team, forward
    row, col = get_location()
    
    
    """ Logic
    Pawn will move directly forward iff it is safe
    If unsafe
        If pawn has support behind it
            go and suicide 
        else
            Stay still
    """

    movedForward = False

    hasSupport = False

    sensed = sense()
    sensedEnemiesSet = set()
    friends = set()
    pawnsBehind = 0
    pawnsAhead = 0

    #
    #   x <- me
    #   
    #   x <- end row
    # this means me needs to gtfo of this line
    pawnAtEndRowOfSameLine = False

    # add hashes of enemy locations in vision
    for row2, col2, team in sensed:
        if (team == opp_team):
            sensedEnemiesSet.add(row2 * board_size + col2)
        else:
            friends.add(row2 * board_size + col2)
            # count number of pawns behind and ahead
            if forward == 1:
                if (row2 <= row):
                    pawnsBehind = pawnsBehind + 1
                else:
                    pawnsAhead = pawnsAhead + 1
                    if (col2 == col and row2 == endIndex):
                        pawnAtEndRowOfSameLine = True
            else:
                if (row2 >= row):
                    pawnsBehind = pawnsBehind + 1
                else:
                    pawnsAhead = pawnsAhead + 1
                    if (col2 == col and row2 == endIndex):
                        pawnAtEndRowOfSameLine = True
            
    # determine if the pawn has enough support to be reckless
    if (pawnsBehind >= 5): 
        hasSupport = True

    # try catpuring pieces
    if check_space_wrapper(row + forward, col + 1, board_size) == opp_team:
        capture(row + forward, col + 1)
    elif check_space_wrapper(row + forward, col - 1, board_size) == opp_team:
        capture(row + forward, col - 1)
    else:
        # if moving forward is not a capturable position or has enough pawn support, try to go forward
        badPos = canGetCaptured(row + forward, col, sensedEnemiesSet, forward)
        if (not badPos) or hasSupport:
            if inBoard(row + forward, col, board_size):
                if not check_space(row + forward, col):
                    # if friend on left or right, that means they will capture for a capture, so go forward
                    
                    if (row * board_size + col - 1) in friends or (row * board_size + col + 1) in friends:
                        move_forward()
                        movedForward = True
                    # if (friend on forward right or left) and friend behind you, then go forward because
                    # friend behind you can go up and protect the friends to the forward right and left (usually...)
                    elif ((((row + forward) * board_size + col - 1) in friends or ((row + forward) * board_size + col + 1) in friends) and ((row - forward * board_size) + col) in friends) :
                        move_forward()
                        movedForward = True
                    # if the forward position is uncapturable, take that territory and move forward
                    elif not badPos:
                        move_forward()
                        movedForward = True


def canGetCaptured(row3, col3, sensedEnemiesSet, forward):
    global board_size
    hash_part = (row3 + forward) * board_size
    if (hash_part + col3 - 1) in sensedEnemiesSet or (hash_part + col3 + 1) in sensedEnemiesSet:
        return True
    return False

def inBoard(r, c, board_size):
    if r < 0 or c < 0 or c >= board_size or r >= board_size:
        return False
    return True