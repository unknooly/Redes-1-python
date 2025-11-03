from socket import socket,AF_INET,SOCK_STREAM,SHUT_WR
from os import scandir,system
import config
# system("clear")

class arquivo:
    def __init__(self,name,path):
        self.name=name
        self.path=path
# class pacote:
#     def __init__(self,maxSize,content,id,isACKED):
#         self.size=maxSize
#         self.content=content
#         self.id=id
#         self.isACKED=isACKED

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
    clientSocket.connect((serverName,serverPort))

    clientSocket.sendall(f"Cliente enviando arquivo: {arquivos[op].name}".encode("utf-8"))
    ack = clientSocket.recv(1024)
    
    with open(arquivos[op].path,"rb") as f:
        while True:
            pacote=f.read(tamanhoPacote)
            if not pacote:
                break
            clientSocket.sendall(pacote)
            ack = clientSocket.recv(1024)
            print(ack.decode())

    clientSocket.shutdown(SHUT_WR)
    ackFinal = clientSocket.recv(1024)
    print(f"Resposta final: {ackFinal.decode()}")