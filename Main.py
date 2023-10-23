import cv2
import poker_image_processor as ip
import cv2utils
from poker_ocr_engine import poker_ocr
from poker_card import cardinfo, analysed_poker_card, deck_of_cards
import hand_ranking_identifier as hid
import numpy as np
from os import listdir
from os.path import isfile, join, isdir

detector_list = [
    hid.detect_royal_flush(),
    hid.detect_straight_flush(),
    hid.detect_four_of_a_kind(),
    hid.detect_full_house(),
    hid.detect_flush(),
    hid.detect_straight(),
    hid.detect_three_of_a_kind(),
    hid.detect_two_pair(),
    hid.detect_pair()
]

def detect_hand_ranking(dealer_cards, player_cards = []):
    merged_list = dealer_cards + player_cards
    for d in detector_list:
        if d.detect(merged_list):
            return d.pattern_name
    return "High card"

def get_dealer_cards(grouped_cards):
    if len(grouped_cards) == 1:
        return (grouped_cards[0], True)
    
    for g in grouped_cards:
        if len(g) == 5:
            return (g, False)
        
    return (None, None)
        
def get_player_cards(grouped_cards):
    valid_list = []
    for g in grouped_cards:
        if len(g) == 2:
            valid_list.append(g)

    return valid_list

def unique_count_app(a):
    colors, count = np.unique(a.reshape(-1,a.shape[-1]), axis=0, return_counts=True)
    return colors[count.argmax()]
def find_dominant_color(a):
    x, y, w, h = cv2.boundingRect(cv2.cvtColor(a,cv2.COLOR_BGR2GRAY))
    crop_mid = a[x: x + (w//2),y: y + (h//2)]
    pix = cv2.resize(crop_mid, (1,1))[0][0].tolist()
    pix.reverse()
    return pix

def analyse_card(ocr_engine, image, card_contour):

    # flatten and change card perspective first
    fl = ip.flatten_perspective_transform(card_contour, image)
    dominant_color = find_dominant_color(fl)
    pts = ip.get_contour_points(card_contour)

    #if (dominant_color[0] >= 165 and dominant_color[0] <= 210) and (dominant_color[1] >= 80 and dominant_color[1] <= 140) and (dominant_color[2] >= 100 and dominant_color[2] <= 150):
    # detect the back color of the card
    if (dominant_color[0] >= 165 and dominant_color[0] <= 210) and (dominant_color[1] >= 80 and dominant_color[1] <= 130) and (dominant_color[2] >= 100 and dominant_color[2] <= 140):
        return analysed_poker_card(pts, cardinfo(4, 13)) #return unknown card

    # get corner info
    rank_img, val_img = ip.get_corner_info_image(cv2.cvtColor(fl, cv2.COLOR_BGR2GRAY))
    if rank_img is None or val_img is None:
        return
    
    shape = ocr_engine.scan_shape(val_img)
    rank = ocr_engine.scan_rank(rank_img)

    # create analysed card info
    card = cardinfo(shape, rank)
    return analysed_poker_card(pts, card)

def detect_cards_from_image(ocr, image):

    # do necessary transformation to image to extract card contours
    thresh = ip.process_card_image(image)
    conts = ip.get_card_contours(thresh)

    if len(conts) == 0:
        return
    
    # cluster nearest cards
    grouped_near_cards = cv2utils.group_near_cards(image, conts)

    dealer_img_cards, is_one = get_dealer_cards(grouped_near_cards)
    player_img_cards = get_player_cards(grouped_near_cards)

    print(f"Group: {len(grouped_near_cards)}")
    print(f"Dealer: {len([] if dealer_img_cards is None else dealer_img_cards)}, Player: {len(player_img_cards)}")
    # check if we have a dealer
    if dealer_img_cards == None:
        return
    
    # check if there is no player
    if is_one:
        player_img_cards = []
    
    # analyse and process dealer card images
    analysed_dealer_cards =  [analyse_card(ocr, image, c) for c in dealer_img_cards]
    if analysed_dealer_cards.count(None) > 0:
        return

    dealer_cards = [c.card for c in analysed_dealer_cards if not(c.card.is_unknown())]
    cv2utils.highlight_card_list(image, analysed_dealer_cards)
    cv2utils.highlight_grouped_cards(image, dealer_img_cards, "Dealer")

    # analyse and process card images of each player
    for p in range(len(player_img_cards)):
        analysed_player_cards = [analyse_card(ocr, image, c) for c in player_img_cards[p]]
        if any(i is None for i in analysed_player_cards):
            continue
        player_cards = [c.card for c in analysed_player_cards if not(c.card.is_unknown())]
        cv2utils.highlight_card_list(image, analysed_player_cards)
        ranking = "Unknown" if len(player_cards) < 2 else detect_hand_ranking(dealer_cards, player_cards)
        cv2utils.highlight_grouped_cards(image, player_img_cards[p], f"Player {p + 1} ({ranking})")

def get_available_camera_devices():
    index = 0
    cam_list = []
    while True:
        cap = cv2.VideoCapture(index)
        if not cap.read()[0]:
            break
        else:
            cam_list.append(index)
        cap.release()
        index += 1
    return cam_list


def test_cam(ocr):

    # get available camera devices
    cam_devices = get_available_camera_devices()
    if len(cam_devices) == 0:
        print("You have no available camera device!")
        return
    
    # select available camera devices
    print("Available devices: ")
    for i in range(len(cam_devices)):
        print(str(i + 1) + ": " + str(cam_devices[i]))

    sel_index = 0
    while(True):
        cam_index = input("Select Camera: ")
        if cam_index.isnumeric() and (int(cam_index) > 0 and int(cam_index) <= len(cam_devices)):
            sel_index = int(cam_index)
            break

    # initialize camera device
    cap = cv2utils.ThreadedCamera(cam_devices[sel_index - 1])

    while True:
        frame = cap.grab_frame()
        if frame is None:
            continue
        
        # highlight cards
        detect_cards_from_image(ocr, frame)
        cv2.imshow('frame', frame)
        if cv2.waitKey(144) & 0xFF == ord('q'):
            break

def edit_video(ocr, vid_path):
    source = cv2.VideoCapture(vid_path)  
    source.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    source.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)          

    # iterate through all the frames if the video clip present
    while(source.isOpened()):                                                                                                                                                 
        #read the frame
        ret, frame = source.read()

        detect_cards_from_image(ocr, frame)                                                                                                                                                    
        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break                                                                                                                                  
    print("Done")

def test_image(ocr):
    # img_path = "test_data/royalflush_ace/IMG20231006142219.jpg"
    # img_path = "test_data/tilted/IMG20231007175210.jpg"
    img_path = "test_data/card_rankings/"
    files = [f for f in listdir(img_path) if f.endswith("jpg") and isfile(join(img_path, f))]
    for f in files:
        image = cv2.imread(img_path + f)
        image = cv2.resize(image, (1920, 1080))
        detect_cards_from_image(ocr, image)
        cv2utils.show_image(image, f)
    #cv2.imwrite("test.jpg", image)

def main():
    ocr = poker_ocr("training")
    ocr.initialize()
    test_cam(ocr)
    #test_image(ocr)
    #edit_video(ocr, "VID20231009234753.mp4")


if __name__ == "__main__":
    main()
