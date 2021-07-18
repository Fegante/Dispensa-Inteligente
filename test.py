import socket
import json
import random
import csv

class Produto:
    def __init__(self, nome, quantidade, preco):
        self.nome = nome
        self.quantidade = quantidade
        self.preco = preco
    
    def setNome(self, nome):
        self.nome = nome

    def setQuantidade(self, quantidade):
        self.quantidade = quantidade

    def setPreco(self, preco):
        self.preco = preco
    
    def getPreco(self):
        return self.preco
        
    def getQuantidade(self):
        return self.quantidade

    def atualizaEstoque(self, numero):
        antigo = self.getQuantidade()
        self.quantidade = antigo - numero

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
    cabeca = ['item', 'quantidade', 'valor unitário', 'valor total']
    for e in msg1:
        for f in lista_super:
            if f[0] == e[0]:
                if f[1] > e[1]:
                    produto = e[0]
                    quantidade = float(e[1])
                    preco = float(f[2])
                    total = quantidade * preco
                    item = [str(produto), str(quantidade),str(preco), str(total)]
                    f[1] = str(int(float(f[1]) - quantidade))                   
                else:
                    item = [0] 
                listas.append(item)
                break
    return listas 

a = gerando_lista()
b = lista_csv_supermercado()
c = pedido(a)
print(c)
