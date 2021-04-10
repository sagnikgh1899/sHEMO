import cv2
import numpy as np
from PIL import Image
import PIL.ImageOps
import os
import math


def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]),
                                                None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank] * rows
        hor_con = [imageBlank] * rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver


def hisEqulColor(img):
    ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
    channels = cv2.split(ycrcb)
    # print (len(channels))
    cv2.equalizeHist(channels[0], channels[0])
    cv2.merge(channels, ycrcb)
    cv2.cvtColor(ycrcb, cv2.COLOR_YCR_CB2BGR, img)
    return img


def reduce_size_of_image(img):
    height, width = img.shape[:2]
    eyebrow_h = int(height / 1.5)  # Can be made ~25% by putting 4 in place of 3
    width_left = int(width / 6)
    width_right = int(width / 6)
    # img = img[eyebrow_h:height, 0:width]  # cut eyebrows out (15 px)
    img = img[eyebrow_h:height, width_left:(width - width_right)]
    return img


def reduce_size_of_image_after_centroid_detection(img, cX):
    height, width = img.shape[:2]
    width_left = int(width / 6)
    width_right = int(width / 6)
    img = img[cX:height, width_left:(width - width_right)]
    return img


def auto_canny(image1, sigma=0.55):
    # compute the median of the single channel pixel intensities
    image = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    v = np.median(image)
    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)
    # return the edged image
    return edged


def MODIFICATION(path_init):
    def Modification_sub(dist, path_init):
        """if dist == 'F':
            dis = 25  # 25
        else:
            dis = 25"""
        dis = 25
        eye1 = cv2.imread(path_init)
        eye = eye1

        def ImfillPython(im_in):
            im_in = cv2.imread("My Image1.png", cv2.IMREAD_GRAYSCALE)
            th, im_th = cv2.threshold(im_in, 50, 255, cv2.THRESH_BINARY_INV)
            im_floodfill = im_th.copy()
            h, w = im_th.shape[:2]
            mask = np.zeros((h + 2, w + 2), np.uint8)
            cv2.floodFill(im_floodfill, mask, (0, 0), 255)
            im_floodfill_inv = cv2.bitwise_not(im_floodfill)
            im_out = im_th | im_floodfill_inv
            path1 = 'Foreground.png'
            cv2.imwrite(path1, im_out)

            img_new = Image.open(path1)
            img_inverted = PIL.ImageOps.invert(img_new)
            imfill_path = 'Imfill.png'
            img_inverted.save(imfill_path)
            return imfill_path

        detector_params = cv2.SimpleBlobDetector_Params()
        detector_params.filterByArea = True
        detector_params.maxArea = 1500  # 1500
        detector = cv2.SimpleBlobDetector_create(detector_params)

        def cut_eyebrows(img):
            height, width = img.shape[:2]
            eyebrow_h = int(height / 4)
            img = img[eyebrow_h:height, 0:width]  # cut eyebrows out (15 px)
            return img

        eye = cut_eyebrows(eye)
        cv2.imshow('my image', eye)

        # cv2.imwrite("eye1.png",eye)
        # cv2.waitKey(0)

        def Refine(input_path):
            img_init = cv2.imread(input_path)
            img = Image.open(input_path)
            rows, columns = img_init.shape[0], img_init.shape[1]
            limit = int(0.28 * columns)
            pix = img.load()
            for i in reversed(range(0, rows)):
                for j in reversed(range(columns - limit, columns)):
                    pix[j, i] = (255, 255, 255)

            result_path = 'Final Blob.png'
            img.save(result_path)
            return result_path

        def blob_process(img, detector):
            gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            _, img = cv2.threshold(gray_frame, 35, 255, cv2.THRESH_BINARY)  # 30

            cv2.imwrite("My Image1.png", img)

            path_req = ImfillPython(img)
            img = cv2.imread(path_req)

            kernel = np.ones((5, 5), np.uint8)
            img = cv2.erode(img, kernel, iterations=2)  # 1
            img = cv2.dilate(img, kernel, iterations=6)  # 2
            img = cv2.medianBlur(img, 5)  # 3

            cv2.imwrite("my image3.png", img)

            keypoints = detector.detect(img)
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(gray_image, 127, 255, 0)

            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            count = 0
            if len(contours) == 0:
                return False
            for c in contours:
                if count == len(contours) - 1 and len(contours) > 1:
                    # calculate moments for each contour
                    M = cv2.moments(c)
                    # calculate x,y coordinate of center
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    # print(cX, cY)
                    cx_fin = cX
                    cy_fin = cY
                    cv2.circle(eye, (cX, cY), 3, (255, 0, 0), -1)
                    new_cx, new_cy = cX, cY + dis
                    # cv2.circle(eye, (new_cx, new_cy), 3, (0, 255, 0), -1)        #Uncomment this for display purpose
                    # cv2.imshow("!", eye)
                    # cv2.waitKey(0)
                    img_my = reduce_size_of_image_after_centroid_detection(eye, new_cy)
                    ROI_reduced_path = "ROI_Reduced.jpg"
                    cv2.imwrite(ROI_reduced_path, img_my)
                    break
                elif len(contours) == 1:
                    # calculate moments for each contour
                    M = cv2.moments(c)
                    # calculate x,y coordinate of center
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    # print(cX, cY)
                    cx_fin = cX
                    cy_fin = cY
                    cv2.circle(eye, (cX, cY), 3, (255, 0, 0), -1)
                    new_cx, new_cy = cX, cY + dis
                    # cv2.circle(eye, (new_cx, new_cy), 3, (0, 255, 0), -1)       #Uncomment this for display purpose
                    # cv2.imshow("!", eye)
                    # cv2.waitKey(0)
                    img_my = reduce_size_of_image_after_centroid_detection(eye, new_cy)
                    ROI_reduced_path = "ROI_Reduced.jpg"
                    cv2.imwrite(ROI_reduced_path, img_my)
                else:
                    count += 1

            return keypoints, cx_fin, cy_fin, img_my

        if not blob_process(eye, detector):
            # print("\nUnclear Image or Blob Not Detected. Please Capture New Image!!")
            return False, 0

        keypoints, cx_fin, cy_fin, img_my = blob_process(eye, detector)

        # eye = cv2.drawKeypoints(eye, keypoints, eye, (0, 255, 0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        # cv2.destroyAllWindows()
        # cv2.imshow('Result1', eye)
        # cv2.waitKey(0)
        # cv2.imshow('Result2', img_my)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    Modification_sub('F', path_init)
    return True
    ##################################################################################################################


