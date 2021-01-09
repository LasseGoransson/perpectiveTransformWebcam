import numpy as np
import cv2
import virtualvideo


# top left, top right, bottom left, bottom right
pts = [(0,0),(0,0),(0,0),(0,0)]
pointIndex = 0

cam = cv2.VideoCapture(0)

_,img = cam.read()


# mouse callback function
def draw_circle(event,x,y,flags,param):
        global img
        global pointIndex
        global pts

        if event == cv2.EVENT_LBUTTONDBLCLK:
                cv2.circle(img,(x,y),0,(255,0,0),-1)
                pts[pointIndex] = (x,y)
                pointIndex = pointIndex + 1

def selectFourPoints():
        global img
        global pointIndex

        print( "Please select 4 points, by double clicking on each of them in the order: \n\
        top left, top right, bottom left, bottom right.")


        while(pointIndex != 4):
                cv2.imshow('image',img)
                key = cv2.waitKey(20) & 0xFF
                if key == 27:
                        return False

        return True
# Create a black image, a window and bind the function to window
# img = np.zeros((512,512,3), np.uint8)

cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_circle)

while(1):
        if(selectFourPoints()):

                # Euc dist
                eucDist = np.sqrt((pts[1][0]-pts[0][0])*(pts[1][0]-pts[0][0])+(pts[1][1]-pts[0][1])*(pts[1][1]-pts[0][1]))

                # Aspect ratio for an A4 sheet. 1:1.414
                ASPECT_RATIO = (eucDist,eucDist*1.414)

                pts2 = np.float32([[0+pts[0][0],0+pts[0][1]],[ASPECT_RATIO[1]+pts[0][0],0+pts[0][1]],[0+pts[0][0],ASPECT_RATIO[0]+pts[0][1]],[ASPECT_RATIO[1]+pts[0][0],ASPECT_RATIO[0]+pts[0][1]]])

                # The four points of the A4 paper in the image
                pts1 = np.float32([\
                        [pts[0][0],pts[0][1]],\
                        [pts[1][0],pts[1][1]],\
                        [pts[2][0],pts[2][1]],\
                        [pts[3][0],pts[3][1]] ])
                            
                M = cv2.getPerspectiveTransform(pts1,pts2)

                break
cam.release()
cv2.destroyAllWindows()






class MyVideoSource(virtualvideo.VideoSource):
    def __init__(self):
        self.cam = cv2.VideoCapture(0)
        _, img = self.cam.read()
        size = img.shape
        #opencv's shape is y,x,channels
        self._size = (size[1],size[0])

    def img_size(self):
        return self._size

    def fps(self):
        return 20

    def generator(self):
        while True:
            _, img = self.cam.read()
            global M
            img = cv2.warpPerspective(img,M,self._size)
            yield img






print("Create video source")



vidsrc = MyVideoSource()
fvd = virtualvideo.FakeVideoDevice()
fvd.init_input(vidsrc)
fvd.init_output(2, 1920, 1080, pix_fmt='yuyv422')
fvd.run()




