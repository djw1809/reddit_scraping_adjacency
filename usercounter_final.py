import praw
import os
import csv
###Create authorized reddit instance
username='djw009'
password='lifegood1'
client_id='cGP7e8gMlUqQwQ'
client_secret='_6Jzg7g8AwHSvuDJCg4WdTIkmmU'

reddit = praw.Reddit(client_id=client_id, client_secret=client_secret,
                    password=password, user_agent='<Python>:<cGP7e8gMlUqQwQ>:<v 1.0>(by /u/djw009)',
                    username=username)
#####

def add_ID_to_submission_list():
    """amends a detected users list of submission IDS"""
    submissionlist = open(foldername+'/'+name+'.txt',"a")
    submissionlist.write('%s \n' % str(submission.id))
    submissionlist.close()


target = raw_input("What subreddit would you like to scrape?")


filename_input = raw_input("What would you like to name the write file?")
filename = str(filename_input)

foldername_input = raw_input("What would you like to name the folder to store submission IDs?")
foldername=str(foldername_input)

os.makedirs(foldername)

user_count = 1
name_list = {}


for submission in reddit.subreddit(target).stream.submissions():
    name = str(submission.author.name)

    if name in name_list:
        value = name_list[name]
        submission_count = value[0]
        submission_count = submission_count + 1
        value[0] = submission_count
        name_list[name] = value
        add_ID_to_submission_list()
        print "%r\'s count is %r" % (name, value[0])

    elif name not in name_list:
        name_list[name] = [1,user_count]
        add_ID_to_submission_list()
        user_count = user_count+1
        print "%r is a new submitter" % (name)

    else:
        print "This should never happen"

    with open(filename+'.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in name_list.items():
            writer.writerow([key, value])
