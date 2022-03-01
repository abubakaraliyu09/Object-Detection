import cv2
import numpy as np
from gui_buttons import *

#Initialise buttons
button = Buttons()
button.add_button("person", 20,20)
button.add_button("cell phone", 20,100)
button.add_button("keyboard", 20,180)
button.add_button("remote", 20,260)
button.add_button("cup", 20,340)
button.add_button("Tv monitor", 20,420)

net = cv2.dnn.readNet('model/yolov4-tiny.weights','model/yolov4-tiny.cfg')
model = cv2.dnn_DetectionModel(net)
model.setInputParams(size = (320,320),scale=1/255)

#load class list
classes = []
with open('model/classes.txt', 'r') as file_object:
    for class_name in file_object.readlines():
        #print(class_name)
        class_name = class_name.strip()
        classes.append(class_name)

#Initialise the Webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
#FUll HD 1920 X 1080

button_person = False
def click_button(event, x, y, flags, params):
    global button_person
    if event == cv2.EVENT_LBUTTONDOWN:
        #print(x, y)
        button.button_click(x,y)
        # polygon = np.array([[(20,20),(200,20),(200,70),(20,70)]])
        #
        # is_inside = cv2.pointPolygonTest(polygon,(x,y),False)
        # if is_inside > 0:
        #     print("we're clicking inside the button", x,y)
        #
        #     if button_person is False:
        #         button_person = True
        #     else:
        #         button_person = False
        #     print("Now button person is: ", button_person)


#Create window
cv2.namedWindow('Frame')
cv2.setMouseCallback('Frame', click_button)

while True:
    #Get frames
    ret,frame = cap.read()

    #Get active button list
    active_button = button.active_buttons_list()
    print("Active buttons",active_button)

    #Object detection
    (class_ids, scores, bboxes) = model.detect(frame)
    for class_id, score, bbox in zip(class_ids,scores,bboxes):
        (x,y,w,h) = bbox
        #print(x,y,w,h)
        class_name = classes[class_id[0]]

        if class_name in active_button:

            cv2.putText(frame, class_name, (x, y - 5), cv2.FONT_HERSHEY_PLAIN,2,(0,100,220),2)
            cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),thickness=2)

    #Create a button
    #cv2.rectangle(frame, (20,20),(200,70),(0,0,200),thickness=-1)
    # polygon = np.array([[(20,20),(200,20),(200,70),(20,70)]])
    # cv2.fillPoly(frame, polygon, (0,0,200))
    # cv2.putText(frame, 'person',(30,60), cv2.FONT_HERSHEY_PLAIN, 3, (0.0,0),3)



    # print('class_ids', class_ids)
    # print('score', scores)
    # print('bboxes', bboxes)

    #Display button
    button.display_buttons(frame)

    cv2.imshow('Frame', frame)

    key = cv2.waitKey(1)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()