import argparse
 
parser = argparse.ArgumentParser(description='Demo')
parser.add_argument('--integer', '-l', required=True, type=int)
parser.add_argument('--string', required=True)
parser.add_argument('--verbose', '-v',
    action='store_true',
    help='verbose flag' )
 
args = parser.parse_args()
 
if args.verbose:
    print("~ Verbose!")
else:
    print("~ Not so verbose")
