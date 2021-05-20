"""Functions to compute pose similarity and matching"""
import json
import random

import numpy as np


def pose_similarity(source_pose_keypoints, found_pose_keypoints):
    """Function to compute inverse cosine similarity between two keypoints"""
    found_pose_vec = np.zeros(51)
    source_pose_vec = np.zeros(51)
    root = (0, 0)
    source_root = (0, 0)

    for keypoint_id in found_pose_keypoints.keys():
        if keypoint_id == 'LShoulder':
            if root == (0,0):
                root = (found_pose_keypoints[keypoint_id][0], found_pose_keypoints[keypoint_id][1])
                found_pose_vec[15] = 0.0000000001
                found_pose_vec[16] = 0.0000000001
                source_root = (source_pose_keypoints[15], source_pose_keypoints[16])
                source_pose_vec[15] = 0.0000000001
                source_pose_vec[16] = 0.0000000001
            else:
                found_pose_vec[15] = found_pose_keypoints[keypoint_id][0] - root[0]
                found_pose_vec[16] = found_pose_keypoints[keypoint_id][1] - root[1]
                source_pose_vec[15] = source_pose_keypoints[15] - source_root[0]
                source_pose_vec[16] = source_pose_keypoints[16] - source_root[1]
        elif keypoint_id == 'RShoulder':
            if root == (0,0):
                root = (found_pose_keypoints[keypoint_id][0], found_pose_keypoints[keypoint_id][1])
                found_pose_vec[18] = 0.0000000001
                found_pose_vec[19] = 0.0000000001
                source_root = (source_pose_keypoints[18], source_pose_keypoints[19])
                source_pose_vec[18] = 0.0000000001
                source_pose_vec[19] = 0.0000000001
            else:
                found_pose_vec[18] = found_pose_keypoints[keypoint_id][0] - root[0]
                found_pose_vec[19] = found_pose_keypoints[keypoint_id][1] - root[1]
                source_pose_vec[18] = source_pose_keypoints[18] - source_root[0]
                source_pose_vec[19] = source_pose_keypoints[19] - source_root[1]
        elif keypoint_id == 'LElbow':
            found_pose_vec[21] = found_pose_keypoints[keypoint_id][0] - root[0]
            found_pose_vec[22] = found_pose_keypoints[keypoint_id][1] - root[1]
            source_pose_vec[21] = source_pose_keypoints[21] - source_root[0]
            source_pose_vec[22] = source_pose_keypoints[22] - source_root[1]
        elif keypoint_id == 'RElbow':
            found_pose_vec[24] = found_pose_keypoints[keypoint_id][0] - root[0]
            found_pose_vec[25] = found_pose_keypoints[keypoint_id][1] - root[1]
            source_pose_vec[24] = source_pose_keypoints[24] - source_root[0]
            source_pose_vec[25] = source_pose_keypoints[25] - source_root[1]
        elif keypoint_id == 'LWrist':
            found_pose_vec[27] = found_pose_keypoints[keypoint_id][0] - root[0]
            found_pose_vec[28] = found_pose_keypoints[keypoint_id][1] - root[1]
            source_pose_vec[27] = source_pose_keypoints[27] - source_root[0]
            source_pose_vec[28] = source_pose_keypoints[28] - source_root[1]
        elif keypoint_id == 'RWrist':
            found_pose_vec[30] = found_pose_keypoints[keypoint_id][0] - root[0]
            found_pose_vec[31] = found_pose_keypoints[keypoint_id][1] - root[1]
            source_pose_vec[30] = source_pose_keypoints[30] - source_root[0]
            source_pose_vec[31] = source_pose_keypoints[31] - source_root[1]
        elif keypoint_id == 'LHip':
            found_pose_vec[33] = found_pose_keypoints[keypoint_id][0] - root[0]
            found_pose_vec[34] = found_pose_keypoints[keypoint_id][1] - root[1]
            source_pose_vec[33] = source_pose_keypoints[33] - source_root[0]
            source_pose_vec[34] = source_pose_keypoints[34] - source_root[1]
        elif keypoint_id == 'RHip':
            found_pose_vec[36] = found_pose_keypoints[keypoint_id][0] - root[0]
            found_pose_vec[37] = found_pose_keypoints[keypoint_id][1] - root[1]
            source_pose_vec[36] = source_pose_keypoints[36] - source_root[0]
            source_pose_vec[37] = source_pose_keypoints[37] - source_root[1]
        elif keypoint_id == 'LKnee':
            found_pose_vec[39] = found_pose_keypoints[keypoint_id][0] - root[0]
            found_pose_vec[40] = found_pose_keypoints[keypoint_id][1] - root[1]
            source_pose_vec[39] = source_pose_keypoints[39] - source_root[0]
            source_pose_vec[40] = source_pose_keypoints[40] - source_root[1]
        elif keypoint_id == 'RKnee':
            found_pose_vec[42] = found_pose_keypoints[keypoint_id][0] - root[0]
            found_pose_vec[43] = found_pose_keypoints[keypoint_id][1] - root[1]
            source_pose_vec[42] = source_pose_keypoints[42] - source_root[0]
            source_pose_vec[43] = source_pose_keypoints[43] - source_root[1]
        elif keypoint_id == 'LAnkle':
            found_pose_vec[45] = found_pose_keypoints[keypoint_id][0] - root[0]
            found_pose_vec[46] = found_pose_keypoints[keypoint_id][1] - root[1]
            source_pose_vec[45] = source_pose_keypoints[45] - source_root[0]
            source_pose_vec[46] = source_pose_keypoints[46] - source_root[1]
        elif keypoint_id == 'RAnkle':
            found_pose_vec[48] = found_pose_keypoints[keypoint_id][0] - root[0]
            found_pose_vec[49] = found_pose_keypoints[keypoint_id][1] - root[1]
            source_pose_vec[48] = source_pose_keypoints[48] - source_root[0]
            source_pose_vec[49] = source_pose_keypoints[49] - source_root[1]

    # mask new vectors
    found_vec = found_pose_vec[15:]
    source_vec = source_pose_vec[15:]
    pose_distance = 1 - (np.dot(found_vec.T, source_vec) / \
                    (np.linalg.norm(found_vec)*np.linalg.norm(source_vec)))
    return pose_distance


def match_pose(msg, person_id, dataset):
    """ Given a pose and a dataset of pre-computed poses,
        find the best matching pose from the dataset """

    # get the pose from the frame / msg
    msg_dict = json.loads(msg)

    # check for person_id
    if not 'people' in msg_dict:
        matching_record = dataset[random.randint(0, len(dataset)-1)]
    else:
        if not str(person_id) in msg_dict['people']:
            matching_record = dataset[random.randint(0, len(dataset)-1)]
        else:
            minimum_pose_dict = {}
            person_keypoints = msg_dict['people'][str(person_id)]['keypoints']
            for i, source_art in enumerate(dataset):
                minimum_pose_dict[i] = pose_similarity(source_art['keypoints'], person_keypoints)

            # sort minimum_pose_dict by Value
            sorted_minimum_pose = sorted(minimum_pose_dict.items(), key=lambda kv: kv[1])
            # pick a random key from top 15
            matching_record = dataset[sorted_minimum_pose[random.randint(0,15)][0]]
    return matching_record
