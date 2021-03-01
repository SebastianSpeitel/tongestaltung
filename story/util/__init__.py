
def get_tracking_data(binsim, tracker='listener'):
    """
    Fetch the tracking data for listener or controller positions.
    This functions performs a sleep of a micro second to prevent threading locks.

    :param tracker: string -> 'listener' for listener's position, 'controller' for controller's position
    :return: respective data list
    """

    # This functions performs a sleep of a micro second to prevent threading locks.
    time.sleep(10e-6)

    if tracker == 'listener':
        # get tracking data for channel '0' -> except for the channel id tracking data is the same for all channels
        data = []
        data.append(binsim.oscReceiver.valueList[0][1])
        data.append(binsim.oscReceiver.valueList[0][2])
        data.append(binsim.oscReceiver.valueList[0][4])

    elif tracker == 'controller':
        # get tracking data for controller
        data = binsim.oscReceiver.ctrlData[:3]

    else:
        raise TypeError(
            'get_tracking_data() called with invalid tracker-argument. Allowed are: "listener" and "controller".')

    return data


def tracker_in_area(binsim, x_min, y_min, x_max, y_max, tracker='listener'):
    """
    Check whether the tracker is located inside a rectangular area defined by lower and upper edges in terms of
    a column and row identifier. These numerical identifiers relate to the QualiSys tracking data.
    See "Tracking data" comment in line 38.

    :param tracker: string -> 'listener' for listener's position, 'controller' for controller's position
    :return: boolean (True -> tracker is in area, False -> tracker is not in area)
    """

    # get tracking data for channel '0' -> except for the channel id tracking data is the same for all channels
    data = get_tracking_data(binsim, tracker)

    # organize into column and row according to filtermap quadrants (A01...Q17)
    x = data[0]
    y = data[1]

    # compare if  tracker is inside defined area
    if x >= x_min and x <= x_max:
        if y >= y_min and y <= y_max:
            # print('\n TRIGGERED \n') # mainly for debug purposes
            return True
    return False
