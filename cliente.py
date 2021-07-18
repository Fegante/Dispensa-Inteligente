"""
Disciplina de Redes de Computadores
Semestre: 2020/2
Trabalho = "Cliente -servidor dispensa-super"

Autor   = "Felipe Gante Maia de Sousa"
E-mail  = "fegante@hotmail.com"
"""
import socket
import json
import random
import csv

def lista_csv_dispensa():
    lista = []
    with open('dispensa.csv', newline='') as csvfile:
        spamreader = csv.reader (csvfile, delimiter=' ', quotechar = '|')
        for row in spamreader:
            row = row[0].split(',')  
            lista.append(row)   
    return lista    

def gerando_lista():  
    lista = lista_csv_dispensa() 
    tamanho = len(lista)
    tamanho = list(range(tamanho))
    rand = random.sample(tamanho, k=5)
    dic = []
    for e in rand:
        dic.append(lista[e])
    return dic


 
def main(ip: str, porta: int):
    HOST = ip     # Endereco IP do Servidor (loopback 127.0.0.1)
    PORT = porta  # Porta que o Servidor esta usando (identifica qual a aplicacao)
    # Cria o socket do cliente
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (HOST, PORT) # Forma a tupla de host, porta

    tcp.connect(dest)	# Estabelece a conexao
    #---------------- inicio protocolo --------------
    dic = gerando_lista()           
    msg_inicial = json.dumps(dic)     
    msg_inicial = msg_inicial.encode('UTF-8')
    tcp.send (msg_inicial)

    msg = tcp.recv(1024)
    msg = msg.decode('UTF-8')
    msg = json.loads(msg)
    soma = 0.0 
    for e in msg:
        soma = float(e[3]) + soma
        print(e[0],', quantidade',e[1])
    print('soma total:', soma, 'reais')

    if [0] in msg:
        print("compra cancelada,devido não ter a quantidade de um dos produtos requerido")
        tcp.close()	# fecha a conexao com o servidor
        return 0

    print ('Aperte 1 para COnfimar a compra ou qualquer uma outra coisa para cancelar  ')
    msg = input()
    msg = msg.encode('UTF-8') 	# Codifica a mensagem para UTF-8
    tcp.send (msg)
    while msg != b'1':
        print("compra cancelada")
        tcp.close()	# fecha a conexao com o servidor
        return 0

    while True:
        msg = tcp.recv(1024)
        msg = msg.decode('UTF-8') # Decodifica a mensagem
        print(msg)	
        break
        
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