

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
# Make pawns use pawns ahead of them as scouts. We assume that every pawn ahead of us has no enemies that can capture 
# it directly
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


    """
      c c x c c
      c c c c c
      c c c c c  
    """
    pawnsBehind = 0

    pawnsAhead = 0

    """
                ->     x
        c x c   ->   c c c
        c c c   ->   c   c
    """
    nearPawnsBehind = 0

    pawnsNearColBehind = 0

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
                    if (dist(row2, col2, row, col) <= 2):
                        nearPawnsBehind = nearPawnsBehind + 1
                    if abs(col - col2) <= 1:
                        pawnsNearColBehind = pawnsNearColBehind + 1
                else:
                    pawnsAhead = pawnsAhead + 1
                    if (col2 == col and row2 == endIndex):
                        pawnAtEndRowOfSameLine = True
            else:
                if (row2 >= row):
                    pawnsBehind = pawnsBehind + 1
                    if (dist(row2, col2, row, col) <= 2):
                        nearPawnsBehind = nearPawnsBehind + 1
                    if abs(col - col2) <= 1:
                        pawnsNearColBehind = pawnsNearColBehind + 1
                else:
                    pawnsAhead = pawnsAhead + 1
                    if (col2 == col and row2 == endIndex):
                        pawnAtEndRowOfSameLine = True
            
    # determine if the pawn has enough support to be reckless
    # if enough pawns right behind that cup this pawn, go forward
    # if (col >= 2 and col <= board_size - 3):
        if (nearPawnsBehind >= 5 and pawnsNearColBehind >= 8): 
            if pawnsBehind >= 10:
                hasSupport = True
    # elif (col == 1 or col == board_size - 2):
    #     if nearPawnsBehind >= 5 and pawnsNearColBehind >= 8 and pawnsBehind >= 9:
    #         hasSupport = True
    # if (nearPawnsBehind >= 5 and pawnsNearColBehind >= 8): 
    #     hasSupport = True
    # else:
    #     if nearPawnsBehind >= 3 and pawnsNearColBehind >= 5 and pawnsBehind >= 7:
    #         hasSupport = True
    
    # if near end row, be a little more reckless
    distToEnd = abs(row - endIndex)
    if (distToEnd <= 3):
        if (nearPawnsBehind >= 4):
            hasSupport = True
    # if there is a pawn ahead at this point, then it is like this
    """
    endrow:     _ o _ _ _
                _ c _ _ _
                _ c x _ _
                _ c c _ _
    """
    if (distToEnd <= 2):
        if (nearPawnsBehind >= 3 and pawnsAhead >= 1):
            hasSupport = True

    # if see friend 2 spaces forward, and has 1 friends right behind same col
    # if (posInSet(friends, row + forward * 2, col) and posInSet(friends, row - forward, col)):
    #     hasSupport = True

    # """ Go forward if this and near end
    #   _ _ c
    #   _ x c 
    #   c c c
    #   c c c
    # """
    # if posInSet(friends, row - forward, col + 1) and posInSet(friends, row - forward, col) and posInSet(friends, row - forward, col - 1) and posInSet(friends, row - forward * 2, col + 1) and posInSet(friends, row - forward * 2, col - 1) and posInSet(friends, row - forward * 2, col) and nearPawnsBehind >= 4 and (posInSet(friends, row + forward, col + 1) or posInSet(friends, row + forward, col + 1)) and distToEnd <= 4:
    #     hasSupport = True

    

    if check_space_wrapper(row + forward, col + 1, board_size) == opp_team:
        capture(row + forward, col + 1)
    elif check_space_wrapper(row + forward, col - 1, board_size) == opp_team:
        capture(row + forward, col - 1)
    else:
        # try to advance and gain ground if we are behind the half
        advance = True
        # if (forward == 1 and row < board_size / 2):
        #     advance = True
        # elif forward == -1 and row > board_size / 2:
        #     advance = True

        # if moving forward is not a capturable position or has enough pawn support, try to go forward
        badPos = canGetCaptured(row + forward, col, sensedEnemiesSet, forward)
        if (not badPos) or (hasSupport and advance):
            if inBoard(row + forward, col, board_size):
                if not check_space(row + forward, col):
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

def dist(r1, c1, r2, c2):
    return pow(r1 - r2, 2) + pow(c1 - c2, 2)

def posInSet(s, r, c):
    global board_size
    return (r*board_size + c) in s