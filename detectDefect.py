import cv2
import numpy as np
import matplotlib.pyplot as plt


def process_image(image):
    image = cv2.resize(image,(300,340))
    image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    img_gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(img_gray,5)
    gaussian = cv2.GaussianBlur(blur,(5,5),0)
    ret,binary = cv2.threshold(gaussian,0,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(15,15))
    morph_open = cv2.morphologyEx(binary,cv2.MORPH_OPEN,kernel)
    return morph_open,image

def detection(image_template,image_check):
    process_temp_opening,process_temp = process_image(image_template)
    row,col = process_temp_opening.shape
    contours_temp,hierarchy = cv2.findContours(process_temp_opening,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    process_blister_opening,process_blister = process_image(image_check)
    process_blister_copy = process_blister.copy()
    process_blister_opening = cv2.resize(process_blister_opening,(col,row))
    contours_blister,hierarchy = cv2.findContours(process_blister_opening,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    tempPack = contours_temp[2]
    
    temp_Tablet = len(contours_temp)
    blister_Tablet = len(contours_blister)

    resultA = []
    for cnt in (contours_blister[2:blister_Tablet]):
        match = cv2.matchShapes(tempPack,cnt, 1, 0.0)
        if match < 0.25:
             resultA.append("Not Defected")
        else:
            resultA.append("Defected")
            x,y,w,h = cv2.boundingRect(cnt)
            cv2.rectangle(process_blister_copy, (x, y), (x + w, y + h), (255,0,0),2)
    if "Defected" in resultA:
        state = "Defected"
    else:
        state = "Not Defected"
    if temp_Tablet != blister_Tablet:
        state = "Defected"
        result = cv2.bitwise_xor(process_temp_opening,process_blister_opening)
        contours_result,hierarchy = cv2.findContours(result,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        areas_ = [cv2.contourArea(c_) for c_ in contours_result]
        max_index_ = np.argmax(areas_)
        tempPack_ =contours_result[max_index_]
        for cnt in contours_result:
            matchR = cv2.matchShapes(tempPack_,cnt, 1, 0.0)
            if matchR < 0.25:
                x,y,w,h = cv2.boundingRect(cnt)
                cv2.rectangle(process_blister_copy, (x, y), (x + w, y + h), (255,0,0),2)
    return process_blister_copy,state

