import cv2
import poker_image_processor as ip
import cv2utils
from poker_ocr_engine import poker_ocr
from poker_card import cardinfo, analysed_poker_card

import hand_ranking_identifier as hid
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
        
    (None, None)
        
def get_player_cards(grouped_cards):
    valid_list = []
    for g in grouped_cards:
        if len(g) == 2:
            valid_list.append(g)

    return valid_list

def analyse_card(ocr_engine, image, card_contour):
    fl = ip.flatten_perspective_transform(card_contour, image)
    rank_img, val_img = ip.get_corner_info_image(fl)
    pts = ip.get_contour_points(card_contour)
    shape = ocr_engine.scan_shape(val_img)
    rank = ocr_engine.scan_rank(rank_img)
    card = cardinfo(shape, rank)
    return analysed_poker_card(pts, card)

def detect_cards_from_image(ocr, image):
    #cv2utils.show_image(image)
    thresh = ip.process_card_image(image)
    conts = ip.get_card_contours(thresh)

    if len(conts) == 0:
        return
    
    # highlight nearest cards
    grouped_near_cards = cv2utils.group_near_cards(image, conts)

    dealer_img_cards, is_one = get_dealer_cards(grouped_near_cards)
    player_img_cards = get_player_cards(grouped_near_cards)

    if dealer_img_cards == None:
        return
    
    if is_one:
        player_img_cards = []
    
    analysed_dealer_cards =  [analyse_card(ocr, image, c) for c in dealer_img_cards]
    dealer_cards = [c.card for c in analysed_dealer_cards]
    cv2utils.highlight_card_list(image, analysed_dealer_cards)
    cv2utils.highlight_grouped_cards(image, dealer_img_cards, "Dealer")

    for p in range(len(player_img_cards)):
        analysed_player_cards = [analyse_card(ocr, image, c) for c in player_img_cards[p]]
        player_cards = [c.card for c in analysed_player_cards]
        cv2utils.highlight_card_list(image, analysed_player_cards)
        ranking = detect_hand_ranking(dealer_cards, player_cards)
        cv2utils.highlight_grouped_cards(image, player_img_cards[p], f"Player {p + 1} ({ranking})")

def main():
    ocr = poker_ocr("test_data/training")
    ocr.initialize()
    # img_path = "test_data/royalflush_ace/IMG20231006142219.jpg"
    # img_path = "test_data/tilted/IMG20231007175210.jpg"
    img_path = "test_data/tilted/IMG20231007175210.jpg"
    image = cv2.imread(img_path)
    image = cv2.resize(image, (1920, 1080))
    detect_cards_from_image(ocr, image)


    cv2utils.show_image(image)
    cv2.imwrite("test.jpg", image)

if __name__ == "__main__":
    main()
