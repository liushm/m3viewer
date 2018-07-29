#!/usr/bin/python3
# -*- coding: utf-8 -*-

import m3
import sys

def doit(structureName, structureVersion):
    structureDescription = m3.structures[structureName].getVersion(structureVersion)
    if structureDescription == None:
        raise Exception("The structure %s hasn't been defined in version %d" % (structureName, structureVersion))
    offset = 0
    print('---------- ' + structureName + ' v ' + str(structureVersion) + ' ----------')
    for field in structureDescription.fields:
        print("{:4d}: {}".format(offset, field.name))
        offset += field.size

if __name__ == '__main__':
    if len(sys.argv) == 3:
        doit(sys.argv[1], int(sys.argv[2]))

    doit('MODL', 29)
    doit('MD34', 11)
    doit('REGN', 4)
