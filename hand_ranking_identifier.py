from poker_card import cardvalue

def cluster_cards_by_shape(card_list, find_len = 5):

    # temporary dict to store clustered values
    shape_dict = {}
    for c in card_list:
        # initialize list if shape is not in dict yet
        if card_list.shape not in shape_dict:
            shape_dict[card_list.shape] = []

        # add current value to shape group
        shape_dict[card_list.shape].append(c)

    # look for group that has `find_len` cards in a shape
    tmp_list = [shape_dict[g] for g in shape_dict if len(shape_dict[g]) == find_len]
    if len(tmp_list) > 0:
        return tmp_list
    
def cluster_cards_by_value(card_list, find_len = 4):

    # temporary dict to store clustered values
    value_dict = {}
    for c in card_list:
        # initialize list if value is not in dict yet
        if card_list.value not in value_dict:
            value_dict[card_list.value] = []

        # add current value to value group
        value_dict[card_list.value].append(c)

    # look for group that has `find_len` cards in a value
    tmp_list = [value_dict[g] for g in value_dict if len(value_dict[g]) == find_len]
    if len(tmp_list) > 0:
        return tmp_list

class detector_base:
    def __init__(self, pattern_name):
        self.pattern_name = pattern_name
    
    def detect(self, arr_card_info):
        return False
    
class detect_royal_flush(detector_base):
    def __init__(self):
        super().__init__("Royal Flush")
        
    def detect(self, cardinfo_z):
        royalFlush = [cardvalue.A, cardvalue.K, cardvalue.Q, cardvalue.J, cardvalue.TEN]
        valid_value_cards_shape = [c.shape for c in cardinfo_z if c.value in royalFlush]
        if len(valid_value_cards_shape) < 5:
            return False
        
        return len(set(valid_value_cards_shape)) == 1
    
class detect_flush(detector_base):
    def __init__(self):
        super().__init__("Flush")

    def detect(self, cardinfo_z):
        if len(cardinfo_z) > 5:
            cardinfo_z = cluster_cards_by_shape(cardinfo_z)

        # check if it's none
        if cardinfo_z == None:
            return False

        return len(set(cardinfo_z[0])) == 1
    
class detect_four_of_a_kind(detector_base):
    def __init__(self):
        super().__init__("Four of a kind")

    def detect(self, cardinfo_z):
        clustered_values = cluster_cards_by_value(cardinfo_z, 4)

        # check if it's none
        if clustered_values == None:
            return False

        return len(set(clustered_values[0])) == 1
    
class detect_three_of_a_kind(detector_base):
    def __init__(self):
        super().__init__("Three of a kind")

    def detect(self, cardinfo_z):
        three_item_group = cluster_cards_by_value(cardinfo_z, 3)

        if three_item_group == None:
            return False
        
        # check if all the group result has 3 same card values
        three_item_group_result = sum([len(set(t1)) == 1 for t1 in three_item_group]) >= 1
        return three_item_group_result

class detect_full_house(detector_base):
    def __init__(self):
        super().__init__("Full house")

    def detect(self, cardinfo_z):
        two_item_group = cluster_cards_by_value(cardinfo_z, 2)
        three_item_group = cluster_cards_by_value(cardinfo_z, 3)

        # check if any cluster is none
        if two_item_group == None or three_item_group == None:
            return False

        # check if all the two item group result has at least one pair
        two_item_group_result = sum([len(set(t1)) == 1 for t1 in two_item_group]) > 0
        
        # check if both group has same card values
        return two_item_group_result and len(set(three_item_group[0])) == 1 
    
class detect_two_pair(detector_base):
    def __init__(self):
        super().__init__("Two pair")

    def detect(self, cardinfo_z):
        two_item_group = cluster_cards_by_value(cardinfo_z, 2) #two groups
        
        if two_item_group == None:
            return False
        
        # check if all the group result has more than one pair (2 pairs)
        two_item_group_result = sum([len(set(t1)) == 1 for t1 in two_item_group]) >= 2 #two pair
        return two_item_group_result 

class detect_pair(detector_base):
    def __init__(self):
        super().__init__("One pair")

    def detect(self, cardinfo_z):
        two_item_group = cluster_cards_by_value(cardinfo_z, 2) #two groups
        
        if two_item_group == None:
            return False
        
        # check if all the group result has more than one pair (2 pairs)
        two_item_group_result = sum([len(set(t1)) == 1 for t1 in two_item_group]) >= 1 #one pair
        return two_item_group_result 
    