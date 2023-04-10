# imports
from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2
import numpy as np

debug = False;

# parser de argumentos cli
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="caminho do arquivo de video")
ap.add_argument("-a", "--min-area", type=int, default=500, help="tamanho mínimo de área")
args = vars(ap.parse_args())

# ler da webcam se não houver video de entrada
if args.get("video", None) is None:
    if debug == True:
        print("if")
    vs = VideoStream(src=0).start()
    time.sleep(2.0)

else:
    if debug == True:
        print("else")
    vs = cv2.VideoCapture(args["video"])

# armazenando o primeiro frame do video (background)
firstFrame = None

# iterando sobre os frames do video
while True:
    frame = vs.read()
    #frame2 = vs.read()
    frame = frame if args.get("video", None) is None else frame[1]
    #frame2 = frame if args.get("video", None) is None else frame2[1]
    text = "Unoccupied"

    if frame is None:
        break

    frame = imutils.resize(frame, width=500)
    #frame2 = imutils.resize(frame2, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if firstFrame is None:
        firstFrame = gray
        continue

    frameDelta = cv2.absdiff(firstFrame, gray)
    #firstFrame = gray
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    for c in cnts:
        if cv2.contourArea(c) < args["min_area"]:
            continue

        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = "Occupied"

    #cv2.putText(frame, "Room Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    #cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
                #cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

    thresh = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
    #thresh[np.all(thresh > (0, 0, 0), axis=-1)] = (0, 0, 255)

    #thresh[thresh[:, :, 1:].all(axis=-1)] = 0
    #frame2[frame2[:, :, 1:].all(axis=-1)] = 0

    #teste = cv2.addWeighted(thresh, 1, frame2, 1, 0)

    cv2.imshow("Resultado", frame)
    cv2.imshow("Thresh", thresh)
    cv2.imshow("Frame Delta", frameDelta)
    #cv2.imshow("Resultado 2", frame2)
    #cv2.imshow("Resultado 3", teste)
    key = cv2.waitKey(20) & 0xFF

    if key == ord("q"):
        break

vs.stop() if args.get("video", None) is None else vs.release()
cv2.destroyAllWindows()