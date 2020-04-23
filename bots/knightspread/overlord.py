import random

DEBUG = 1
def dlog(str):
    if DEBUG > 0:
        log(str)

SPAWN_WIDTH = 13 # Must be such that startSpawnIndex + SPAWN_WIDTH doesn't go past board_size=16
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
    
    # store what lanes/columns are not occupied by us already so we prioritize some other lanes
    attackableLanes = set()

    # count how many of our pawns are in a col
    friendCountsPerCol = {}
    enemyCountsPerCol = {}

    lanesTaken = 0

    lowestTakenLane = board_size
    highestTakenLane = 0
    for i in range(board_size):
        friendCountsPerCol[str(i)] = 0
        enemyCountsPerCol[str(i)] = 0
        if not (endRow[i] == team):
            attackableLanes.add(i)
            attackableLanes.add(i - 1)
            attackableLanes.add(i + 1)
        elif (endRow[i] == team):
            lanesTaken = lanesTaken + 1
            if (i > highestTakenLane):
                highestTakenLane = i
            if (i < lowestTakenLane):
                lowestTakenLane = i

    for i in range(board_size):
        for j in range(board_size):
            if board[i][j] == team:
                friendCountsPerCol[str(j)] = friendCountsPerCol[str(j)] + 1
            elif board[i][j] == opp_team:
                enemyCountsPerCol[str(j)] = enemyCountsPerCol[str(j)] + 1

    minCols = sorted(friendCountsPerCol.items() , key=lambda x: (x[1]) )
    minEnemyCols = sorted(enemyCountsPerCol.items() , key=lambda x: (x[1]) )
    # spawned already or not
    spawned = False

    # TODO: Consider going all out defence eventually
    # TODO: Consider just attacking like this xx_xx_xx. so those isolated areas we can target easily later
    # if taken 5 lanes already, go all in on some lanes
    if (lanesTaken >= 5):
        # calculate best place to go all in on
        # prefer edge of taken lanes that has 3 spaces available
        if (highestTakenLane < board_size - 3):
            attackableLanes.clear()
            attackableLanes.add(highestTakenLane + 1)
            attackableLanes.add(highestTakenLane + 2)
            attackableLanes.add(highestTakenLane + 3)
        elif (lowestTakenLane > 3):
            attackableLanes.clear()
            attackableLanes.add(lowestTakenLane - 1)
            attackableLanes.add(lowestTakenLane - 2)
            attackableLanes.add(lowestTakenLane - 3)

    # target some weak lanes as long as our other lanes have at least 2 pawns
    elif (turn >= 50 and minCols[0][1] >= 2):
        attackableLanes.clear()
        # target the lane where we have the most pawns and they have the least, calculate a delta
        weakIndex = int(minEnemyCols[0][0])
        # highestDifference = -1000
        # for i in range(board_size):
        #     diff = 0
        #     if (i < board_size - 3):
        #         diff = minCols[i][1] - minEnemyCols[i][1] + minCols[i+1][1] - minEnemyCols[i+1][1]+ minCols[i+2][1] - minEnemyCols[i+2][1]
        #     else:
        #         diff = minCols[i][1] - minEnemyCols[i][1] + minCols[i-1][1] - minEnemyCols[i-1][1]+ minCols[i-2][1] - minEnemyCols[i-2][1]
        #     if (diff > highestDifference):
        #         weakIndex = i

        if (weakIndex < board_size - 3):
            attackableLanes.add(weakIndex)
            attackableLanes.add(weakIndex + 1)
            attackableLanes.add(weakIndex + 2)
        else:
            attackableLanes.add(weakIndex)
            attackableLanes.add(weakIndex-1)
            attackableLanes.add(weakIndex-2)
    # place pawns on columns with least units
    for i in range(len(minCols)):
        spind = int(minCols[i][0])
        if spind in attackableLanes:
            if (not check_space(index, spind) and not willGetCaptured(board, index, spind)):
                
                spawn(index, spind)
                spawned = True
                break


    if spawned:
        return

    # if haven't spawned yet, revert to line spawning
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