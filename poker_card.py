class card_suit:
    CLUB = 0
    DIAMOND = 1
    HEART = 2
    SPADE = 3
    UNKNOWN = 4

class card_rank:
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
    UNKNOWN = 13
    
def card_suit_from_yolo(id):
    match id:
        case "club":
            return card_suit.CLUB
        case "diamond":
            return card_suit.DIAMOND
        case "heart":
            return card_suit.HEART
        case "spade":
            return card_suit.SPADE
        case _:
            raise "NOT SUPPORTED SUIT!"

def card_rank_from_yolo(id):
    match id:
        case "2":
            return card_rank.TWO
        case "3":
            return card_rank.THREE
        case "4":
            return card_rank.FOUR
        case "5":
            return card_rank.FIVE
        case "6":
            return card_rank.SIX
        case "7":
            return card_rank.SEVEN
        case "8":
            return card_rank.EIGHT
        case "9":
            return card_rank.NINE
        case "10":
            return card_rank.TEN
        case "A":
            return card_rank.A
        case "J":
            return card_rank.J
        case "K":
            return card_rank.K
        case "Q":
            return card_rank.Q
        case _:
            raise "NOT SUPPORTED RANK!"
class cardinfo:
    def __init__(self, shape, value):
        self.shape = shape
        self.value = value

    def __str__(self):
        if self.shape == card_suit.UNKNOWN and self.value == card_rank.UNKNOWN:
            return "Unknown"
        
        return f"{cardinfo.get_text_from_rank_id(self.value)} of {cardinfo.get_text_from_shape_id(self.shape)}s"

    def __repr__(self) -> str:
        if self.shape == card_suit.UNKNOWN and self.value == card_rank.UNKNOWN:
            return "Unknown"
        
        return f"{cardinfo.get_text_from_rank_id(self.value)} of {cardinfo.get_text_from_shape_id(self.shape)}s"

    def is_unknown(self):
        return self.shape == card_suit.UNKNOWN and self.value == card_rank.UNKNOWN

    def get_text_from_rank_id(id):
        match id:
            case card_rank.TWO:
                return "Two"
            case card_rank.THREE:
                return "Three"
            case card_rank.FOUR:
                return "Four"
            case card_rank.FIVE:
                return "Five"
            case card_rank.SIX:
                return "Six"
            case card_rank.SEVEN:
                return "Seven"
            case card_rank.EIGHT:
                return "Eight"
            case card_rank.NINE:
                return "Nine"
            case card_rank.TEN:
                return "Ten"
            case card_rank.A:
                return "Ace"
            case card_rank.J:
                return "Jack"
            case card_rank.Q:
                return "Queen"
            case card_rank.K:
                return "King"
            case card_rank.UNKNOWN:
                return "UNKNOWN"
            case _:
                raise "invalid id!"

    def get_text_from_shape_id(id):
        match id:
            case card_suit.CLUB:
                return "Club"
            case card_suit.DIAMOND:
                return "Diamond"
            case card_suit.HEART:
                return "Heart"
            case card_suit.SPADE:
                return "Spade"
            case card_suit.UNKNOWN:
                return "UNKNOWN"
            case _:
                raise "invalid id!"

class analysed_poker_card:
    def __init__(self, pts, card):
        self.points = pts
        self.card = card

    def __repr__(self):
        return "analysed: " + str(self.card)
        
