import praw
import csv
import numpy
from ast import literal_eval as make_tuple


def array_maker(dict):
    # Find how many users there are
    key_list = []
    for key in dict.keys():
        tuple1 = make_tuple(key)
        key_list.append(tuple1[0])
        key_list.append(tuple1[1])

    dimension = max(key_list)

# Fill out matrix
    adjacency_m = numpy.zeros( (dimension+1, dimension+1))
    for key in dict.keys():
        place = make_tuple(key)
        adjacency_m[place[0],place[1]] = dict[key]
        print '(%r, %r) = %r' % (place[0], place[1], adjacency_m[place[0],place[1]])

    symmetry = raw_input("Do you want to symmetrize?")
# symmetrize optionally
    if symmetry == 'yes':
        index = range(0,dimension+1)
        for i in index:
            for j in index:
                if j > i:
                    adjacency_m[i,j] = adjacency_m[i,j] + adjacency_m[j,i]
                    adjacency_m[j,i] = adjacency_m[i,j]

                print '(%r, %r) = %r' % (i, j, adjacency_m[i,j])
            else:
                pass
        print 'Done'

    else:
        print 'Done'

# write to csv file
    name_input = raw_input("What would you like to name the output file containing the adjacency data?")
    name = str(name_input)

    numpy.savetxt(name_input+'.csv', adjacency_m, delimiter =",")

    return adjacency_m
