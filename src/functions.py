import time
import socket as sck
from errno import errorcode
import sys
import re

def try_connect( port_num , host_ip , timeout = 1. ):

    #--------------------------------------------------
    # Cria um novo socket para testar a conexão. Como
    # não é possível mudar a porta para um mesmo socket
    # e necessário criar um novo para cada porta
    sock = sck.socket( sck.AF_INET , sck.SOCK_STREAM )
    sock.settimeout( timeout )
    tup = ( host_ip , port_num )
    #--------------------------------------------------

    #--------------------------------------------------
    # Tentando conexão, o tempo é medido para calibrar o
    # valor de timeout na proxima tentativa
    t = time.time()
    result = "ABERTA"
    try: sock.connect( tup )
    except sck.error as e:
        result = "FECHADA"
        if e.__class__ == sck.timeout or e.__class__ == TimeoutError:
            result = "FILTRADA"
    else:
        # ja tem-se o errno então não precisamos mais do so
        # cket.
        sock.shutdown( sck.SHUT_RDWR )
    dt = time.time() - t

    sock.close()

    return result , dt

def string_connect_result( port_num , result, dt ):
    
    try:
        port_name = sck.getservbyport( port_num ).upper()
    except OSError:
        port_name = "NO SERVICE"
    true_time = "{:.5f} seconds".format( dt )
    

    s = "-"*50 + "\n"
    s += "PORT {}: {}\n".format( port_num , port_name )
    s += result + "\n"
    s += true_time

    return s

def scan_header( host_name, start , end , timeout = 1.):

    host_ip = sck.gethostbyname( host_name )
    s = "\nHost \"{}\" have IP of \"{}\"\n".format( host_name , host_ip )
    s += "START {} END {}\n".format( start , end )
    s += "TIMEOUT OF {:.5F} seconds\n".format( timeout )

    return s

def summary_str( summary ):

    s = "\n" + "-"*50 + "\n"
    s += "\nSUMMARY OF PORT SCANNING\n"
    for result , freq in summary.items():
        s += "{} {}\n".format( result , freq )
    return s


def iteractive_scan( host_name, start , end , timeout):
    
    '''
    escaneameto de modo iterativo, em contraste com o modo multithread
    '''

    s = scan_header( host_name, start , end , timeout)
    yield s
    
    host_ip = sck.gethostbyname( host_name )

    #--------------------------------------------------
    # caso aluem troque os valores
    if start > end: start , end = end , start
    summary = {}

    for port_num in range( start , end + 1 ):

        result , dt = try_connect( port_num, host_ip, timeout )
        s = string_connect_result( port_num, result, dt )
        yield s

        #--------------------------------------------------
        # salvando resultados na para summrizar
        summary[ result ] = summary.get( result , 0 ) + 1
    yield summary_str( summary )

def handle_input( input_lst ):

    '''
    Os tipos de entradas aceitas:

    HOSTNAME [START] [END] [TIMEOUT] [ALPHA]
    '''

    host_regex = re.compile( r'\b[\w\.]+\b' )
    host_name = host_regex.match( input_lst[ 0 ] )[ 0 ]

    start = 1
    if len( input_lst ) > 1:
        start = max( 1 , int( input_lst[ 1 ] ) )

    end = 65535
    if len( input_lst ) > 2:
        end = min( 65535 , int( input_lst[ 2 ] ) )

    timeout = 22.
    if len( input_lst ) > 3:
        timeout = max( 3. , float( input_lst[ 3 ] ) )
    
    return host_name , start , end , timeout

if __name__ == "__main__":
    
    #--------------------------------------------------
    # s = "g1.globo.com"
    # start , end = 80 , 2048
    # t = 1.
    # 
    # 
    # resp = iteractive_scan( s , start, end, timeout = t, alpha = .1 )
    # try:
    #     for s in resp:
    #         print( s )
    # except KeyboardInterrupt:
    #     print( "\n ABORTANDO!" )
    #     sys.exit()

    s , start , end , t = handle_input( sys.argv[ 1: ] )
    resp = iteractive_scan( s , start, end, timeout = t)
    try:
        for s in resp:
            print( s )
    except KeyboardInterrupt:
        print( "\n ABORTANDO!" )
        sys.exit()

