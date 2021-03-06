#!/usr/bin/python

# printtopics.py: Prints the words that are most prominent in a set of
# topics.
#
# Copyright (C) 2010  Matthew D. Hoffman
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys, os, re, random, math, urllib2, time, cPickle
import numpy as np
from collections import defaultdict


def main():
    """
    Displays topics fit by onlineldavb.py. The first column gives the
    (expected) most prominent words in the topics, the second column
    gives their (expected) relative prominence.
    """
    vocab = [f.strip() for f in file(sys.argv[1]).readlines()]
    print len(vocab)
    betafile = np.loadtxt(sys.argv[2])

    testlambda = np.zeros((100, 21945))
    #testlambda = np.zeros((100, 6293))
    #testlambda = np.zeros((2, 24))
    for v in range(len(betafile)):
        #testlambda[:,int(betafile[v,1])] = betafile[v,2:]
        testlambda[:,int(betafile[v,0])] = betafile[v,1:]
    '''if len(sys.argv) == 5:
        k = int(sys.argv[4])
        lambdak = list(testlambda[k, :])
        lambdak = lambdak / sum(lambdak)
        temp = zip(lambdak, range(0, len(lambdak)))
        temp = sorted(temp, key = lambda x: x[0], reverse=True)
        print 'topic %d:' % (k)
        # feel free to change the "53" here to whatever fits your screen nicely.
        for i in range(0, int(sys.argv[3])):
            print '%20s  \t---\t  %.4f' % (vocab[temp[i][1]], temp[i][0])
        return''' # single topic: obsolete
    frequency = {}
    exclusivity = defaultdict(dict)
    V = testlambda.shape[1]
    #print V, "vocab size"

    for k in range(0, len(testlambda)):
        lambdak = testlambda[k, :]
        lambdak = lambdak / sum(lambdak)
        lambdak = np.array(lambdak)
        lambdak[lambdak==np.inf] = 0
        frequency[k] = lambdak
    for v in range(V):
        total = 0.
        for k in range(len(frequency)):
            total += frequency[k][v]
        for k in range(len(frequency)):
            if total == 0:
                exclusivity[k][v] = 0
                #print vocab[v]
            else:
                exclusivity[k][v] = frequency[k][v] / total

    Fcdf = {}
    Ecdf = {}
    for k in range(0, len(testlambda)):
        temp = zip(list(frequency[k]), range(0, len(lambdak)))
        temp = sorted(temp, key = lambda x: x[0], reverse=True)
        Fcdf[k] = {}
        cv = 0
        for val,idx in temp:
            cv += val
            Fcdf[k][idx] = cv

        ex = [exclusivity[k][v] for v in range(V)]
        temp = zip(ex, range(0, len(lambdak)))
        temp = sorted(temp, key = lambda x: x[0], reverse=True)
        Ecdf[k] = {}
        cv = 0
        for val,idx in temp:
            cv += val
            Ecdf[k][idx] = cv

    for k in range(0, len(testlambda)):
        temp = sorted(range(V), key = lambda v: 1./((0.5/Ecdf[k][v]) + (0.5/Fcdf[k][v])), reverse=False)
        terms = ', '.join(['%s' % vocab[temp[i]] for i in range(int(sys.argv[3]))])
        print '%d H\t%s' % (k, terms)#, 1./((0.5/Ecdf[k][v]) + (0.5/Fcdf[k][v])))

        temp = sorted(range(V), key = lambda v: 1./((0.0/Ecdf[k][v]) + (1.0/Fcdf[k][v])), reverse=False)
        terms = ', '.join(['%s' % vocab[temp[i]] for i in range(int(sys.argv[3]))])
        print '%d F\t%s' % (k, terms)#, 1./((0.5/Ecdf[k][v]) + (0.5/Fcdf[k][v])))

        temp = sorted(range(V), key = lambda v: 1./((1.0/Ecdf[k][v]) + (0.0/Fcdf[k][v])), reverse=False)
        terms = ', '.join(['%s' % vocab[temp[i]] for i in range(int(sys.argv[3]))])
        print '%d E\t%s' % (k, terms)#, 1./((0.5/Ecdf[k][v]) + (0.5/Fcdf[k][v])))


if __name__ == '__main__':
    main()
