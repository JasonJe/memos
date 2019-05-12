import os
import pickle
import numpy as np
from PIL import Image
from io import BytesIO

def get_imnp(binary_data):
    image_np = pickle.loads(binary_data)
    return image_np

def object_info(boxes, scores, label_id, label_dict, score_thresh=0.8, max_boxes_to_draw=32,):
    boxes = np.squeeze(boxes)
    scores = np.squeeze(scores)
    label_id = np.squeeze(label_id).astype(np.int32)

    box_info = []
    for (box, score, idx) in zip(boxes, scores, label_id):
        y_min, x_min, y_max, x_max = box
        label = label_dict[idx] if idx in label_dict.keys() else 'N/A'
        if score > score_thresh:
            display_str = '{}: {}%'.format(
                label,
                int(100 * score))
            box_info.append([display_str, score, y_min, x_min, y_max, x_max])

    max_len = min(max_boxes_to_draw, len(boxes))

    box_info = np.array(box_info)
    argsort_key = box_info[:, 1] if len(box_info) != 0 else []
    box_info = box_info[np.argsort(argsort_key, axis=0)]
    box_info = box_info[:max_len].tolist()
    return box_info

def get_roibox(box_info, img, color='red'):
    y_len, x_len = img.shape[:2]

    roi_msg = []
    for i, (display_str, score, y_min, x_min, y_max, x_max) in enumerate(box_info):
        y_min, x_min, y_max, x_max = [float(s) for s in (y_min, x_min, y_max, x_max)]
        pt1 = (int(x_min * x_len), int(y_min * y_len))
        pt2 = (int(x_max * x_len), int(y_max * y_len))

        object = display_str.split(':')[0]
        score = float(display_str.split(':')[-1].replace('%', '')) / 100

        roi_msg.append({
            'xmax': pt2[0],
            'xmin': pt1[0],
            'ymax': pt2[1],
            'ymin': pt1[1],
            'score': score,
            'object': object
        })

    return roi_msg

def label_handle(model_path):
    label_dict = {}
    pbtxt_path = []
    for path in os.walk(model_path):
        file_path = [os.path.join(path[0], file) for file in path[2] if 'pbtxt' in file]
        pbtxt_path.extend(file_path)

    pbtxt_file = pbtxt_path[0]

    with open(pbtxt_file, 'r') as f:
        line = f.readline()
        while line:
            if line == "item {\n":
                key = int(f.readline().split(':')[-1])
                value = f.readline().split(':')[-1][2:-2]
                label_dict[key] = value
            line = f.readline()
    return label_dict

