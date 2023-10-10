from poker_card import cardvalue

def cluster_cards_by_shape(card_list, find_len = 5, limit = True):

    # temporary dict to store clustered values
    shape_dict = {}
    for c in card_list:
        # initialize list if shape is not in dict yet
        if c.shape not in shape_dict:
            shape_dict[c.shape] = []

        # add current value to shape group
        if limit and len(shape_dict[c.shape]) >= find_len:
            continue

        shape_dict[c.shape].append(c)

    # look for group that has `find_len` cards in a shape
    tmp_list = [shape_dict[g] for g in shape_dict if len(shape_dict[g]) >= find_len]

    # return none if list is empty
    if len(tmp_list) > 0:
        return tmp_list
    
def cluster_cards_by_value(card_list, find_len = 4, limit = True):

    # temporary dict to store clustered values
    value_dict = {}
    for c in card_list:
        # initialize list if value is not in dict yet
        if c.value not in value_dict:
            value_dict[c.value] = []

        # add current value to value group
        if limit and len(value_dict[c.value]) >= find_len:
            continue
        
        value_dict[c.value].append(c)

    # look for group that has `find_len` cards in a value
    tmp_list = [value_dict[g] for g in value_dict if len(value_dict[g]) >= find_len]

    # return none if list is empty
    if len(tmp_list) > 0:
        return tmp_list

def get_shapes_only(card_list):
    return [c.shape for c in card_list]

def get_values_only(card_list):
    return [c.value for c in card_list]

# structure of base class for hand type detection
class detector_base:
    def __init__(self, pattern_name):
        self.pattern_name = pattern_name
    
    def detect(self, cardinfo_z):
        return False
    
class detect_royal_flush(detector_base):
    # constants
    ROYAL_FLUSH_PATTERN = [cardvalue.A, cardvalue.K, cardvalue.Q, cardvalue.J, cardvalue.TEN]

    def __init__(self):
        super().__init__("Royal flush")
        
    def detect(self, cardinfo_z):
        # only get card shapes if card value is in royal flush pattern
        valid_value_cards_shape = [c.shape for c in cardinfo_z if c.value in detect_royal_flush.ROYAL_FLUSH_PATTERN]

        # if card shapes count is less than 5, we return false
        if len(valid_value_cards_shape) < 5:
            return False
        
        # check if all the collected shapes are all the same
        return len(set(valid_value_cards_shape)) == 1
    
class detect_flush(detector_base):
    def __init__(self):
        super().__init__("Flush")

    def detect(self, cardinfo_z):
        clustered_cards = cluster_cards_by_shape(cardinfo_z)
        return clustered_cards != None
    
class detect_four_of_a_kind(detector_base):
    def __init__(self):
        super().__init__("Four of a kind")

    def detect(self, cardinfo_z):
        # find at least 1 four cards in a group
        clustered_values = cluster_cards_by_value(cardinfo_z, 4)
        return clustered_values != None
    
class detect_three_of_a_kind(detector_base):
    def __init__(self):
        super().__init__("Three of a kind")

    def detect(self, cardinfo_z):
        # find at least 1 three cards in a group
        three_item_group = cluster_cards_by_value(cardinfo_z, 3)
        return three_item_group != None

class detect_full_house(detector_base):
    def __init__(self):
        super().__init__("Full house")

    def detect(self, cardinfo_z):
        # detect all cards in same group that has 2 or more items
        two_item_group = cluster_cards_by_value(cardinfo_z, 2, False)
        if two_item_group == None:
            return False
        
        # get groups that has three or more cards
        three_card_group = [t for t in two_item_group if len(t) >= 3]
        if len(three_card_group) == 0:
            return False
        elif len(three_card_group) >= 2:
            return True
        
        # get card group that has only 2 items
        two_card_group =  [t for t in two_item_group if t not in three_card_group]
        return len(two_card_group) > 0
    
class detect_two_pair(detector_base):
    def __init__(self):
        super().__init__("Two pair")

    def detect(self, cardinfo_z):
        # look for pairs
        two_item_group = cluster_cards_by_value(cardinfo_z, 2)

        # check if we have two or more pairs
        return two_item_group != None and len(two_item_group) >= 2

class detect_pair(detector_base):
    def __init__(self):
        super().__init__("One pair")

    def detect(self, cardinfo_z):
        # look for pairs
        two_item_group = cluster_cards_by_value(cardinfo_z, 2)

        # we only need at least 1 result for valid result
        return two_item_group != None

class detect_straight(detector_base):
    def __init__(self):
        super().__init__("Straight")

    def detect(self, cardinfo_z):
        # sort cards first
        sorted_cards = sorted(cardinfo_z, key= lambda x: x.value)

        result_list = []
        tmp_list = []
        for i in range(len(sorted_cards)):
            tmp_list.append(sorted_cards[i])

            # reset counter if current card + 1 does not match expected card
            if i + 1 < len(sorted_cards) and sorted_cards[i].value + 1 == sorted_cards[i + 1].value:
                continue
            
            # append to result if next card is not the expected card
            result_list.append(tmp_list)
            tmp_list = []
        
        # check how many cards have 5 or more consecutive numbers
        count_result = sum(len(r) >= 5 for r in result_list)
        return count_result == 1
    
class detect_straight_flush(detector_base):
    def __init__(self):
        super().__init__("Straight flush")

    def detect(self, cardinfo_z):
        # sort cards first
        sorted_cards = sorted(cardinfo_z, key= lambda x: x.value)

        result_list = []
        tmp_list = []
        for i in range(len(sorted_cards)):
            tmp_list.append(sorted_cards[i])

            # reset counter if current card + 1 does not match expected card
            if i + 1 < len(sorted_cards) and sorted_cards[i].value + 1 == sorted_cards[i + 1].value:
                continue
            
            # append to result if next card is not the expected card
            result_list.append(tmp_list)
            tmp_list = []
        
        # check how many cards have 5 or more consecutive numbers
        five_cons_group = [r for r in result_list if len(r) >= 5]
        if len(five_cons_group) > 0:
            shape_list = [sh.shape for sh in five_cons_group[0]] # it is impossible to have more than 1 five 5 group
            return len(set(shape_list)) == 1 

        return False