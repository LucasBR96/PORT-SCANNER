import socket as sck

start = 80
stop = 200
host_ip = sck.gethostbyname( "www.amazon.com" )
print( host_ip )

for i in range( start , stop + 1 ):
    
    #--------------------------------------------------
    # SOCK_STREAM indica conexão tcp
    sock = sck.socket( sck.AF_INET , sck.SOCK_STREAM )
    sock.settimeout( 1. )
    tup = ( host_ip , i )

    #--------------------------------------------------
    # connect_ex e uma função que faz o socket conectar
    # com um endereço de IP e um port_number, e retorna
    # um numero de erro da conexão
    print( i , sock.connect_ex( tup ) )

    #--------------------------------------------------
    # Fecha a conexão e mata o socket. Por assim dizer
    sock.shutdown( sck.SHUT_RDWR )
    sock.close()


