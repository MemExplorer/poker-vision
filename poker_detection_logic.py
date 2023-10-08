from poker_card import cardvalue, cardshape, cardinfo

class cardinfo:
    def __init__(self, shape, value):
        self.shape = shape
        self.value = value
    def __eq__(self, c):
        return self.shape == c.shape and self.value == c.value
        
class detector_base:
    def __init__(self, pattern_name):
        self.pattern_name = pattern_name
    
    def detect(self, cardinfo_z) -> bool:
        return False
        


class detect_royal_flush(detector_base): #First Rank
    def __init__(self):
        super().__init__("Royal Flush")
        
    def detect(self, cardinfo_z) -> bool:
        royalFlush = sorted([cardvalue.A, cardvalue.K, cardvalue.Q, cardvalue.J, cardvalue.TEN])
        
        shape_list = [c.shape for c in cardinfo_z]
        value_list = [c.value for c in cardinfo_z]
        
        sorted_vl = sorted(set(value_list))
        last_five = sorted_vl[-5:]

        if len(set(shape_list)) != 1:
            return False
            
        if royalFlush == last_five:
            return True
        
        return False

class detect_straight_flush(detector_base): #Second Rank
    def __init__(self):
        super().__init__("Straight Flush")
    
    def detect(self, cardinfo_z) -> bool:
        straightflush = []
        
        for start_value in range(cardvalue.TWO, cardvalue.A - 3):
            straightflush_values = [start_value + i for i in range(5)]
            straightflush.append(straightflush_values)

        shape_list = [c.shape for c in cardinfo_z]
        value_list = [c.value for c in cardinfo_z]
        
        sorted_vl = sorted(set(value_list))
        first_five = sorted_vl[:5]
        
        if len(set(shape_list)) != 1:
            return False
            
        for v in straightflush:
            if v == first_five:
                return True
        
        return False

class detect_straight(detector_base): #Sixth Rank
    def __init__(self):
        super().__init__("Straight")
    
    def detect(self, cardinfo_z) -> bool:
        straight = []
        
        for start_value in range(cardvalue.TWO, cardvalue.A - 3):
            straight_values = [start_value + i for i in range(5)]
            straight.append(straight_values)

        shape_list = [c.shape for c in cardinfo_z]
        value_list = [c.value for c in cardinfo_z]
        
        sorted_vl = sorted(set(value_list))
        first_five = sorted_vl[:5]
        
        if len(set(shape_list)) != 1:   
            for v in straight:
                if v == first_five:
                    return True
        
        return False


        
class detect_high_card(detector_base): #Lowest Rank
    def __init__(self):
        super().__init__("High Card")
    
    def detect(self, cardinfo_z):
        value_order = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        highest_card = max(cardinfo_z, key=lambda card: card.value)

        if 0 <= highest_card.value < len(value_order):
            highcard_name = value_order[highest_card.value]

        return highcard_name


#Test Inputs
# card_arr = [cardinfo(cardshape.CLUB, cardvalue.TWO), cardinfo(cardshape.CLUB, cardvalue.THREE), 
# cardinfo(cardshape.CLUB, cardvalue.FOUR), cardinfo(cardshape.CLUB, cardvalue.FIVE), 
# cardinfo(cardshape.CLUB, cardvalue.SIX),cardinfo(cardshape.CLUB, cardvalue.EIGHT),cardinfo(cardshape.CLUB, cardvalue.NINE)]

# card_arr = [cardinfo(cardshape.CLUB, cardvalue.K), cardinfo(cardshape.CLUB, cardvalue.THREE), 
# cardinfo(cardshape.CLUB, cardvalue.FOUR), cardinfo(cardshape.CLUB, cardvalue.FIVE), 
# cardinfo(cardshape.CLUB, cardvalue.SIX)]
      
card_arr = [cardinfo(cardshape.CLUB, cardvalue.A), cardinfo(cardshape.CLUB, cardvalue.K), 
cardinfo(cardshape.CLUB, cardvalue.Q), cardinfo(cardshape.CLUB, cardvalue.J), 
cardinfo(cardshape.CLUB, cardvalue.TEN)] #Royal Flush


detection_royalflush = detect_royal_flush()
detection_straightflush = detect_straight_flush()
detection_straight = detect_straight()
detection_highcard = detect_high_card()


result_royalflush = detection_royalflush.detect(card_arr)
result_straightflush = detection_straightflush.detect(card_arr)
result_straight = detection_straight.detect(card_arr)
result_highcard = detection_highcard.detect(card_arr)


print("Royal House? :", result_royalflush)
print("Straight Flush? :", result_straightflush)
print("Straight? :", result_straight)
print("High Card:", result_highcard)

# card_values = [cardinfo.value for cardinfo in card_arr]
# sort_card_values = sorted(card_values)
# print(sort_card_values)

