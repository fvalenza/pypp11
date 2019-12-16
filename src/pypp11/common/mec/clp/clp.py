#!/usr/bin/env python3
import sys


class CLP(object):
    '''
    Command Line Parser
    '''

    '''
     Character for delimiting file names in a list
    '''
    __delimiter = ","

    def __init__(self, argv=None):

        # Initialise arguments
        self.__arguments = []

        if argv is None:
            argv = sys.argv

        for args in argv[1:]:
            self.__arguments.append(args.split(CLP.__delimiter))
        pass

    def run(self):
        print(self.__arguments)
        pass
