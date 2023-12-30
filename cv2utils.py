import cv2
import numpy as np
from threading import Thread

class ThreadedCamera(object):
    def __init__(self, source = 0, w = 1920, h = 1080):

        self.capture = cv2.VideoCapture(source)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, w)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
        self.capture.set(cv2.CAP_PROP_FPS, 60)
        self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 10)
        self.thread = Thread(target = self.update, args = ())
        self.thread.daemon = True
        self.thread.start()

        self.status = False
        self.frame  = None

    def update(self):
        while True:
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()

    def grab_frame(self):
        if self.status:
            return self.frame
        return None  

# show image in a popup window
def show_image(image, title = "image"):
    cv2.namedWindow(title, cv2.WINDOW_AUTOSIZE)
    cv2.moveWindow(title, 40,30)
    cv2.imshow(title, image)
    cv2.waitKey(0)

# highlight object in an image
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

# technique to check distance between two objects in an image regardless of image size
def calculate_normalized_distance(point1, point2, image_width, image_height):
    # Calculate the Euclidean distance between two points
    distance = np.linalg.norm(np.array(point1) - np.array(point2))

    # Normalize the distance based on image dimensions
    normalized_distance = distance / max(image_width, image_height)

    return normalized_distance

# function for check if two objects in an image are close to one another or not
def find_if_close(image, cnt1, cnt2):
    threshold = 0.3
    image_height, image_width, _ = image.shape

    normalized_distance = calculate_normalized_distance(cnt1, cnt2, image_width, image_height)
    return normalized_distance < threshold

# sets name of the detected card
def set_image_text(image, name, pts):
    average = np.sum(pts, axis=0)/len(pts)
    text_x = int(average[0][0])
    text_y = int(average[0][1])
    # Define the text and font parameters
    text = name
    font = cv2.LINE_AA
    font_scale = 0.5
    font_color = (255, 0, 0)  # Black color in BGR
    font_thickness = 2

    text_size_vec = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
    to_sub_len = int(text_size_vec[0] * 0.5)
    yadd = int((text_size_vec[1] * 2.8))
    # Put the text on the image
    cv2.putText(image, text, (text_x - to_sub_len, text_y + yadd), font, font_scale, font_color, font_thickness)

# sets name of the detected group
def set_group_text(image, name, x, y):
    text_x = int(x)
    text_y = int(y)
    # Define the text and font parameters
    text = name
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.8
    font_color = (255,0,0)  # Black color in BGR
    font_thickness = 2
    # Put the text on the image
    cv2.putText(image, text, (text_x, text_y - 10), font, font_scale, font_color, font_thickness)

# highlights the group of cards
def highlight_grouped_cards(image, card_group, text):
    x,y,w,h = union(card_group[0].contour, card_group[-1].contour)
    wdiff = int(w * 0.05)
    hdiff = int(h * 0.05)
    x -= int(wdiff)
    y -= int(hdiff)
    w += wdiff * 2
    h += hdiff * 2
    cv2.rectangle(image, (x, y), (x + w, y + h),(0,0,255), 3)
    set_group_text(image, text, x, y)

# highlights all the cards in a list
def highlight_card_list(image, card_list):
    for b in card_list:
        draw_image(image, b.points)
        set_image_text(image, str(b.card), b.points)

# clusters near cards
def group_near_cards(image, card_list):
    ret = []
    curr_list = []
    for i in range(len(card_list)):
        curr_list.append(card_list[i])
        if i + 1 < len(card_list) and find_if_close(image, card_list[i].contour, card_list[i + 1].contour):
            continue
        curr_list.sort(key= lambda x: cv2.boundingRect(x.contour)[0])
        ret.append(curr_list)
        curr_list = []
            
    return ret

# union two contours
def union(a1,b1):
    a = cv2.boundingRect(a1)
    b = cv2.boundingRect(b1)
    x = min(a[0], b[0])
    y = min(a[1], b[1])
    w = max(a[0]+a[2], b[0]+b[2]) - x
    h = max(a[1]+a[3], b[1]+b[3]) - y
    return (x, y, w, h)
