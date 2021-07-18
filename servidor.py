"""
Disciplina de Redes de Computadores
Semestre: 2020/2
Trabalho = "Cliente -servidor dispensa-super"

Autor   = "Felipe Gante Maia de Sousa"
E-mail  = "fegante@hotmail.com"
"""

from cliente import lista_csv_dispensa
import socket
import json
import random
import csv



def lista_csv_supermercado():
    lista = []
    with open('supermercado.csv', newline='') as csvfile:
        spamreader = csv.reader (csvfile, delimiter=' ', quotechar = '|')
        for row in spamreader:
            row = row[0].split(',')  
            lista.append(row)   
    return lista    

def pedido(msg1):
    lista_super = lista_csv_supermercado()
    listas= []
    lista_mudanca = []
    for e in msg1:
        for f in lista_super:
            if f[0] == e[0]:
                if f[1] > e[1]:
                    produto = e[0]
                    quantidade = float(e[1])
                    preco = float(f[2])
                    total = quantidade * preco
                    item = [str(produto), str(quantidade),str(preco), str(total)]
                    nova_quantidade = str(int(float(f[1]) - quantidade))
                    mudanca = [f[0],nova_quantidade,f[2]]
                    lista_mudanca.append(mudanca)                   
                else:
                    item = [0] 
                listas.append(item)
                break
    return listas, lista_mudanca 

def atuliza(mudanca, lista):
    i = 0
    for e in mudanca:
        for f in lista:
            if f[0] == e[0]:
                f = e
                break        
            i = i + 1  

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
        lista = lista_csv_supermercado()
        print ('Concetado por', cliente)
    #------- inicio do protocolo --------------
        msg1 = con.recv(1024)
        msg1 = msg1.decode('UTF-8')
        msg1 = json.loads(msg1)

            

        dic,mudanca = pedido(msg1)
        msg_inicial = json.dumps(dic)
        msg_inicial = msg_inicial.encode('UTF-8')
        con.send (msg_inicial)
        

        while True:
           msg = con.recv(1024)		# Recebe mensagem
           msg = msg.decode('UTF-8')	# Decodifica a mensagem
           if not msg: break
           elif '1' == msg:
                atuliza(mudanca, lista)
                print('dados da compra')
                soma = 0.0 
                for e in dic:
                    soma = float(e[3]) + soma
                    print(e[0],', quantidade',e[1])
                print('soma total:', soma, 'reais')
                final = "compra foi realizada com sucesso e em breve os itens serao entregues"
                final = final.encode('UTF-8')
                con.send (final)

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