import cv2
import poker_image_processor as ip
import numpy as np
import os


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
    # img_path = "test_data/royalflush_ace/IMG20231006142219.jpg"
    # img_path = "test_data/tilted/IMG20231007175210.jpg"
    img_path = "poker-vision/test_data/royalflush_spade/IMG20231006142542.jpg"
    image = cv2.imread(img_path)
    image = cv2.resize(image, (1920, 1080))

    thresh = ip.process_card_image(image)
    conts = ip.get_card_contours(thresh)
    # testsdf = group_near_cards(conts)

    gathered_text = []
    for c in conts:
        x, y, w, h = cv2.boundingRect(c)
        fl = ip.flatten_perspective_transform(c, image)
        rank_img, val_img = ip.get_corner_info_image(fl)
        pts = ip.get_contour_points(c)
        draw_image(image, pts)
        # show_image(fl)
        # show_image(rank_img)
        # show_image(val_img)
        # cv2.rectangle(image, (x, y), (x + w, y + h),(36,255,12))
        # cv2.drawContours(image, c, -1, (0, 255, 0), 2)
        gathered_text.append(ip.perform_card_comparision(rank_img))

    print(gathered_text)


if __name__ == "__main__":
    test_all_images()
    # main()
