"""Utility functions for user detection and alignment"""
import json


def is_user(msg):
    """Function to check for presence of user within camera XZ plane"""
    # convert string to JSON dict
    msg_dict = json.loads(msg)

    # check if there are any people (at all)
    if not 'people' in msg_dict:
        user_id = -1
    else:
        user_id = -1
        for person_id in msg_dict['people'].keys():
            person_x = msg_dict['people'][person_id]['avg_position'][0]
            person_z = msg_dict['people'][person_id]['avg_position'][2]
            if -1500 < person_x < 1800:
                if 1200 < person_z < 5400:
                    user_id = int(person_id)

    return user_id


def user_alignment(msg, person_id):
    """Function to check for user alignment within XZ bounding box"""
    msg_dict = json.loads(msg)

    if not 'people' in msg_dict:
        alignment = 'No users'
    else:
        # check if same person is still in frame
        if not str(person_id) in msg_dict['people']:
            alignment = 'Previous user not found'
        else:
            candidate_position = msg_dict['people'][str(person_id)]['avg_position']
            if candidate_position[0] < -230:
                alignment = 'Left'
            elif candidate_position[0] > 250:
                alignment = 'Right'
            elif candidate_position[2] > 3200:
                alignment = 'Forward'
            elif candidate_position[2] < 1400:
                alignment = 'Backward'
            else:
                alignment = 'Aligned'

    return alignment