class deck_of_cards:

    # clubs
    TWO_OF_CLUBS = cardinfo(card_suit.CLUB, card_rank.TWO)
    THREE_OF_CLUBS = cardinfo(card_suit.CLUB, card_rank.THREE)
    FOUR_OF_CLUBS = cardinfo(card_suit.CLUB, card_rank.FOUR)
    FIVE_OF_CLUBS = cardinfo(card_suit.CLUB, card_rank.FIVE)
    SIX_OF_CLUBS = cardinfo(card_suit.CLUB, card_rank.SIX)
    SEVEN_OF_CLUBS = cardinfo(card_suit.CLUB, card_rank.SEVEN)
    EIGHT_OF_CLUBS = cardinfo(card_suit.CLUB, card_rank.EIGHT)
    NINE_OF_CLUBS = cardinfo(card_suit.CLUB, card_rank.NINE)
    TEN_OF_CLUBS = cardinfo(card_suit.CLUB, card_rank.TEN)
    JACK_OF_CLUBS = cardinfo(card_suit.CLUB, card_rank.J)
    QUEEN_OF_CLUBS = cardinfo(card_suit.CLUB, card_rank.Q)
    KING_OF_CLUBS = cardinfo(card_suit.CLUB, card_rank.K)
    ACE_OF_CLUBS = cardinfo(card_suit.CLUB, card_rank.A)

    # diamonds
    TWO_OF_DIAMONDS = cardinfo(card_suit.DIAMOND, card_rank.TWO)
    THREE_OF_DIAMONDS = cardinfo(card_suit.DIAMOND, card_rank.THREE)
    FOUR_OF_DIAMONDS = cardinfo(card_suit.DIAMOND, card_rank.FOUR)
    FIVE_OF_DIAMONDS = cardinfo(card_suit.DIAMOND, card_rank.FIVE)
    SIX_OF_DIAMONDS = cardinfo(card_suit.DIAMOND, card_rank.SIX)
    SEVEN_OF_DIAMONDS = cardinfo(card_suit.DIAMOND, card_rank.SEVEN)
    EIGHT_OF_DIAMONDS = cardinfo(card_suit.DIAMOND, card_rank.EIGHT)
    NINE_OF_DIAMONDS = cardinfo(card_suit.DIAMOND, card_rank.NINE)
    TEN_OF_DIAMONDS = cardinfo(card_suit.DIAMOND, card_rank.TEN)
    JACK_OF_DIAMONDS = cardinfo(card_suit.DIAMOND, card_rank.J)
    QUEEN_OF_DIAMONDS = cardinfo(card_suit.DIAMOND, card_rank.Q)
    KING_OF_DIAMONDS = cardinfo(card_suit.DIAMOND, card_rank.K)
    ACE_OF_DIAMONDS = cardinfo(card_suit.DIAMOND, card_rank.A)

    # hearts
    TWO_OF_HEARTS = cardinfo(card_suit.HEART, card_rank.TWO)
    THREE_OF_HEARTS = cardinfo(card_suit.HEART, card_rank.THREE)
    FOUR_OF_HEARTS = cardinfo(card_suit.HEART, card_rank.FOUR)
    FIVE_OF_HEARTS = cardinfo(card_suit.HEART, card_rank.FIVE)
    SIX_OF_HEARTS = cardinfo(card_suit.HEART, card_rank.SIX)
    SEVEN_OF_HEARTS = cardinfo(card_suit.HEART, card_rank.SEVEN)
    EIGHT_OF_HEARTS = cardinfo(card_suit.HEART, card_rank.EIGHT)
    NINE_OF_HEARTS = cardinfo(card_suit.HEART, card_rank.NINE)
    TEN_OF_HEARTS = cardinfo(card_suit.HEART, card_rank.TEN)
    JACK_OF_HEARTS = cardinfo(card_suit.HEART, card_rank.J)
    QUEEN_OF_HEARTS = cardinfo(card_suit.HEART, card_rank.Q)
    KING_OF_HEARTS = cardinfo(card_suit.HEART, card_rank.K)
    ACE_OF_HEARTS = cardinfo(card_suit.HEART, card_rank.A)

    # spades
    TWO_OF_SPADES = cardinfo(card_suit.SPADE, card_rank.TWO)
    THREE_OF_SPADES = cardinfo(card_suit.SPADE, card_rank.THREE)
    FOUR_OF_SPADES = cardinfo(card_suit.SPADE, card_rank.FOUR)
    FIVE_OF_SPADES = cardinfo(card_suit.SPADE, card_rank.FIVE)
    SIX_OF_SPADES = cardinfo(card_suit.SPADE, card_rank.SIX)
    SEVEN_OF_SPADES = cardinfo(card_suit.SPADE, card_rank.SEVEN)
    EIGHT_OF_SPADES = cardinfo(card_suit.SPADE, card_rank.EIGHT)
    NINE_OF_SPADES = cardinfo(card_suit.SPADE, card_rank.NINE)
    TEN_OF_SPADES = cardinfo(card_suit.SPADE, card_rank.TEN)
    JACK_OF_SPADES = cardinfo(card_suit.SPADE, card_rank.J)
    QUEEN_OF_SPADES = cardinfo(card_suit.SPADE, card_rank.Q)
    KING_OF_SPADES = cardinfo(card_suit.SPADE, card_rank.K)
    ACE_OF_SPADES = cardinfo(card_suit.SPADE, card_rank.A)