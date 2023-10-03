from poker_card import cardvalue

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
        
        shape_list = [c.shape for c in cardinfo_z]
        
        if len(set(shape_list)) != 1:
            return False
            
        for v in range(len(cardinfo_z)):
            if cardinfo_z[v].value not in royalFlush:
                return False
        
        return True