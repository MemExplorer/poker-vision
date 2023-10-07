import cv2
import poker_image_processor as ip

def show_image(image):
    cv2.namedWindow("image", cv2.WINDOW_AUTOSIZE)
    cv2.imshow("image", image)
    cv2.waitKey(0)

def draw_image(image, points):
    color = (36,255,12)
    pt1 = (int(points[0][0][0]), int(points[0][0][1]))
    pt2 = (int(points[1][0][0]), int(points[1][0][1]))
    pt3 = (int(points[2][0][0]), int(points[2][0][1]))
    pt4 = (int(points[3][0][0]), int(points[3][0][1]))

    cv2.line(image, pt1, pt2, color, 3)
    cv2.line(image, pt2, pt3, color, 3)
    cv2.line(image, pt3, pt4, color, 3)
    cv2.line(image, pt4, pt1, color, 3)

def main():
    img_path = "test_data/royalflush_spade/IMG20231006142219.jpg"
    image = cv2.imread(img_path)
    image = cv2.resize(image, (1920, 1080))
    thresh = ip.process_card_image(image)
    conts = ip.get_card_contours(thresh)
    for c in conts:
        fl = ip.flatten_perspective_transform(c, image)
        rank_img, val_img = ip.get_corner_info_image(fl)
        show_image(val_img)
    cv2.waitKey(0)

if __name__ == "__main__":
    main()