import cv2
import numpy as np
from os import listdir
from os.path import isfile, join, isdir
from poker_card import cardshape, cardvalue

class poker_ocr():
    file_dict_id = {
            #ranks
            "R2.jpg": cardvalue.TWO,
            "R3.jpg": cardvalue.THREE,
            "R4.jpg": cardvalue.FOUR,
            "R5.jpg": cardvalue.FIVE,
            "R6.jpg": cardvalue.SIX,
            "R7.jpg": cardvalue.SEVEN,
            "R8.jpg": cardvalue.EIGHT,
            "R9.jpg": cardvalue.NINE,
            "R10.jpg": cardvalue.TEN,
            "RA.jpg": cardvalue.A,
            "RJ.jpg": cardvalue.J,
            "RK.jpg": cardvalue.K,
            "RQ.jpg": cardvalue.Q,

            #shapes
            "SC.jpg": cardshape.CLUB,
            "SD.jpg": cardshape.DIAMOND,
            "SH.jpg": cardshape.HEART,
            "SS.jpg": cardshape.SPADE,
    }

    def __init__(self, sample_path):
        self.sample_path = sample_path + "/"
        self.rank_comparer_list = []
        self.shape_comparer_list = []

    def initialize(self):
        
        if not(isdir(self.sample_path)):
            raise f"Path '{self.sample_path}' does not exist!"

        # initialize images
        img_rank_list = [f for f in listdir(self.sample_path) if len(f) == 6 and f[0] == "R" and f.endswith("jpg") and isfile(join(self.sample_path, f))]
        img_shape_list = [f for f in listdir(self.sample_path) if len(f) == 6 and f[0] == "S" and f.endswith("jpg") and isfile(join(self.sample_path, f))]

        if len(img_rank_list) != 12:
            raise "Image rank list must be exactly 12!"
        
        if len(img_shape_list) != 4:
            raise "Image shape list must be exactly 4!"
        
        for r in img_rank_list:
            if r not in self.file_dict_id:
                raise f"file {r} does not have any entry in id dictionary!"

            rank_img_comparer = self.__create_image_comparer(self.sample_path + r, self.file_dict_id[r])
            self.rank_comparer_list.append(rank_img_comparer)

        for s in img_shape_list:
            if s not in self.file_dict_id:
                raise f"file {s} does not have any entry in id dictionary!"
            
            shape_img_comparer = self.__create_image_comparer(self.sample_path + s, self.file_dict_id[s])
            self.shape_comparer_list.append(shape_img_comparer)

    def scan_rank(self, input_img):
        lowest_score_item = min(self.rank_comparer_list, key= lambda c: c.get_score(input_img))
        return lowest_score_item.id
    
    def scan_shape(self, input_img):
        lowest_score_item = min(self.shape_comparer_list, key= lambda c: c.get_score(input_img))
        return lowest_score_item.id

    def __create_image_comparer(self, file, id):
        loaded_image = cv2.imread(file, 0)
        return poker_ocr_comparer(loaded_image, id)

class poker_ocr_comparer():

    def __init__(self, loaded_image, id):
        self.image = loaded_image
        self.id = id

    def get_score(self, input_image):
        diff_img = cv2.absdiff(input_image, self.image)
        diff_score = int(np.sum(diff_img)/255)
        return diff_score
