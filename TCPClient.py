from socket import socket,AF_INET,SOCK_STREAM,SHUT_WR
from os import scandir,system
import config
import random
# system("clear")

class arquivo:
    def __init__(self,name,path):
        self.name=name
        self.path=path
class pacote:
    def __init__(self,maxSize,content,id,isACKED):
        self.size=maxSize
        self.content=content
        self.id=id
        self.isACKED=isACKED

# selecionar arquivo
arquivos=[]

def scan(path):
    with scandir(path) as lista:
        for item in lista:
            if item.is_file():
                arquivos.append(arquivo(item.name,item.path))
            elif item.is_dir() and not item.name.startswith("."):
                scan(item.path)
scan("./")

if config.debug:
    op=0
    tamanhoPacote=5
else:
    op=-1
    for i,item in enumerate(arquivos,start=0):
        print(f"{i} - {item.name}")
    while(op<0 or op>=len(arquivos)):
        op=int(input("\n\tSelecione um arquivo para enviar: "))

    tamanhoPacote=int(input("\tTamanho do pacote: "))

# envia arquivo selecionado
serverName=config.ip
serverPort=12000

with socket(AF_INET,SOCK_STREAM) as clientSocket:
    pacotes=[]
    n=0
    clientSocket.connect((serverName,serverPort))

    clientSocket.sendall(f"Cliente enviando arquivo: {arquivos[op].name}".encode("utf-8"))
    ack = clientSocket.recv(1024)
    
    with open(arquivos[op].path,"rb") as f:
        while True:
            pkg=f.read(tamanhoPacote)
            chance=random.randint(1,100)
            pacotes.append(pacote(tamanhoPacote,pkg,n,False))
            if not pkg:
                break
            clientSocket.sendall(pkg)
            if chance!=100:
                try:
                    ack = clientSocket.recv(1024)
                    if ack:
                        pacotes[n].isACKED=True
                        print(f"ACK recebido do pacote {n}: {ack.decode()}")
                except Exception as erro:
                    print(f"Erro ao receber ACK do pacote {n}: {erro}")
            n+=1

    clientSocket.shutdown(SHUT_WR)
    ackFinal = clientSocket.recv(1024)
    print(f"Resposta final: {ackFinal.decode()}")

# pacotes que não foram enviados
for item in pacotes:
    if item.isACKED==False:
        print(f"Pacote {item.id}")