def Eye_Detection(img):
    eyesCascade = cv2.CascadeClassifier("haarcascade_eye.xml")
    eyes = eyesCascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(100, 100))

    if len(eyes) != 0:
        print("Number of Eyes detected = ", len(eyes))
        for (x, y, w, h) in eyes:
            eye = img[y:y + h, x:x + w]
            ROI = eye
            cv2.imwrite("ROI_1.jpg", ROI)

            ROI_reduced = cv2.imread('ROI_1.jpg')
            # Use the MODIFICATION function here; If blob is detected then use the modified reduced image; If blob is
            # not identified, return False and reduce the image by the previous method; However if blob is detected
            # in a wrong position and detected centroid is different then we need to check that manually; A solution
            # to the above problem is to display the Reduced Image and computer asks whether user is satisfied with
            # the capture; If user says YES(Y), the rest of the work takes place; If user says NO(N), the code stops
            # and prompts the user to take a better image;

            path_init = 'ROI_1.jpg'
            boolean = MODIFICATION(path_init)
            if not boolean:
                ROI_reduced = reduce_size_of_image(ROI_reduced)
                ROI_reduced_path = "ROI_Reduced.jpg"
                cv2.imwrite(ROI_reduced_path, ROI_reduced)

            check_img = cv2.imread('ROI_Reduced.jpg')
            cv2.imshow("Reduced Image", check_img)
            cv2.waitKey(0)
            satisfaction = str(input('Are you satisfied with the Reduced Image [Y/N]? '))
            satisfaction = satisfaction.upper()

            if satisfaction != 'Y':
                return 129, 129

            ROI_reduced_path = 'ROI_Reduced.jpg'
            ROI_reduced_1_color = cv2.imread('ROI_Reduced.jpg')
            # ROI_reduced_1 = cv2.cvtColor(ROI_reduced_1_color, cv2.COLOR_BGR2GRAY)
            # ROI_reduced_1_color_median = cv2.medianBlur(ROI_reduced_1_color, 1)
            edges = auto_canny(ROI_reduced_1_color)
            # ROI_reduced_1_blurred = cv2.GaussianBlur(ROI_reduced_1_color_median, (5, 5), 0)
            # edges = cv2.Canny(ROI_reduced_1_blurred, 40, 150)  # Originally was 30, 150

            edges_path = "EDGES.png"
            cv2.imwrite(edges_path, edges)

            # imgStack = stackImages(0.5, ([ROI, ROI_reduced, edges]))
            # cv2.imshow("Stacked Images", imgStack)  ## Uncomment this
            # cv2.waitKey(0)
            cv2.destroyAllWindows()

            return ROI_reduced_path, edges_path
    else:
        return 0, 0


