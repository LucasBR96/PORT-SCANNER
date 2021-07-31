import time
import socket as sck
from errno import errorcode


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

def string_connect_result( port_num , result, dt ):
    
    port_name = sck.getservbyport( port_num ).upper()
    true_time = "{:.5f} seconds".format( dt )
    
    result_name = "SUCCESS" 
    if result
        result_name = errorcode[ result ]

    s = "-"*50 + "\n"
    s += "{} {}\n".format( port_num , port_name )
    s += "{} {}\n".format( result , result_name )
    s += true_time

    return s



