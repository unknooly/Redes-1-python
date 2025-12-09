from socket import socket,AF_INET,SOCK_STREAM,SHUT_WR
from os import scandir,system
import config
import random

if not config.debug:
    system("clear")

arquivos=[]
pacotes=[]

class arquivo:
    def __init__(self,name,path):
        self.name=name
        self.path=path
class pacote:
    def __init__(self,maxSize,content,id):
        self.size=maxSize
        self.content=content
        self.id=id
        self.isACKed=False

# selecionar arquivo
def scan(path):
    with scandir(path) as lista:
        for item in lista:
            if item.is_file() and not item.name.startswith("."):
                arquivos.append(arquivo(item.name,item.path))
            elif item.is_dir() and not item.name.startswith("."):
                scan(item.path)
scan("./")

# input
if config.debug:
    op=config.op
    tamanhoPacote=config.tamanhoPacote
else:
    for i,item in enumerate(arquivos,start=0):
        print(f"{i} - {item.name}")
    print("\n")

    op=-1
    while(op<0 or op>=len(arquivos)):
        op=int(input("\tSelecione um arquivo para enviar: "))
    print()

    tamanhoPacote=0
    while(tamanhoPacote<1 or tamanhoPacote>1024):
        tamanhoPacote=int(input("\tTamanho do pacote: "))
    print("\n")

# envia arquivo selecionado
serverName=config.ip
serverPort=12000

with socket(AF_INET,SOCK_STREAM) as clientSocket:
    clientSocket.settimeout(0.1)

    try:
        clientSocket.connect((serverName,serverPort))
    except Exception as erroConectar:
        print(f"Erro em conectar: {erroConectar}")

    try:
        clientSocket.sendall(f"Cliente enviando arquivo: {arquivos[op].name}".encode("utf-8"))
        ack = clientSocket.recv(1024).decode()
        print(f"Servidor respondeu: {ack}")
    except Exception as erroEnvioHeader:
        print(f"Erro ao enviar cabeçalho: {erroEnvioHeader}")

    contador=0

    try:
        with open(arquivos[op].path,"rb") as f:
            while True:
                payload=f.read(tamanhoPacote)
                if not payload:
                    break

                pacotes.append(pacote(tamanhoPacote,payload,contador))

                if random.randint(1,100) > config.chance:
                    header=contador.to_bytes(4,"big")
                    try:
                        clientSocket.sendall(header+payload)
                        try:
                            ack = clientSocket.recv(1024).decode()
                            if ack==f"ACK nº {contador}":
                                pacotes[contador].isACKed=True
                                print(f"✅ ACK {contador}: {ack}")
                        except Exception as erroReceberAck:
                            print(f"Erro ao receber ACK {contador}: {erroReceberAck}")
                    except Exception as erroEnviarPacote:
                        print(f"Erro ao enviar pacote {contador}: {erroEnviarPacote}")
                else:
                    print(f"❌ Falha em enviar pacote {contador}")
                contador+=1
    except Exception as erroAbrir:
        print(f"Erro ao ler arquivo: {erroAbrir}")
 
    clientSocket.shutdown(SHUT_WR)
    ackFinal = clientSocket.recv(1024)
    print(f"Resposta final: {ackFinal.decode()}")

# pacotes que não foram enviados
# tentativas=0

# while any(not pac.isACKed for pac in pacotes) and tentativas<1:
#     print(f"\n🔁 Reenvio nº {tentativas}")
#     for pac in pacotes:
#         if not pac.isACKed:
#             if random.randint(1,100) > config.chance:
#                 header=pac.id.to_bytes(4,"big")
#                 try:
#                     clientSocket.sendall(header+pac.content)
#                     try:
#                         ack = clientSocket.recv(1024).decode()
#                         if ack==f"ACK nº {pac.id}":
#                             pac.isACKed=True
#                             print(f"✅ ACK {pac.id}: {ack}")
#                     except Exception as erroReceberAck:
#                         print(f"Erro ao receber ACK {pac.id}: {erroReceberAck}")
#                 except Exception as erroEnviarPacote:
#                     print(f"Erro ao enviar pacote {pac.id}: {erroEnviarPacote}")
#             else:
#                 print(f"❌ Falha em enviar pacote {pac.id}")
#     tentativas+=1