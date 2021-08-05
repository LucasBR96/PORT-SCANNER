import sys
import iteractive
import thrdport
import re


def print_hlp():

    s =  '''usage:
    pscan --help
    pscan [ options ] url [ start ] [ end ] [ timeout ]
    
    url   -> the url of the target host

    start -> the first port number to be scanned
             default 1.

    end   -> last to be scanned ( inclusive )
             default 65535.

    timeout -> the amount of time ( in seconds ) to wait 
               for target's response before giving the connection up.
               default = 22, min = 3

    options are:

        s -> if no protocol is known for a given port number
             do not try to connect

    '''

    print( s )

def handle_opts( opt ):
    
    foo = iteractive.iteractive_scan

    must_serv = False
    if opt == "-s":
        must_serv = True

    def fun( args ):
        host_name , start , end , timeout = args
        return foo( host_name , start , end , timeout, must_serv )
    return fun

def handle_vals( val_lst ):
    pass

def handle_input( entry ):
    
    option_pat = r'\-[a-z]+(?=\s)'
    s = re.search( option_pat , entry )
    opt_str = ""
    if not( s is None ):
        opt_str = s.group( 0 )
    # print( opt_str )
    # f = handle_opts( opt_str )

    url_pat = r'((\w+\.)+\w+)\b'
    s = re.search( url_pat , entry )
    url_str = "localhost"
    if not( s is None ):
        url_str = s.groups( 0 )[0]
    # print( url_str )

    values_pat = r'((\s\d+){,3})$'
    s = re.search( values_pat , entry )
    values_str = ""
    if not( s is None ):
        values_str = s.groups( 0 )[0]
    print( values_str )


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
    print( entry )

    if entry == "--help":
        print_hlp()
    elif valid_input( entry ):
        fun , args =  handle_input( entry )
        run( fun , args )
    else:
        print( "INVALID INPUT" )

    sys.exit()
