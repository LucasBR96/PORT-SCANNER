import time
import socket as sck
from errno import errorcode
import sys

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
    # result = sock.connect_ex( tup )
    result = "SUCCESS"
    try: sock.connect( tup )
    except sck.error as e:
        result = e
    dt = time.time() - t

    #--------------------------------------------------
    # ja tem-se o errno então não precisamos mais do so
    # cket.
    sock.shutdown( sck.SHUT_RDWR )
    sock.close()

    return result , dt

def string_connect_result( port_num , result, dt ):
    
    port_name = sck.getservbyport( port_num ).upper()
    true_time = "{:.5f} seconds".format( dt )
    

    s = "-"*50 + "\n"
    s += "{} {}\n".format( port_num , port_name )

   # se não houve erro, a porta é aberta
    if result == "SUCCESS":
        s += "ABERTA"
   # se ocorrer o timeout do socket ou do sistema, a porta é filtrada
    elif result.__class__ == sck.timeout or result.args[0] == 10060:
        s += "FILTRADA"
   # nos outros erros, a porta é fechada
    else:
        s += "FECHADA"
    s += "\n"
    s += true_time

    return s

def scan_header( host_name, start , end , timeout = 1. , alpha = .15 ):

    host_ip = sck.gethostbyname( host_name )
    s = "\nHost with name \"{}\" have IP of \"{}\"\n".format( host_name , host_ip )
    s += "START {} END {}\n".format( start , end )
    s += "TIMEOUT OF {:.5F} seconds\n".format( timeout )
    s += "ALPHA OF {:.5f}%\n".format( 100*alpha )

    return s

def iteractive_scan( host_name, start , end , timeout = 1. , alpha = .15 ):
    
    '''
    escaneameto de modo iterativo, em contraste com o modo multithread
    '''

    s = scan_header( host_name, start , end , timeout , alpha )
    yield s
    
    host_ip = sck.gethostbyname( host_name )

    #--------------------------------------------------
    # caso aluem troque os valores
    if start > end: start , end = end , start
    summary = {}

    for port_num in range( start , end + 1 ):
        
        #--------------------------------------------------
        # algus valores para porta não tem um protocolo mapeado
        # se for o caso pula-se o numero
        try: sck.getservbyport( port_num )
        except OSError: continue

        result , dt = try_connect( port_num, host_ip, timeout )
        s = string_connect_result( port_num, result, dt )
        yield s

        #--------------------------------------------------
        # recomputando timeout
        timeout = ( 1 - alpha )*timeout + alpha*dt

        #--------------------------------------------------
        # salvando resultados na para summrizar
        summary[ result ] = summary.get( result , 0 ) + 1


if __name__ == "__main__":

    s = "g1.globo.com"
    start , end = 80 , 1024
    t = 1.
    
    
    resp = iteractive_scan( s , start, end, timeout = t, alpha = .1 )
    try:
        for s in resp:
            print( s )
    except KeyboardInterrupt:
        print( "\n ABORTANDO!" )
        sys.exit()


