import datetime


def convert_iso_time(isotime):
    """Will convert an isotime (string) to datetime.datetime"""
    return datetime.strptime(isotime,"%Y%m%dT%H%M%S.%fZ")


def dict_array(array):
    """Will convert all items in an array to dict objects"""
    output = []
    if array is not None:
        for item in array:
            output.append(dict(item))
    else:
        output = None
    return output


def class_array(class_object, data_array):
    """Will convert all data in an array to the specified class in a new array"""
    output = []
    if data_array is not None:
        for item in data_array:
            output.append(class_object(item))
    return output
