# Import required modules
import cv2 as cv
import math
import argparse


############ Utility functions ############
def decode(scores, geometry, scoreThresh):
    detections = []
    confidences = []

    ############ CHECK DIMENSIONS AND SHAPES OF geometry AND scores ############
    assert len(scores.shape) == 4, "Incorrect dimensions of scores"
    assert len(geometry.shape) == 4, "Incorrect dimensions of geometry"
    assert scores.shape[0] == 1, "Invalid dimensions of scores"
    assert geometry.shape[0] == 1, "Invalid dimensions of geometry"
    assert scores.shape[1] == 1, "Invalid dimensions of scores"
    assert geometry.shape[1] == 5, "Invalid dimensions of geometry"
    assert scores.shape[2] == geometry.shape[2], "Invalid dimensions of scores and geometry"
    assert scores.shape[3] == geometry.shape[3], "Invalid dimensions of scores and geometry"
    height = scores.shape[2]
    width = scores.shape[3]
    for y in range(0, height):

        # Extract data from scores
        scoresData = scores[0][0][y]
        x0_data = geometry[0][0][y]
        x1_data = geometry[0][1][y]
        x2_data = geometry[0][2][y]
        x3_data = geometry[0][3][y]
        anglesData = geometry[0][4][y]
        for x in range(0, width):
            score = scoresData[x]

            # If score is lower than threshold score, move to next x
            if (score < scoreThresh):
                continue

            # Calculate offset
            offsetX = x * 4.0
            offsetY = y * 4.0
            angle = anglesData[x]

            # Calculate cos and sin of angle
            cosA = math.cos(angle)
            sinA = math.sin(angle)
            h = x0_data[x] + x2_data[x]
            w = x1_data[x] + x3_data[x]

            # Calculate offset
            offset = (
            [offsetX + cosA * x1_data[x] + sinA * x2_data[x], offsetY - sinA * x1_data[x] + cosA * x2_data[x]])

            # Find points for rectangle
            p1 = (-sinA * h + offset[0], -cosA * h + offset[1])
            p3 = (-cosA * w + offset[0], sinA * w + offset[1])
            center = (0.5 * (p1[0] + p3[0]), 0.5 * (p1[1] + p3[1]))
            detections.append((center, (w, h), -1 * angle * 180.0 / math.pi))
            confidences.append(float(score))

    # Return detections and confidences
    return [detections, confidences]


def textDetector(filename, debug=False):
    # Read and store arguments
    confThreshold = 0.5
    nmsThreshold = 0.4
    inpWidth = 320
    inpHeight = 320
    model = "./frozen_east_text_detection.pb"

    # Load network
    net = cv.dnn.readNet(model)

    outNames = []
    outNames.append("feature_fusion/Conv_7/Sigmoid")
    outNames.append("feature_fusion/concat_3")

    frame = cv.imread(filename)
    if frame is None:
        raise Exception("invalid path to input image")

    # Get frame height and width
    height_ = frame.shape[0]
    width_ = frame.shape[1]
    rW = width_ / float(inpWidth)
    rH = height_ / float(inpHeight)

    # Create a 4D blob from frame.
    blob = cv.dnn.blobFromImage(frame, 1.0, (inpWidth, inpHeight), (123.68, 116.78, 103.94), True, False)

    # Run the model
    net.setInput(blob)
    outs = net.forward(outNames)
    t, _ = net.getPerfProfile()
    label = 'Inference time: %.2f ms' % (t * 1000.0 / cv.getTickFrequency())

    # Get scores and geometry
    scores = outs[0]
    geometry = outs[1]
    [boxes, confidences] = decode(scores, geometry, confThreshold)
    if debug:
        # Create a new named window
        kWinName = "EAST: An Efficient and Accurate Scene Text Detector"
        cv.namedWindow(kWinName, cv.WINDOW_NORMAL)

        # show window and bounding boxes for image..

        # Apply NMS
        indices = cv.dnn.NMSBoxesRotated(boxes, confidences, confThreshold, nmsThreshold)
        for i in indices:
            # get 4 corners of the rotated rect
            vertices = cv.boxPoints(boxes[i[0]])
            # scale the bounding box coordinates based on the respective ratios
            for j in range(4):
                vertices[j][0] *= rW
                vertices[j][1] *= rH
            for j in range(4):
                p1 = (vertices[j][0], vertices[j][1])
                p2 = (vertices[(j + 1) % 4][0], vertices[(j + 1) % 4][1])
                cv.line(frame, p1, p2, (0, 255, 0), 1)

        # Put efficiency information
        cv.putText(frame, label, (0, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

        # Display the frame
        cv.imshow(kWinName, frame)
        cv.waitKey(0)
        cv.destroyAllWindows()

    return True if boxes and confidences else False


if __name__ == "__main__":
    isTextPresent = textDetector("test_images/carPlate.jpg")
    print(isTextPresent)
