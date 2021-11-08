#CarDetectionOnVideo


import cv2

thres = 0.6
# Kynnysarvo objektin tunnistamiselle (0-1)


classNames = []
classFile = 'coco.names3'
with open(classFile, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')  # Tässä haetaan objektien nimet, poistetaan rivinvaihdot, jako

configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'  #
weightsPath = 'frozen_inference_graph.pb'

net = cv2.dnn_DetectionModel(weightsPath, configPath)
net.setInputSize(320, 320)
net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)


def getObjects(img, draw=True, objects=[]):
    classIds, confs, bbox = net.detect(img, confThreshold=thres, nmsThreshold=0.2)
    # print(classIds,bbox)
    if len(objects) == 0: objects = classNames

    objectInfo = []
    if len(classIds) != 0:
        for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
            className = classNames[classId - 1]
            if className in objects:

                objectInfo.append([box, className])
                if (draw):
                    cv2.rectangle(img, box, color=(0, 255, 0), thickness=2)  # Tekee neliön objektin ympärille
                    cv2.putText(img, className.upper(), (box[0] + 10, box[1] + 30),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0),
                                2)  # Laitetaan teksti nimen(classIds) perusteella
                    cv2.putText(img, str(round(confidence * 100, 2)), (box[0] + 200, box[1] + 30),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0),
                                2)  # Laitetaan teksti confidence valuen perusteella
    return img, objectInfo


if __name__ == "__main__":

    cap = cv2.VideoCapture('10_3.MP4')  # Avataan videoyhteys
    #cap.set(3, 1920)  # Videon resoluutio(leveys)
    #cap.set(4, 1080)  # Videon resoluutio(korkeus)
    # cap.set(10,70) #Brightness
    while True:
        img = cv2.imread('testaaja.png')
        ##success, img = cap.read()
        result, objectInfo = getObjects(img, objects=['person'])
        #print(objectInfo)
        cv2.imshow("Output", img)
        cv2.waitKey(1)