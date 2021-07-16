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
    # Cria o socket do servidor
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    orig = (HOST, PORT) # Forma a tupla de host, porta

    tcp.bind(orig)		# Solicita ao S.O. acesso exclusivo a porta 5000
    tcp.listen(10)		# Entra no modo de escuta

    while True:
        con, cliente = tcp.accept() # Aceita conexao do cliente
        print ('Concetado por', cliente)

    #------- inicio do protocolo --------------
        msg = con.recv(1024)
        msg = msg.decode('UTF-8')
        print (cliente, msg)

        msg_inicial = "Bom dia!"
        msg_inicial = msg_inicial.encode('UTF-8')
        con.send (msg_inicial)


        while True:
            msg = con.recv(1024)		# Recebe mensagem
            msg = msg.decode('UTF-8')	# Decodifica a mensagem
            if not msg: break
            print (cliente, msg)

    #---------------- fim do protocolo --------------

        print ('Finalizando conexao do cliente', cliente)
        con.close()		# fecha a conexao com o cliente

        return 0

#------- Início do programa ---------
if __name__ == '__main__':
    from sys import argv
    if (len(argv) > 2):
        ip = argv[1]
        porta = int(argv[2])
        exit(main(ip, porta))
    else:
        print("exemplo de inicialização: python3 servidor.py 127.0.0.1 5000")