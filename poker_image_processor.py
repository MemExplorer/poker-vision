import cv2
import numpy as np
from functools import cmp_to_key

#constants
CARD_MAX_AREA = 10000000
CARD_MIN_AREA = 15000

def flattener(image, pts, w, h):
    """Flattens an image of a card into a top-down 200x300 perspective.
    Returns the flattened, re-sized, grayed image.
    See www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/"""
    temp_rect = np.zeros((4,2), dtype = "float32")
    
    s = np.sum(pts, axis = 2)

    tl = pts[np.argmin(s)]
    br = pts[np.argmax(s)]

    diff = np.diff(pts, axis = -1)
    tr = pts[np.argmin(diff)]
    bl = pts[np.argmax(diff)]

    # Need to create an array listing points in order of
    # [top left, top right, bottom right, bottom left]
    # before doing the perspective transform

    if w <= 0.8*h: # If card is vertically oriented
        temp_rect[0] = tl
        temp_rect[1] = tr
        temp_rect[2] = br
        temp_rect[3] = bl

    if w >= 1.2*h: # If card is horizontally oriented
        temp_rect[0] = bl
        temp_rect[1] = tl
        temp_rect[2] = tr
        temp_rect[3] = br

    # If the card is 'diamond' oriented, a different algorithm
    # has to be used to identify which point is top left, top right
    # bottom left, and bottom right.
    
    if w > 0.8*h and w < 1.2*h: #If card is diamond oriented
        # If furthest left point is higher than furthest right point,
        # card is tilted to the left.
        if pts[1][0][1] <= pts[3][0][1]:
            # If card is titled to the left, approxPolyDP returns points
            # in this order: top right, top left, bottom left, bottom right
            temp_rect[0] = pts[1][0] # Top left
            temp_rect[1] = pts[0][0] # Top right
            temp_rect[2] = pts[3][0] # Bottom right
            temp_rect[3] = pts[2][0] # Bottom left

        # If furthest left point is lower than furthest right point,
        # card is tilted to the right
        if pts[1][0][1] > pts[3][0][1]:
            # If card is titled to the right, approxPolyDP returns points
            # in this order: top left, bottom left, bottom right, top right
            temp_rect[0] = pts[0][0] # Top left
            temp_rect[1] = pts[3][0] # Top right
            temp_rect[2] = pts[2][0] # Bottom right
            temp_rect[3] = pts[1][0] # Bottom left
            
        
    maxWidth = w
    maxHeight = h

    # Create destination array, calculate perspective transform matrix,
    # and warp card image
    dst = np.array([[0,0],[maxWidth-1,0],[maxWidth-1,maxHeight-1],[0, maxHeight-1]], np.float32)
    M = cv2.getPerspectiveTransform(temp_rect,dst)
    warp = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    return warp

def process_card_image(image):
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)

    #separate foreground objects from background
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

    return thresh

def contour_sort(a, b):

    br_a = cv2.boundingRect(a)
    br_b = cv2.boundingRect(b)

    if abs(br_a[1] - br_b[1]) <= 15:
        return br_a[0] - br_b[0]

    return br_a[1] - br_b[1]


def get_card_contours(thresh):
    cnts, hier = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    half = cv2.boundingRect(thresh)[2] * 0.6
    valid_conts = []
    for i in range(len(cnts)):
        size = cv2.contourArea(cnts[i])
        peri = cv2.arcLength(cnts[i],True)
        approx = cv2.approxPolyDP(cnts[i],0.01*peri,True)
        
        if ((size < CARD_MAX_AREA) and (size > CARD_MIN_AREA)
            and (len(approx) == 4) and  cv2.boundingRect(cnts[i])[2] < half):
            valid_conts.append(cnts[i])

    #sort the detected cards by their area in descending order
    valid_conts.sort(key=lambda x: cv2.contourArea(x), reverse=True)

    valid_conts2 = []
    #iterate through the sorted cards and exclude detection inside another detection
    for i, card in enumerate(valid_conts):
        is_inside = False
        for j, other_card in enumerate(valid_conts):
            if i != j:
                ptt = tuple([int(round(card[0][0][0])), int(round(card[0][0][1]))])
                result = cv2.pointPolygonTest(other_card, ptt, False)
                if result == 1:
                    is_inside = True
                    break
        if not is_inside:
            valid_conts2.append(card)

    # sort cards from top, left to right, then botton, left to right
    return sorted(valid_conts2, key=cmp_to_key(contour_sort))

def get_contour_points(contour):
    #find perimeter of card and use it to approximate corner points
    peri = cv2.arcLength(contour,True)
    approx = cv2.approxPolyDP(contour,0.01*peri,True)
    pts = np.float32(approx)
    return pts

def flatten_perspective_transform(contour, image):
    pts = get_contour_points(contour)
    c = cv2.boundingRect(contour)
    flattened_image = flattener(image, pts, c[2], c[3])
    return flattened_image

def remove_spaces(image):
    #find the largest contour
    card_rank_contours = cv2.findContours(image, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[0]

    #sort to get the highest value at first index
    card_rank_contours = sorted(card_rank_contours, key=cv2.contourArea,reverse=True)

    #return something if we find any contours
    if len(card_rank_contours) != 0:
        x1,y1,w1,h1 = cv2.boundingRect(card_rank_contours[0])
        cropped_object = image[y1:y1+h1, x1:x1+w1]
        resized_picture = cv2.resize(cropped_object, (70, 125), 0, 0)
        return resized_picture

def get_corner_info_image(flattened_img):

    #crop card info part of the card
    x,y,w,h = cv2.boundingRect(flattened_img)
    y_percent = 0.26
    x_percent = 0.15
    c_width = int(w * x_percent)
    cropped_info = flattened_img[y:y+int(h * y_percent), x:x+c_width]
    resized_card_info_img = cv2.resize(cropped_info, (0,0), fx=4, fy=4)

    #update values to calculate card info image size
    x,y,w,h = cv2.boundingRect(resized_card_info_img)
    cent_y = int(h * 0.5)

    #get thresh level
    white_level = resized_card_info_img[15,int((c_width*4)/2)]
    thresh_level = white_level - 60
    if (thresh_level <= 0):
        thresh_level = 1

    blur = cv2.GaussianBlur(resized_card_info_img,(3,3),0)
    rank_threshed = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 27, 5)
    val_threshed = cv2.threshold(resized_card_info_img, thresh_level, 255, cv2.THRESH_BINARY_INV)[1]
    
    #split card symbol and value
    card_rank_img = remove_spaces(rank_threshed[10:cent_y + 10, 0:w])
    card_val_img = remove_spaces(val_threshed[cent_y:cent_y + (h - cent_y), 0:w])

    # small hack to fix detection issues
    if card_val_img is None:
        card_val_img = remove_spaces(rank_threshed[cent_y:cent_y + (h - cent_y), 0:w])

    return (card_rank_img, card_val_img)