def Get_Conjunctiva_Region(ROI_reduced_path, edges_path):
    img_init = cv2.imread(edges_path)
    img = Image.open(edges_path)
    rows, columns = img_init.shape[0], img_init.shape[1]

    pix = img.load()

    for i in range(0, rows):
        for j in range(0, columns):
            # print(pix[j, i])
            if pix[j, i] > 250:
                for k in range(0, i):
                    pix[j, k] = 255

    inverted_image = PIL.ImageOps.invert(img)
    inverted_image.save('EdgesTest.png')

    img_red = cv2.imread(ROI_reduced_path)
    img_new = cv2.imread('EdgesTest.png')

    fin_img = cv2.subtract(img_red, img_new)

    result_path = "RESULT.jpg"
    for i in range(len(fin_img)):
        for j in range(len(fin_img[i])):
            img_val_list = [fin_img[i][j]]
            if img_val_list[0][0] < 10 and img_val_list[0][1] < 10 and img_val_list[0][2] < 10:
                fin_img[i][j] = [255, 255, 255]  # _val_list = [[255,255,255]]

    # cv2.imshow('FINAL ROI', fin_img)
    # cv2.waitKey(0)
    cv2.imwrite(result_path, fin_img)
    cv2.destroyAllWindows()
    return result_path

# Enter the input image here:
img = cv2.imread("51.png")

ROI_reduced_path, edges_path = Eye_Detection(img)
if ROI_reduced_path == 129 and edges_path == 129:
    print("\nPlease Capture a New Image!!")
elif ROI_reduced_path == 0 and edges_path == 0:
    print("\nNo eyes detected!!")
else:
    result_path = Get_Conjunctiva_Region(ROI_reduced_path, edges_path)
    img_res = cv2.imread(result_path)
    imgStack = stackImages(0.5, ([img, img_res]))
    # cv2.imshow("Stacked Images", imgStack)    # For showing results to Profs
    # cv2.waitKey(0)

os.remove('EDGES.png')
os.remove('EdgesTest.png')
os.remove('Foreground.png')
os.remove('Imfill.png')
os.remove('My Image1.png')
os.remove('my image3.png')
os.remove('ROI_Reduced.jpg')
os.remove('ROI_1.jpg')

add_value = 3
# opencv loads the image in BGR, convert it to RGB
img_orig = cv2.imread('RESULT.jpg')
startIdx = []
endIdx = []
whitebeginIdx = []
for row in range(len(img_orig)):
    for column in range(len(img_orig[0])):
        if img_orig[row][column][0] < 220 and img_orig[row][column][1] < 220 and img_orig[row][column][2] < 220:
            startIdx.append([row, column])
            break
    break

for row in range(len(img_orig)):
    for column in reversed(range(len(img_orig[0]))):
        if img_orig[row][column][0] < 220 and img_orig[row][column][1] < 220 and img_orig[row][column][2] < 220:
            endIdx.append([row, column])
            break
    break

mid_point = (startIdx[0][1] + endIdx[0][1]) // 2

for row in range(0, len(img_orig)):
    if img_orig[row][mid_point][0] > 230 and img_orig[row][mid_point][1] > 230 and img_orig[row][mid_point][2] > 230:
        whitebeginIdx.append(row)
        break

# This will set the correct lower range depending on the eye size
if 60 <= len(img_orig) < 100:
    my_value = 23
elif len(img_orig) >= 90:
    my_value = 40
else:
    my_value = 18

y_coordinate = whitebeginIdx[0] - my_value

img1 = cv2.rectangle(img_orig, (mid_point, y_coordinate), (mid_point + 5, y_coordinate + 5), (0, 255, 255), 1)
img2 = img_orig[y_coordinate:y_coordinate + 5, mid_point:mid_point + 5]
img = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)

