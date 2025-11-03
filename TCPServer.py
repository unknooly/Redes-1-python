from socket import socket,AF_INET,SOCK_STREAM
from config import caminho

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("",serverPort))
serverSocket.listen(1)
print("Servidor funcionando\n")

# número do ACK (server-side)
n=0

while True:
	connectionSocket,addr = serverSocket.accept()
	print(f"Conectado com {addr}")

	try:
		header=connectionSocket.recv(1024).decode("utf-8")
		arquivo=header.split(":",1)[1].strip()
		print(f"Arquivo <{arquivo}> está vindo")
		connectionSocket.send(b"ACK inicial")

		with open(f"{caminho}/{arquivo}","wb") as f:
			while True:
				pacote=connectionSocket.recv(1024)
				if not pacote:
					break
				f.write(pacote)
				connectionSocket.send(f"ACK nº {n}".encode())
				n+=1

		print(f"Arquivo <{arquivo}> recebido com sucesso")
		connectionSocket.send(b"Arquivo recebido")

	except Exception as erro:
		print(f"Erro ao receber arquivo: {erro}")

	finally:
		connectionSocket.close()
		print("Conexão encerrada\n")