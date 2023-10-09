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

    def __repr__(self) -> str:
        return f"{cardinfo.get_text_from_rank_id(self.value)} of {cardinfo.get_text_from_shape_id(self.shape)}s"

    def get_text_from_rank_id(id):
        match id:
            case cardvalue.TWO:
                return "2"
            case cardvalue.THREE:
                return "3"
            case cardvalue.FOUR:
                return "4"
            case cardvalue.FIVE:
                return "5"
            case cardvalue.SIX:
                return "6"
            case cardvalue.SEVEN:
                return "7"
            case cardvalue.EIGHT:
                return "8"
            case cardvalue.NINE:
                return "9"
            case cardvalue.TEN:
                return "10"
            case cardvalue.A:
                return "A"
            case cardvalue.J:
                return "J"
            case cardvalue.Q:
                return "Q"
            case cardvalue.K:
                return "K"
            case _:
                raise "invalid id!"

    def get_text_from_shape_id(id):
        match id:
            case cardshape.CLUB:
                return "Club"
            case cardshape.DIAMOND:
                return "Diamond"
            case cardshape.HEART:
                return "Heart"
            case cardshape.SPADE:
                return "Spade"
            case _:
                raise "invalid id!"

class deck_of_cards:

    # clubs
    TWO_OF_CLUBS = cardinfo(cardshape.CLUB, cardvalue.TWO)
    THREE_OF_CLUBS = cardinfo(cardshape.CLUB, cardvalue.THREE)
    FOUR_OF_CLUBS = cardinfo(cardshape.CLUB, cardvalue.FOUR)
    FIVE_OF_CLUBS = cardinfo(cardshape.CLUB, cardvalue.FIVE)
    SIX_OF_CLUBS = cardinfo(cardshape.CLUB, cardvalue.SIX)
    SEVEN_OF_CLUBS = cardinfo(cardshape.CLUB, cardvalue.SEVEN)
    EIGHT_OF_CLUBS = cardinfo(cardshape.CLUB, cardvalue.EIGHT)
    NINE_OF_CLUBS = cardinfo(cardshape.CLUB, cardvalue.NINE)
    TEN_OF_CLUBS = cardinfo(cardshape.CLUB, cardvalue.TEN)
    JOKER_OF_CLUBS = cardinfo(cardshape.CLUB, cardvalue.J)
    QUEEN_OF_CLUBS = cardinfo(cardshape.CLUB, cardvalue.Q)
    KING_OF_CLUBS = cardinfo(cardshape.CLUB, cardvalue.K)
    ACE_OF_CLUBS = cardinfo(cardshape.CLUB, cardvalue.A)

    # diamonds
    TWO_OF_DIAMONDS = cardinfo(cardshape.DIAMOND, cardvalue.TWO)
    THREE_OF_DIAMONDS = cardinfo(cardshape.DIAMOND, cardvalue.THREE)
    FOUR_OF_DIAMONDS = cardinfo(cardshape.DIAMOND, cardvalue.FOUR)
    FIVE_OF_DIAMONDS = cardinfo(cardshape.DIAMOND, cardvalue.FIVE)
    SIX_OF_DIAMONDS = cardinfo(cardshape.DIAMOND, cardvalue.SIX)
    SEVEN_OF_DIAMONDS = cardinfo(cardshape.DIAMOND, cardvalue.SEVEN)
    EIGHT_OF_DIAMONDS = cardinfo(cardshape.DIAMOND, cardvalue.EIGHT)
    NINE_OF_DIAMONDS = cardinfo(cardshape.DIAMOND, cardvalue.NINE)
    TEN_OF_DIAMONDS = cardinfo(cardshape.DIAMOND, cardvalue.TEN)
    JOKER_OF_DIAMONDS = cardinfo(cardshape.DIAMOND, cardvalue.J)
    QUEEN_OF_DIAMONDS = cardinfo(cardshape.DIAMOND, cardvalue.Q)
    KING_OF_DIAMONDS = cardinfo(cardshape.DIAMOND, cardvalue.K)
    ACE_OF_DIAMONDS = cardinfo(cardshape.DIAMOND, cardvalue.A)

    # hearts
    TWO_OF_HEARTS = cardinfo(cardshape.HEART, cardvalue.TWO)
    THREE_OF_HEARTS = cardinfo(cardshape.HEART, cardvalue.THREE)
    FOUR_OF_HEARTS = cardinfo(cardshape.HEART, cardvalue.FOUR)
    FIVE_OF_HEARTS = cardinfo(cardshape.HEART, cardvalue.FIVE)
    SIX_OF_HEARTS = cardinfo(cardshape.HEART, cardvalue.SIX)
    SEVEN_OF_HEARTS = cardinfo(cardshape.HEART, cardvalue.SEVEN)
    EIGHT_OF_HEARTS = cardinfo(cardshape.HEART, cardvalue.EIGHT)
    NINE_OF_HEARTS = cardinfo(cardshape.HEART, cardvalue.NINE)
    TEN_OF_HEARTS = cardinfo(cardshape.HEART, cardvalue.TEN)
    JOKER_OF_HEARTS = cardinfo(cardshape.HEART, cardvalue.J)
    QUEEN_OF_HEARTS = cardinfo(cardshape.HEART, cardvalue.Q)
    KING_OF_HEARTS = cardinfo(cardshape.HEART, cardvalue.K)
    ACE_OF_HEARTS = cardinfo(cardshape.HEART, cardvalue.A)

    # spades
    TWO_OF_SPADES = cardinfo(cardshape.SPADE, cardvalue.TWO)
    THREE_OF_SPADES = cardinfo(cardshape.SPADE, cardvalue.THREE)
    FOUR_OF_SPADES = cardinfo(cardshape.SPADE, cardvalue.FOUR)
    FIVE_OF_SPADES = cardinfo(cardshape.SPADE, cardvalue.FIVE)
    SIX_OF_SPADES = cardinfo(cardshape.SPADE, cardvalue.SIX)
    SEVEN_OF_SPADES = cardinfo(cardshape.SPADE, cardvalue.SEVEN)
    EIGHT_OF_SPADES = cardinfo(cardshape.SPADE, cardvalue.EIGHT)
    NINE_OF_SPADES = cardinfo(cardshape.SPADE, cardvalue.NINE)
    TEN_OF_SPADES = cardinfo(cardshape.SPADE, cardvalue.TEN)
    JOKER_OF_SPADES = cardinfo(cardshape.SPADE, cardvalue.J)
    QUEEN_OF_SPADES = cardinfo(cardshape.SPADE, cardvalue.Q)
    KING_OF_SPADES = cardinfo(cardshape.SPADE, cardvalue.K)
    ACE_OF_SPADES = cardinfo(cardshape.SPADE, cardvalue.A)