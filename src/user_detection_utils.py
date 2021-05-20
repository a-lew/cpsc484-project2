import json


def is_user(msg):
    # convert string to JSON dict
    msg_dict = json.loads(msg)

    # check if there are any people (at all)
    if not 'people' in msg_dict:
        return -1
    else:
        for person_id in msg_dict['people'].keys():
            person_x = msg_dict['people'][person_id]['avg_position'][0]
            person_z = msg_dict['people'][person_id]['avg_position'][2]
            if person_x > -1500 and person_x < 1800:
                if person_z > 1200 and person_z < 5400:
                    return int(person_id)

        return -1


def user_alignment(msg, person_id):
    msg_dict = json.loads(msg)

    if not 'people' in msg_dict:
        return 'No users'
    else:
        # check if same person is still in frame
        if not str(person_id) in msg_dict['people']:
            return 'Previous user not found'
        else:
            candidate_position = msg_dict['people'][str(person_id)]['avg_position']
            if candidate_position[0] < -230:
                return 'Left'
            elif candidate_position[0] > 250:
                return 'Right'
            elif candidate_position[2] > 3200:
                return 'Forward'
            elif candidate_position[2] < 1400:
                return 'Backward'
            else:
                return 'Aligned'