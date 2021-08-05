import sys
import iteractive
import thrdport
import re


def print_hlp():

    s =  '''
    this app bla bla bla
    '''

    print( s )

def handle_opts( opt ):
    pass

def handle_vals( val_lst ):
    pass

def handle_url( url ):

    regex = r''

def handle_input( entry ):
    pass

def valid_input( entry ):
    
    regex = r'^(\-[a-z]+\s)?[\w\.]+(\s\d+)*$'
    pat = re.match( regex , entry )
    return not( pat is None )

def run( f, args ):

    resp = f( *args )
    try:
        for s in resp:
            print( s )
    except KeyboardInterrupt:
        print( "\n ABORTANDO!" )
        sys.exit()

if __name__ == "__main__":

    entry = " ".join( sys.argv[ 1: ] )

    if entry == "--help":
        print_hlp()
    elif valid_input( entry ):
        fun , args =  handle_input( entry )
        run( fun , args )
    else:
        print( "INVALID INPUT" )

    sys.exit()
