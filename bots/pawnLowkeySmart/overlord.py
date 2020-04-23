
DEBUG = 1
def dlog(str):
    if DEBUG > 0:
        log(str)

startSpawnIndex = -1
spawnIndex = startSpawnIndex


# idea - Focus on lanes 3 - 13, 10 lanes only
def run():
    global spawnIndex
    team = get_team()
    opp_team = Team.WHITE if team == Team.BLACK else team.BLACK
    board_size = get_board_size()

    if team == Team.WHITE:
        index = 0
        endIndex = board_size - 1
    else:
        index = board_size - 1
        endIndex = 0

    board = get_board()
    freeSpots = board[index]
    endRow = board[endIndex]
    
    attackableLanes = set()

    for i in range(board_size):
        if not (endRow[i] == team):
            attackableLanes.add(i)
    
    while (True):

        spawnIndex = (spawnIndex + 1) % board_size
        if spawnIndex in attackableLanes:
            if not check_space(index, spawnIndex):
                spawn(index, spawnIndex)
                break
        

    # for _ in range(board_size):
    #     spawnIndex = (spawnIndex + 1) % board_size
    #     if spawnIndex > startSpawnIndex + 10:
    #         spawnIndex = startSpawnIndex
    #     if not check_space(index, spawnIndex):
    #         spawn(index, spawnIndex)
    #         break
        