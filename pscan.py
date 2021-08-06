import time
import socket as sck
import sys
import re
import threading as thrd

# FUNÇOES COMUNS ------------------------------------------------------------------------------------
def try_connect( port_num , host_ip , timeout = 1. ):

    #--------------------------------------------------
    # Cria um novo socket para testar a conexão. Como
    # não é possível mudar a porta para um mesmo socket
    # e necessário criar um novo para cada porta
    sock = sck.socket( sck.AF_INET , sck.SOCK_STREAM )
    sock.settimeout( timeout )
    tup = ( host_ip , port_num )

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
    dt = time.time() - t

    sock.close()

    return result , dt

def check_service( num ):

    #--------------------------------------------------
    # verifica se existe um protocolo conhecido para o
    # numero de porta
    try: sck.getservbyport( num ).upper()
    except OSError: return False
    return True

def string_connect_result( port_num , result, dt ):
    
    port_name = "NO SERVICE"
    if check_service( port_num ):
        port_name = sck.getservbyport( port_num ).upper()
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


# PARA O MODO ITERATIVO -----------------------------------------------------------------------------
def iteractive_scan( host_name, start , end , timeout, must_serv = True ):
    
    '''
    escaneameto de modo iterativo, em contraste com o modo multithread
    para ambos, os argumentos:

    host_name -> url
    start     -> primeiro numero de porta a ser explorado
    end       -> ultimo numero de porta a ser explorado
    timeout   -> tempo maximo para a conexão
    must_serv -> se o numero de porta não existir, pular o teste
    '''

    s = scan_header( host_name, start , end , timeout)
    yield s
    
    host_ip = sck.gethostbyname( host_name )

    #--------------------------------------------------
    # caso aluem troque os valores
    if start > end: start , end = end , start
    summary = {}

    for port_num in range( start , end + 1 ):
        
        if must_serv and not( check_service( port_num ) ): continue

        result , dt = try_connect( port_num, host_ip, timeout )
        s = string_connect_result( port_num, result, dt )
        yield s

        #--------------------------------------------------
        # salvando resultados na para summrizar
        summary[ result ] = summary.get( result , 0 ) + 1
    yield summary_str( summary )


# PARA O MODO MULTITHREAD ---------------------------------------------------------------------------
class thread_port( thrd.Thread ):
    
    portas = {}
    host_ip = "127.0.0.1" #localhost
    timeout = 1.

    def __init__( self, port_num ):    
        thrd.Thread.__init__( self )
        self.port_num = port_num
    
    def run( self ):

        host_ip = thread_port.host_ip
        timeout = thread_port.timeout

        result , dt = try_connect( self.port_num , host_ip , timeout )
        thread_port.portas[ self.port_num ] = ( result , dt ) 

def sync():
    
    while True:
        if thrd.active_count() == 1:
            break

def thread_scan(  host_name, start , end , timeout, must_serv = True ):
    

    s = scan_header( host_name, start , end , timeout)
    yield s
    
    host_ip = sck.gethostbyname( host_name )
    thread_port.host_ip = host_ip
    thread_port.timeout = timeout

    #--------------------------------------------------
    # caso aluem troque os valores
    if start > end: start , end = end , start
    summary = {}
    
    for port_num in range( start , end + 1 ):
        if must_serv and not( check_service( port_num ) ): continue
        thread_port( port_num ).start()
    sync()
        
    portas = thread_port.portas
    for port_num in range( start , end + 1 ):
        if port_num not in portas: continue

        result , dt = portas[ port_num ]
        s = string_connect_result( port_num, result, dt )
        yield s

        #--------------------------------------------------
        # salvando resultados na para summrizar
        summary[ result ] = summary.get( result , 0 ) + 1
    yield summary_str( summary )

if __name__ == "__main__":
    

    host = input()
    start = max( int( input() ), 1 )
    end = min( int( input() ) , 65535 )
    
    # modo de execução, 0 para iterativo e demais numeros para paralelo
    f = iteractive_scan
    if ( int( input() ) ):
        f = thread_scan
    t = 10.

    st = time.time()
    resp = f( host , start, end, t)
    try:
        for s in resp:
            print( s )
    except KeyboardInterrupt:
        print( "\n ABORTANDO!" )
        sys.exit()

    dt = time.time() - st
    print( "A busca durou {:.5f} segundos".format( dt ) )

