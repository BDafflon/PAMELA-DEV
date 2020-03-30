import cv2
import imutils


def importation(path):
    font = cv2.FONT_HERSHEY_SIMPLEX
    # Read image*
    image = cv2.imread(path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, gray = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)

    cnts = cv2.findContours(gray.copy(), cv2.RETR_TREE,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    i=0
    result = []
    for c in cnts:

        if i != 0 :
            # compute the center of the contour, then detect the name of the
            # shape using only the contour
            M = cv2.moments(c)
            cX = int((M["m10"] / M["m00"]) * 1)
            cY = int((M["m01"] / M["m00"]) * 1)

            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 5, True)
            shape = "unidentified"
            print(str(i)+str(len(approx)))
            if len(approx) == 4:

                (x, y, w, h) = cv2.boundingRect(approx)
                ar = w / float(h)

                c = c.astype("int")
                image = cv2.drawContours(image, [c], -1, (255, 0, 0), 2)

                i=i+1

                k = image[cY, cX]
                k1=image[cY, cX]

                if k[0] == 0 and k[1] == 255 and k[2]==0:
                    cv2.putText(image, "pickup", (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, (255, 255, 255), 2)
                    result.append({'type':'pickup','coord':[x, y, w, h]})
                else :
                    if k[0] == 0 and k[1] == 0 and k[2]==255:
                        cv2.putText(image, "dropoff", (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
                                    0.5, (255, 255, 255), 2)
                        result.append({'type': 'dropoff', 'coord': [x, y, w, h]})
                    else :

                        if k[0] == 0 and k[1] == 0 and k[2] == 0:
                            cv2.putText(image, "wall", (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
                                        0.5, (255, 255, 255), 2)
                            result.append({'type': 'wall', 'coord': [x, y, w, h]})

                image = cv2.rectangle(image, (cX, cY), (cX, cY), (255,0,0), 5)



        i = i + 1

    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return result
    # show the output image

