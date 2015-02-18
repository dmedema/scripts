#!/usr/bin/python

# This is an example of using getopt for parsing command line arguments
# sys.argv[0] is the name of the script

import getopt, sys
 
def main(argv):
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:v", ["help", "output="])
    except getopt.GetoptError, err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    output = None
    verbose = False
    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-o", "--output"):
            output = a
        else:
            assert False, "unhandled option"
def usage():
    usage = "getopt.py opt1 opt2 opt3 [opt4 ...]"
    opt1    "tenant name (t501)"
    opt2    "description of the tenant"
    opt3    "subnet1 (10.71.0.0/22)"
    opt4    "subnet2 (10.73.100.0/22)"
    opt5    "subnet3 (10.73.128.0/22)"
    print usage
 
if __name__ == "__main__":
    main(sys.argv[1:]) #slices off the first argument which is the name of the program
