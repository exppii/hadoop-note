#!/usr/bin/env python
import os
import sys, getopt


def main(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print 'test.py -i <inputfile> -o <outputfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'test.py -i <inputfile> -o <outputfile>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   print ("rsync -avhP -e ssh {} slave1.dream:{}". format(inputfile,outputfile))
   # os.system("rsync -avhP -e ssh {} slave1.dream:{}". format(inputfile,outputfile))
   # os.system("rsync -avhP -e ssh {} slave2.dream:{}". format(inputfile,outputfile))
   # os.system("rsync -avhP -e ssh {} slave3.dream:{}". format(inputfile,outputfile))
   # os.system("rsync -avhP -e ssh {} zookeeper.dream:{}". format(inputfile,outputfile))

if __name__ == "__main__":
   main(sys.argv[1:])
