"""
Disciplina de Redes de Computadores
Semestre: 2020/2
Trabalho = "Título do trabalho"

Autor   = "Seu nome"
E-mail  = "seu e-mail"
"""
import socket

def main(ip: str, porta: int):
    HOST = ip     # Endereco IP do Servidor (loopback 127.0.0.1)
    PORT = porta  # Porta que o Servidor esta usando (identifica qual a aplicacao)
    # Cria o socket do cliente
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (HOST, PORT) # Forma a tupla de host, porta

    tcp.connect(dest)	# Estabelece a conexao

    #---------------- inicio protocolo --------------
    msg_inicial = "Bom dia!"
    msg_inicial = msg_inicial.encode('UTF-8')
    tcp.send (msg_inicial)

    msg = tcp.recv(1024)
    msg = msg.decode('UTF-8')
    print (dest, msg)

    print ('Para sair use CTRL+X\n')
    msg = input()
    while msg != '\x18':
        msg = msg.encode('UTF-8') 	# Codifica a mensagem para UTF-8
        tcp.send (msg) 				# Envio a mensagem para o servidor
        msg = input()
    #---------------- fim do protocolo --------------

    tcp.close()	# fecha a conexao com o servidor
    return 0

#------- Início do programa ---------
if __name__ == '__main__':
    from sys import argv
    if (len(argv) > 2):
        ip = argv[1]
        porta = int(argv[2])
        exit(main(ip, porta))
    else:
        print("exemplo de inicialização: python3 cliente.py 127.0.0.1 5000")