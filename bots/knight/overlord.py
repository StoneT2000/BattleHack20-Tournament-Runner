
DEBUG = 1
def dlog(str):
    if DEBUG > 0:
        log(str)

SPAWN_WIDTH = 7 # Must be such that startSpawnIndex + SPAWN_WIDTH doesn't go past board_size=16
startSpawnIndex = 1
spawnIndex = startSpawnIndex
board_size = get_board_size()
team = get_team()
opp_team = Team.WHITE if team == Team.BLACK else team.BLACK

takenLanesSoFar = 0

index = 0
turn = 0
endIndex = board_size - 1
forward = 1
if team == Team.WHITE:
    forward = 1
    index = 0
    endIndex = board_size - 1
else:
    index = board_size - 1
    forward = -1
    endIndex = 0
# idea - Focus on lanes 3 - 13, 10 lanes only
# then focus on other lanes

def run():
    global spawnIndex, board_size, opp_team, startSpawnIndex, SPAWN_WIDTH, forward, index, endIndex, team, takenLanesSoFar, turn
    turn = turn + 1
    board = get_board()


    spawnRow = board[index]
    endRow = board[endIndex]
    
    attackableLanes = set()

    # store what lanes/columns are not occupied by us already so we prioritize some other lanes
    for i in range(board_size):
        if not (endRow[i] == team):
            attackableLanes.add(i)
            attackableLanes.add(i - 1)
            attackableLanes.add(i + 1)


    # spawned already or not
    spawned = False

    # the index we are trying to start spawning on
    beginSpawn = spawnIndex
    while (True):
        
        sindex = getNextSpawnIndex()
        if sindex in attackableLanes:
            if (not check_space(index, sindex) and not willGetCaptured(board, index, sindex)):
                spawn(index, sindex)
                spawned = True
                break

        # if we wrapped around for spawn indexes, stop
        if sindex == beginSpawn:
            break
    
    # looped over and found no spawnindex in attackable lanes, just spawn anywhere
    if not spawned:
        while (True):
            sindex = getNextSpawnIndex()
            if (not check_space(index, sindex) and not willGetCaptured(board, index, sindex)):
                spawn(index, sindex)
                spawned = True
                break
        
            # if we wrapped around for spawn indexes, stop
            if sindex == beginSpawn:
                break
        
# get the next spawning index
def getNextSpawnIndex():
    global spawnIndex, SPAWN_WIDTH, board_size
    spawnIndex = (spawnIndex + 1) % board_size
    if spawnIndex > startSpawnIndex + SPAWN_WIDTH:
        spawnIndex = startSpawnIndex

    return spawnIndex

# if spawning on row col will get captured by a unit
def willGetCaptured(board, row, col):
    global forward, opp_team
    if (col >= 1 and board[row + forward][col - 1] == opp_team):
        return True
    if (col <= board_size - 2 and board[row + forward][col + 1] == opp_team):
        return True
    return False