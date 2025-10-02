import cv2


def draw_frame(frame, terry):
    myframe = frame.copy()
    # cv2.rectangle(myframe, ())
    if terry is not None:
        cv2.rectangle(myframe, terry[0:2], terry[2:], (0, 0, 255), 2)
    return myframe


def join_detections(result):
    detections = result.boxes.xyxy.cpu().numpy()
    if detections.shape[0] == 0:
        return None
    if detections.shape[0] >= 1:
        bbox = detections.max(axis=0)
        bbox = bbox.astype("int")
    return bbox
