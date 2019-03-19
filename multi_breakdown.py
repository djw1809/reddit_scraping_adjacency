import praw
import csv
import numpy
import math
from ast import literal_eval as make_tuple
err_count = 0

def createredditinstance(username,password,client_id, client_secret):
    reddit = praw.Reddit(client_id=client_id, client_secret=client_secret,
                        password=password, user_agent='<Python>:<%r>:<v 1.0>(by /u/%r)' %(client_id, username),
                        username=username)

    print "You have a reddit instance stored to the variable reddit with the user %r" % (username)
    return reddit

def dictpopper(dic,limit):
    minidict = dict(dic.items()[0:limit])

    for key in minidict.iterkeys():
        dic.pop(key)

    return minidict

def dictbreaker(name_list, limit):
    minidict1 = dictpopper(name_list, limit)
    minidict2 = dictpopper(name_list, limit)
    minidict3 = dictpopper(name_list, limit)
    minidict4 = dictpopper(name_list, limit)
    minidict5 = dictpopper(name_list, limit)
    minidict6 = dictpopper(name_list, limit)
    minidict7 = dictpopper(name_list, limit)
    minidict8 = dictpopper(name_list, limit)
    minidict9 = dictpopper(name_list, limit)
    minidict10 = dictpopper(name_list, limit)

    return minidict1, minidict2, minidict3, minidict4, minidict5, minidict6, minidict7, minidict8, minidict9, minidict10


def listofdicts_writer(bigdict):
    number_of_dicts_input = raw_input("How many nonempty dictionaries are in the list?")
    number = int(number_of_dicts_input)
    name_list = []
    for i in range(0,number):
        name_list.append('%r' % (i))


    for dic in bigdict[0:number]:
        name = name_list.pop(0)
        with open(name +'.csv', 'w') as csv_file:
            writer = csv.writer(csv_file)
            for key, value in dic.items():
                writer.writerow([key, value])







