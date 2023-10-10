import cv2
import numpy as np
from os import listdir
from os.path import isfile, join, isdir
from poker_card import cardshape, cardvalue

class poker_ocr():
    """
    An improvised OCR class for identifying Values and Shapes specifically
    for bicycle type cards.
    """

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
            "R0.jpg": cardvalue.TEN,
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
        # set values and its default values
        self.__sample_path = sample_path + "/"
        self.__rank_comparer_list = []
        self.__shape_comparer_list = []
        self.__inited = False

    def initialize(self):
        
        # check if folder exists
        if not(isdir(self.__sample_path)):
            raise f"Path '{self.__sample_path}' does not exist!"

        # initialize images
        img_rank_list = [f for f in listdir(self.__sample_path) if len(f) == 6 and f[0] == "R" and f.endswith("jpg") and isfile(join(self.__sample_path, f))]
        img_shape_list = [f for f in listdir(self.__sample_path) if len(f) == 6 and f[0] == "S" and f.endswith("jpg") and isfile(join(self.__sample_path, f))]

        # deck of cards has only 13 values
        if len(img_rank_list) != 13:
            raise "Image rank list must be exactly 13!"
        
        # deck of cards has only 4 shapes
        if len(img_shape_list) != 4:
            raise "Image shape list must be exactly 4!"
        
        # convert filename for rank type cards to card id
        for r in img_rank_list:
            if r not in self.file_dict_id:
                raise f"file {r} does not have any entry in id dictionary!"

            # create image comparer andadd it to comparer list
            rank_img_comparer = self.__create_image_comparer(self.__sample_path + r, self.file_dict_id[r])
            self.__rank_comparer_list.append(rank_img_comparer)

        # convert filename for shape type cards to card id
        for s in img_shape_list:
            if s not in self.file_dict_id:
                raise f"file {s} does not have any entry in id dictionary!"
            
            # create image comparer andadd it to comparer list
            shape_img_comparer = self.__create_image_comparer(self.__sample_path + s, self.file_dict_id[s])
            self.__shape_comparer_list.append(shape_img_comparer)

        # set value to true to indicate that we have initialized the class
        self.__inited = True

    def scan_rank(self, input_img):
        # check if class is initialized
        if not(self.__inited):
            raise "To use this function, please initialize the class."

        lowest_score_item = min(self.__rank_comparer_list, key= lambda c: c.get_score(input_img))
        return lowest_score_item.id
    
    def scan_shape(self, input_img):
        # check if class is initialized
        if not(self.__inited):
            raise "To use this function, please initialize the class."
        
        lowest_score_item = min(self.__shape_comparer_list, key= lambda c: c.get_score(input_img))
        return lowest_score_item.id

    # private functions
    def __create_image_comparer(self, file, id):
        # read greyscale image
        loaded_image = cv2.imread(file, 0)
        return poker_ocr_comparer(loaded_image, id)

class poker_ocr_comparer():

    def __init__(self, loaded_image, id):
        self.image = loaded_image
        self.id = id

    def get_score(self, input_image):
        # comparison technique
        diff_img = cv2.absdiff(input_image, self.image)
        diff_score = int(np.sum(diff_img)/255)
        return diff_score
