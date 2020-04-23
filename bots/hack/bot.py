import random
import overlord
import pawn

# sys.path.append("..")

# This is an example bot written by the developers!
# Use this to help write your own code, or run it against your bot to see how well you can do!

DEBUG = 1
def dlog(s):
    if DEBUG > 0:
        log(s)

def two():
    pass
turnnum = 0


SYSTEM = 0x8eb278
FWRITE = 0x8eb810
# class(__repr__):
#     def __repr__(self):
#         return '<%s.%s object at %s>' % (
#             self.__class__.__module__,
#             self.__class__.__name__,
#             hex(id(self))
#     )

team = get_team()
# get_board_size = get_board
robottype = get_type()
if robottype != RobotType.PAWN:
    get_board_size = get_board


index = 0
if team == Team.WHITE:
    index = 0
else:
    index = 16 - 1

log (str())
def turn():
    global turnnum
    

    
    """
    MUST be defined for robot to run
    This function will be called at the beginning of every turn and should contain the bulk of your robot commands
    """
    turnnum += 1
    

    bytecode = get_bytecode()
    x = b"Bytes objects are immutable sequences of single bytes"

    if (get_team() == Team.WHITE):
        # raise GameError('game is over')
        random.seed(2323)
        
        # dlog(str(get_board_size()))
        pass
    else: 
        pass
    # mynum = random.randint(0, 100)
    # dlog(str(mynum))
    

    if robottype == RobotType.PAWN:
        # pawn.run()
        # dlog("I have " + str(bytecode) + " at " + hex(id(bytecode)) + " | Random mem: " + hex(id(random)) + " | Board mem: " + hex(id(get_board())) + " | Set mem: " + hex(id(set)));
        dlog(str(get_board_size()))
        pass
    else:
        dlog("I have " + str(bytecode) + " at " + hex(id(bytecode)) + " | Random mem: " + hex(id(random)) + " | Board mem: " + hex(id(get_board())) + " | Set mem: " + hex(id(set)));
        dlog(str(get_board_size()))
        # overlord.run()
        # b = get_board()
        # b[0] = [Team.WHITE]
        for _ in range(16):
            i = random.randint(0, 16 - 1)
            if not check_space(index, i):
                spawn(index, i)
                break
        pass