img4 = cv2.rectangle(img_orig, (mid_point + 10, y_coordinate), (mid_point + 5 + 10, y_coordinate + 5), (0, 255, 255), 1)
img5 = cv2.rectangle(img_orig, (mid_point - 10, y_coordinate), (mid_point + 5 - 10, y_coordinate + 5), (0, 255, 255), 1)

# cv2.imshow("F1", img5)
# cv2.waitKey(0)

img8 = img_orig[y_coordinate:y_coordinate + 5, mid_point + 10:mid_point + 5 + 10]
img9 = img_orig[y_coordinate:y_coordinate + 5, mid_point - 10:mid_point + 5 - 10]

img11 = cv2.cvtColor(img8, cv2.COLOR_BGR2RGB)
img12 = cv2.cvtColor(img9, cv2.COLOR_BGR2RGB)

############################################################################
red_list = []
green_list = []
blue_list = []

#############################################################################
# 1st small patch
histg_list = []
histr_list = []

histg = cv2.calcHist([img], [1], None, [256], [0, 220])
histr = cv2.calcHist([img], [0], None, [256], [0, 220])
histb = cv2.calcHist([img], [2], None, [256], [0, 220])

total_value_g = 0
for i in range(len(histg)):
    total_value_g += (i * histg[i])
avg_value_g = total_value_g / sum(histg)

total_value_r = 0
for i in range(len(histr)):
    total_value_r += (i * histr[i])
avg_value_r = total_value_r / sum(histr)

total_value_b = 0
for i in range(len(histb)):
    total_value_b += (i * histb[i])
avg_value_b = total_value_b / sum(histb)
red_list.append(avg_value_r)
blue_list.append(avg_value_b)
green_list.append(avg_value_g)

##########################################################33
# 2nd Small patch
histg_list = []
histr_list = []

histg = cv2.calcHist([img11], [1], None, [256], [0, 220])
histr = cv2.calcHist([img11], [0], None, [256], [0, 220])
histb = cv2.calcHist([img11], [2], None, [256], [0, 220])

total_value_g = 0
for i in range(len(histg)):
    total_value_g += (i * histg[i])
avg_value_g = total_value_g / sum(histg)

total_value_r = 0
for i in range(len(histr)):
    total_value_r += (i * histr[i])
avg_value_r = total_value_r / sum(histr)

total_value_b = 0
for i in range(len(histb)):
    total_value_b += (i * histb[i])
avg_value_b = total_value_b / sum(histb)
red_list.append(avg_value_r)
blue_list.append(avg_value_b)
green_list.append(avg_value_g)

###############################################################
# 3rd small patch
histg_list = []
histr_list = []

histg = cv2.calcHist([img12], [1], None, [256], [0, 220])
histr = cv2.calcHist([img12], [0], None, [256], [0, 220])
histb = cv2.calcHist([img12], [2], None, [256], [0, 220])

total_value_g = 0
for i in range(len(histg)):
    total_value_g += (i * histg[i])
avg_value_g = total_value_g / sum(histg)

total_value_r = 0
for i in range(len(histr)):
    total_value_r += (i * histr[i])
avg_value_r = total_value_r / sum(histr)

total_value_b = 0
for i in range(len(histb)):
    total_value_b += (i * histb[i])
avg_value_b = total_value_b / sum(histb)

red_list.append(avg_value_r)
blue_list.append(avg_value_b)
green_list.append(avg_value_g)


#########################################################################
avg_value_r = sum(red_list) / 3
avg_value_b = sum(blue_list) / 3
avg_value_g = sum(green_list) / 3

val1 = (-1.922 + 0.206 * avg_value_r - 0.241 * avg_value_g + 0.012 * avg_value_b)
Num = math.exp(val1)
Den = 1 + math.exp(val1)
L = Num / Den
if (L * 10 + add_value) < 6:
    Hgb_val = 10
else:
    Hgb_val = (L * 10 + add_value)
print("\n Hgb = ", round(Hgb_val, 2), "g/dl")

if Hgb_val < 13:  # A Threshold value I have used on the basis of data available to me
    print("\nAnemic")
else:
    print("\nNon-Anemic")

startIdx = []
endIdx = []
whitebeginIdx = []
