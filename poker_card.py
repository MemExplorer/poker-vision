class cardshape:
    CLUB = 0
    DIAMOND = 1
    HEART = 2
    SPADE = 3

class cardvalue:
    TWO = 0
    THREE = 1
    FOUR = 2
    FIVE = 3
    SIX = 4
    SEVEN = 5
    EIGHT = 6
    NINE = 7
    TEN = 8
    J = 9
    Q = 10
    K = 11
    A = 12
    
class cardinfo:
    def __init__(self, shape, value):
        self.shape = shape
        self.value = value