import time
import socket as sck

def try_connect( port_num , host_ip , timeout = 1. ):

    
    sock = sck.socket( sck.AF_INET , sck.SOCK_STREAM )
    sock.set_timeout( timeout )
    tup = ( host_ip , port_num )

    t = time.time()
    result = sock.connect_ex( tup )
    dt = time.time() - t

    sock.shutdown( sck.SHUT_RDWR )
    sock.close()

    return result , dt

