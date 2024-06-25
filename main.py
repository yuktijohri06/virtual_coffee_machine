import os
import cv2
from cvzone.HandTrackingModule import HandDetector

# Initialize the webcam
cap = cv2.VideoCapture(0)
cap.set(3, 350)  # Width
cap.set(4, 305)  # Height

# Read the background image
imgBackground = cv2.imread("Resources/Background.png")

# Importing all the mode images to a list
folderPathModes = "Resources/Modes"
listImgModesPath = os.listdir(folderPathModes)
listImgModes = [cv2.imread(os.path.join(folderPathModes, imgModePath)) for imgModePath in listImgModesPath]

# Importing all the icons to a list
folderPathIcons = "Resources/Icons"
listImgIconsPath = os.listdir(folderPathIcons)
listImgIcons = [cv2.imread(os.path.join(folderPathIcons, imgIconsPath)) for imgIconsPath in listImgIconsPath]

# For changing selection mode
modeType = 0
selection = -1
counter = 0
selectionSpeed = 7
detector = HandDetector(detectionCon=0.8, maxHands=1)
modePositions = [(1136, 196), (1000, 384), (1136, 581)]
counterPause = 0
selectionList = [-1, -1, -1]

while True:
    success, img = cap.read()

    if not success:
        print("Failed to capture image")
        break

    # Resize the captured image to fit in the background
    img = cv2.resize(img, (350, 305))

    # Overlaying the webcam feed on the background image
    imgBackground[98:98 + 305, 55:55 + 350] = img

    # Ensure there is at least one mode image before attempting to display it
    if listImgModes:
        # Define the area where the mode image will be placed
        mode_img_area_height = 438
        mode_img_area_width = 338

        # Resize the mode image to fit the designated area
        mode_img_resized = cv2.resize(listImgModes[modeType], (mode_img_area_width, mode_img_area_height))

        # Calculate the starting x-coordinate to place the mode image in the farthest right position
        x_offset = imgBackground.shape[1] - mode_img_area_width

        # Overlay the resized mode image onto the background at the specified position
        imgBackground[282:282 + mode_img_area_height, x_offset:imgBackground.shape[1]] = mode_img_resized

    # Find the hand and its landmarks
    hands, img = detector.findHands(img)  # with draw

    if hands and counterPause == 0 and modeType < 3:
        # Hand 1
        hand1 = hands[0]
        fingers1 = detector.fingersUp(hand1)
        print(fingers1)
        if fingers1 == [0, 1, 0, 0, 0]:
            if selection != 1:
                counter = 1
            selection = 1
        elif fingers1 == [0, 1, 1, 0, 0]:
            if selection != 2:
                counter = 1
            selection = 2
        elif fingers1 == [0, 1, 1, 1, 0]:
            if selection != 3:
                counter = 1
            selection = 3
        else:
            selection = -1
            counter = 0

        if counter > 0:
            counter += 1
            print(counter)
            cv2.ellipse(imgBackground, modePositions[selection - 1], (103, 103), 0, 0,
                        counter * selectionSpeed, (0, 255, 0), 20)
            if counter * selectionSpeed > 360:
                selectionList[modeType] = selection
                modeType += 1
                counter = 0
                selection = -1
                counterPause = 1

    # To pause after each selection is made
    if counterPause > 0:
        counterPause += 1
        if counterPause > 60:
            counterPause = 0

    # Add selection icon at the bottom
    if selectionList[0] != -1:
        imgBackground[636:636 + 65, 133:133 + 65] = listImgIcons[selectionList[0] - 1]
    if selectionList[1] != -1:
        imgBackground[636:636 + 65, 340:340 + 65] = listImgIcons[2 + selectionList[1]]
    if selectionList[2] != -1:
        imgBackground[636:636 + 65, 542:542 + 65] = listImgIcons[5 + selectionList[2]]

    # Displaying
    cv2.imshow("Background", imgBackground)

    # Break the loop if the 'l' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('l'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
