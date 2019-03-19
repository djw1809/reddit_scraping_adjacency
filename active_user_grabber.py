

import operator



def dictconverter(name_list):
    intermediate_dict = {}

    for key in name_list.iterkeys():
        value = name_list[key]
        submission_value = value[0]
        intermediate_dict[key] = submission_value

    return intermediate_dict

def activeusergrabber(name_list,int_dict):
    limit = int(raw_input("How many of the top active users do you want to grab?"))
    ###Grab top users from intermediate dictionary
    new_dict = dict(sorted(int_dict.iteritems(), key=operator.itemgetter(1), reverse=True)[:limit])

    ###Give their values the right formatting
    for key in new_dict.iterkeys():
        new_dict[key]=name_list[key]

    return new_dict
