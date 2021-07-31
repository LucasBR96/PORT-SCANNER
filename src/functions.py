import time
import socket as sck
from errno import errorcode


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
    result = sock.connect_ex( tup )
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
    
    result_name = "SUCCESS" 
    if result:
        result_name = errorcode[ result ]

    s = "-"*50 + "\n"
    s += "{} {}\n".format( port_num , port_name )
    s += "{} {}\n".format( result , result_name )
    s += true_time

    return s


def iteractive_scan( host_name, start , end , timeout = 1. , alpha = .15 ):
    
    '''
    escaneameto de modo iterativo, em contraste com o modo multithread
    '''

    host_ip = sck.gethostbyname( host_name )
    s = "\nHost with name \"{}\" have IP of \"{}\"\n".format( host_name , host_ip )
    yield s
    
    #--------------------------------------------------
    # caso aluem troque os valores
    if start > end: start , end = end , start

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


if __name__ == "__main__":

    s = "www.amazon.com.br"
    start , end = 80 , 500
    t = 8.

    resp = iteractive_scan( s , start, end, timeout = t, alpha = .1 )
    for s in resp:
        print( s )