def miniscraper(redditinstance, name_list, minidict):
    global err_count
    filename = raw_input('What would like to call the .csv file that the tuple list gets written to?')
    stuff_limit = 1000
    tuple_list={}

    for key in minidict.iterkeys():
        try:
            submission_reply_list = {}
            comment_reply_list = {}

            #submission_filename = key + '_submission_repliers'

            #comment_filename = key + '_comment_repliers'

            target = redditinstance.redditor(str(key))
            target_redditor = str(target)

            #grab submissions of target

        except:
            print "error in naming files"
            err_count = err_count + 1
            quit()

        submissions = target.submissions.new(limit=stuff_limit)

        #grab authors of top level comments to all submissions
        for submission in submissions:
            try:
                submission.comments.replace_more(limit=0)
                for comment in submission.comments:
                        name = str(comment.author)

                        if name in submission_reply_list:
                            submission_reply_list[name] = submission_reply_list[name] + 1
                            print "%r has been a top level replier to %r %r times" % (name, target_redditor, submission_reply_list[name])

                        elif name not in submission_reply_list:
                            submission_reply_list[name] = 1
                            print "%r has been a top level replier to %r %r times" % (name, target_redditor, submission_reply_list[name])

                        else:
                            pass
                            print "This should never happen"
            except:
                print "Something went wrong pulling a submission author"
                err_count = err_count+1
                continue

        #grab comments of target
        comments = target.comments.new(limit=stuff_limit)


        #collects authors to top level replies to all comments
        for comment in comments:
            try:
                comment.refresh()
                comment.replies.replace_more()
                for reply in comment.replies:
                    name = str(reply.author)

                    if name in comment_reply_list:
                        comment_reply_list[name] = comment_reply_list[name] + 1
                        print "%r has replied to a comment by %r %r times" % (name, target_redditor, comment_reply_list[name])

                    elif name not in comment_reply_list:
                        comment_reply_list[name] = 1
                        print "%r has replied to a comment by %r %r times" % (name, target_redditor, comment_reply_list[name])

                    else:
                        print "This should never happen, something is broken, quitting now."
                        continue
            except:
                    err_count=err_count+1
                    continue
        #writes lists to csv files  comment out later, will use to check output
        #with open(submission_filename +'.csv', 'w') as csv_file:
            #writer = csv.writer(csv_file)
            #for key, value in submission_reply_list.items():
                #writer.writerow([key, value])

        #with open(comment_filename +'.csv', 'w') as csv_file:
            #writer = csv.writer(csv_file)
            #for key, value in comment_reply_list.items():
                #writer.writerow([key, value])
        #print "error count is %r" % (err_count)

        #creates dictionary and array with adjacency matrix entries

        dict_value = name_list[target_redditor]
        tuple_value1 = dict_value[1]


        for user in submission_reply_list.iterkeys():

            if user in name_list.keys():
                dict_value = name_list[str(user)]
                tuple_value2 = dict_value[1]
                matrix_entry = (tuple_value1, tuple_value2)
                tuple_list[matrix_entry] = submission_reply_list[user]
                print "the value of the %r entry of the adjacency matrix is %r" % (matrix_entry , tuple_list[matrix_entry])

            else:
                print "%r is not part of the target community" % (user)
                pass

        for user in comment_reply_list.iterkeys():

            if user in name_list.keys():
                dict_value = name_list[str(user)]
                tuple_value2 = dict_value[1]
                matrix_entry = (tuple_value1, tuple_value2)

                if matrix_entry in tuple_list.keys():
                    tuple_list[matrix_entry] = tuple_list[matrix_entry] + comment_reply_list[user]
                    print "the value of the %r entry of the adjacency matrix is %r" % (matrix_entry , tuple_list[matrix_entry])

                elif matrix_entry not in tuple_list.keys():
                    tuple_list[matrix_entry] = comment_reply_list[user]
                    print "the value of the %r entry of the adjacency matrix is %r" % (matrix_entry , tuple_list[matrix_entry])

                else:
                    print "This should never happen, something is broken"
                    pass
            else:
                print "%r is not part of the target community" % (user)
                pass


    with open(filename +'.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in tuple_list.items():
            writer.writerow([key, value])

    return tuple_list


def tuplemerger(tuple0, tuple1, tuple2, tuple3, tuple4, tuple5, tuple6, tuple7, tuple8):

    inputs = [tuple0, tuple1, tuple2, tuple3, tuple4, tuple5, tuple6, tuple7, tuple8]
    tuple_list = tuple0


    for i in range(1,9):

        current_tuple = inputs[i]

        for key in current_tuple.iterkeys():
            if key in tuple_list.keys():
                tuple_list[key] = tuple_list[key] + current_tuple[key]

            elif key not in tuple_list.keys():
                tuple_list[key] = current_tuple[key]

            else:
                print "something is broken"
                quit()


    return tuple_list

def writecsv(dict):

    filename = raw_input("What would you like to name the output csv file")

    with open(filename +'.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in submission_reply_list.items():
            writer.writerow([key, value])


def load_andconvert_namelists_todict(name):

    reader = csv.reader(open(name , 'r'))
    dictionary = dict(reader)

    for key in dictionary.iterkeys():
        value = dictionary[key]
        new_value = make_tuple(value)
        dictionary[key] = new_value

    return dictionary

def bot_scrape():
    username = raw_input("What is the bots username")
    password = raw_input("What is the bots password?")
    client_id = raw_input("What is the bots client_id?")
    client_secret = raw_input("What is the bots client_secret?")
    mininame = raw_input("What is the name of the csv file containing the minidictionary?")
    bigname = raw_input("What is the name of the csv file containing the name_list?")

    reddit = createredditinstance(username, password, client_id, client_secret)
    minidictionary = load_andconvert_namelists_todict(mininame)
    name_list = load_andconvert_namelists_todict(bigname)
    tuple_list = miniscraper(reddit, name_list, minidictionary)

    return tuple_list



# name = raw_input("What is the name of the csv file youd like to load the name list from?")
#
#
# name_list = {}
#
# #imports csv file to a dictionary
# reader = csv.reader(open(name , 'r'))
# name_list = dict(reader)
#
# #Changes the values in the dict from strings to readable tuples:
# for key in name_list.iterkeys():
#     value = name_list[key]
#     new_value = make_tuple(value)
#     name_list[key] = new_value
#
# #Creates reddit instances for all bots
#
# reddit1 = createredditinstance('djw009','lifegood1','cGP7e8gMlUqQwQ', '_6Jzg7g8AwHSvuDJCg4WdTIkmmU')
# reddit2 = createredditinstance('djw0001', 'Abcd354112', 'wHQBw6Nmuju0eg','EHUolAW_SU7QrBh6rbP-Nie7FtI')
# reddit3 = createredditinstance('djw0002', 'Abcd354112', 'pjTn6xwtCFvBnw', 'lh2rAHEWp9SffwlzpKpJjhSuvzA')
# reddit4 = createredditinstance('djw0003', 'Abcd354112', 'fhMwI1iK3rsL9A', 'leSv9bBiYgpaUcI707AtFC-o2DU')
# reddit5 = createredditinstance('djw0004', 'Abcd354112', 'URRTUNFN6_pOZA', 'WUvwzUl6wwPN1qvpiBAw1N9A8ic')
# reddit6 = createredditinstance('djw0005', 'Abcd354112', 'AgFxY0gk1bhhfQ', 'd8nNyGChcE1YEyF_tMY2z7Rv-ds')
# #reddit7 =
# #reddit8 =
# #reddit9 =
# #reddit10 =
#
# #creates smaller dictionaries each to be given to a reddit instance above
# number_of_dicts_input = raw_input("How many different instances of reddit are you using?")
# number = int(number_of_dicts_input)
# limit = int(math.ceil(len(name_list.keys())/number))
#
# minidicts = dictbreaker(name_list, limit)
#
# #creates a tuple list from each smaller dictionary
# tuple1 = miniscraper(reddit1, name_list, minidicts[0])
# tuple2 = miniscraper(reddit2, name_list, minidicts[1])
# tuple3 = miniscraper(reddit3, name_list, minidicts[2])
# tuple4 = miniscraper(reddit4, name_list, minidicts[3])
# tuple5 = miniscraper(reddit5, name_list, minidicts[4])
# tuple6 = miniscraper(reddit6, name_list, minidicts[5])
#
# tuple_list = tuplemerger(tuple1, tuple2, tuple3, tuple4, tuple5, tuple6)
