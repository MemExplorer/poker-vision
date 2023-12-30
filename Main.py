import cv2
import poker_image_processor as ip
import cv2utils
from poker_card import cardinfo, analysed_poker_card, card_suit_from_yolo, card_rank_from_yolo
import hand_ranking_identifier as hid
import numpy as np
from ultralytics import YOLO

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

def read_corner_info_pred(c, yolo_result):
    yolo_labels = []
    for b in yolo_result.boxes:
        cont_label = yolo_result.names[int(b.cls)]
        yolo_labels.append(cont_label)
    if len(yolo_labels) > 2 or len(yolo_labels) < 2:
        return (None, None)
    
    yolo_labels.sort(key=lambda x: len(x))
    if len(yolo_labels[0]) != 1:
        return (None, None)
    return card_rank_from_yolo(yolo_labels[0]), card_suit_from_yolo(yolo_labels[1])


def analyse_card(ocr_engine, image, card_contour):

    # flatten and change card perspective first
    fl = ip.flatten_perspective_transform(image, card_contour)
    if(card_contour.label == "card back"):
        return analysed_poker_card(card_contour.contour, cardinfo(4, 13)) #return unknown card

    # get corner info
    img_corner = ip.get_corner_info_image(cv2.cvtColor(fl, cv2.COLOR_BGR2GRAY))
    corner_info_pred = ocr_engine(cv2.cvtColor(img_corner, cv2.COLOR_GRAY2BGR), conf=0.5)
    card_rank, card_suit = read_corner_info_pred(img_corner, corner_info_pred[0])
    if card_rank is None:
        return

    # create analysed card info
    card = cardinfo(card_suit, card_rank)
    return analysed_poker_card(card_contour.contour, card)

class yolo_contour:
        def __init__(self, label, contour, w, h):
            self.label = label
            self.contour = contour
            self.width = w
            self.height = h

def get_contours_from_yolo(yolo_result):
        yolo_conts = []
        for b in yolo_result.boxes:
            x1, y1, x2, y2 = [int(z) for z in b.xyxy[0]]
            pts = np.array([[(x1, y1)], [(x1, y2)], [(x2, y2)], [(x2, y1)]])
            cont_label = yolo_result.names[int(b.cls)]
            yolo_conts.append(yolo_contour(cont_label, pts, x2 - x1, y2 - y1))
        return yolo_conts

def detect_cards_from_image(ocr, card_detector, image):
    detection_result = card_detector(image, conf=0.5)
    yolo_conts = get_contours_from_yolo(detection_result[0])
    yolo_conts = ip.sort_cards(yolo_conts)
    # cluster nearest cards
    grouped_near_cards = cv2utils.group_near_cards(image, yolo_conts)

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


def test_cam(ocr, card_detector):

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
        detect_cards_from_image(ocr, card_detector, frame)
        cv2.imshow('frame', frame)
        if cv2.waitKey(144) & 0xFF == ord('q'):
            break

def main():
    ocr = YOLO(r"pretrained/bestcorner.pt")
    card_detector = YOLO(r"pretrained/best.pt")
    test_cam(ocr, card_detector)

if __name__ == "__main__":
    main()
