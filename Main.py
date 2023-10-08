import cv2
import poker_image_processor as ip
import numpy as np
import os
from poker_ocr_engine import poker_ocr


def show_image(image):
    cv2.namedWindow("image", cv2.WINDOW_AUTOSIZE)
    cv2.imshow("image", image)
    cv2.waitKey(0)


def draw_image(image, points):
    color = (36, 255, 12)

    pt1 = (int(points[0][0][0]), int(points[0][0][1]))
    pt2 = (int(points[1][0][0]), int(points[1][0][1]))
    pt3 = (int(points[2][0][0]), int(points[2][0][1]))
    pt4 = (int(points[3][0][0]), int(points[3][0][1]))

    cv2.line(image, pt1, pt2, color, 3)
    cv2.line(image, pt2, pt3, color, 3)
    cv2.line(image, pt3, pt4, color, 3)
    cv2.line(image, pt4, pt1, color, 3)


def find_if_close(cnt1, cnt2):
    row1, row2 = cnt1.shape[0], cnt2.shape[0]
    for i in range(row1):
        for j in range(row2):
            dist = np.linalg.norm(cnt1[i] - cnt2[j])
            if abs(dist) < 800:
                return True
            elif i == row1 - 1 and j == row2 - 1:
                return False

def set_text(image, name, pts):
    average = np.sum(pts, axis=0)/len(pts)
    text_x = int(average[0][0])
    text_y = int(average[0][1])
    # Define the text and font parameters
    text = name
    font = cv2.LINE_AA
    font_scale = 1
    font_color = (0, 255, 0)  # Black color in BGR
    font_thickness = 2

    yadd = int(average[0][1] * 0.3)

    # Put the text on the image
    cv2.putText(image, text, (text_x - 60, text_y + yadd), font, font_scale, font_color, font_thickness)

def group_near_cards(card_list):
    ret = []
    loop_num = 0
    while loop_num < len(card_list):
        curr_list = []
        curr_list.append(card_list[loop_num])
        loop_num2 = loop_num
        while loop_num2 + 1 < len(card_list) and find_if_close(
            card_list[loop_num2], card_list[loop_num2 + 1]
        ):
            curr_list.append(card_list[loop_num2 + 1])
            loop_num += 1
            loop_num2 = loop_num
        ret.append(curr_list)
        loop_num += 1

    return ret


def test_all_images():
    main_folder = "poker-vision/test_data"

    for root, dirs, files in os.walk(main_folder):
        for file in files:
            base_name, extension = os.path.splitext(file)
            img_path = os.path.join(root, file)
            image = cv2.imread(img_path)
            image = cv2.resize(image, (1920, 1080))
            thresh = ip.process_card_image(image)
            conts = ip.get_card_contours(thresh)

            gathered_text = []
            for c in conts:
                fl = ip.flatten_perspective_transform(c, image)
                rank_img, val_img = ip.get_corner_info_image(fl)
                gathered_text.append(ip.perform_card_comparision(rank_img))

            print(base_name, ":", gathered_text)


def main():
    ocr = poker_ocr("test_data/training")
    ocr.initialize()
    # img_path = "test_data/royalflush_ace/IMG20231006142219.jpg"
    # img_path = "test_data/tilted/IMG20231007175210.jpg"
    img_path = "test_data/unique cards/IMG20231008001157.jpg"
    image = cv2.imread(img_path)
    image = cv2.resize(image, (1920, 1080))
    show_image(image)
    thresh = ip.process_card_image(image)
    conts = ip.get_card_contours(thresh)
    # testsdf = group_near_cards(conts)

    for c in conts:
        x, y, w, h = cv2.boundingRect(c)
        fl = ip.flatten_perspective_transform(c, image)
        rank_img, val_img = ip.get_corner_info_image(fl)
        pts = ip.get_contour_points(c)
        shape = ocr.scan_shape(val_img)
        rank = ocr.scan_rank(rank_img)
        print()
        draw_image(image, pts)
        set_text(image, ocr.get_text_from_rank_id(rank) + " " + ocr.get_text_from_shape_id(shape), pts)

    show_image(image)
    cv2.imwrite("test.jpg", image)

if __name__ == "__main__":
    main()
