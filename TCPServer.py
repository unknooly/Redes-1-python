from socket import socket,AF_INET,SOCK_STREAM
from config import caminho

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("",serverPort))
serverSocket.listen(1)
print("Servidor funcionando\n")

while True:
	connectionSocket,addr = serverSocket.accept()
	print(f"🔗 Conectado com {addr}")

	try:
		header=connectionSocket.recv(1024).decode("utf-8")
		arquivo=header.split(":",1)[1].strip()
		print(f"Arquivo <{arquivo}> está vindo")
		connectionSocket.send(b"ACK inicial")

		buffer={}
		next_id=0
		with open(f"{caminho}/{arquivo}","wb") as f:
			while True:
				header=connectionSocket.recv(4)
				if not header:
					break
				pacote_id=int.from_bytes(header,"big")

				payload=connectionSocket.recv(1024)
				if not payload:
					break

				buffer[pacote_id]=payload

				while next_id in buffer:
					f.write(buffer.pop(next_id))
					ack_msg=f"ACK nº {next_id}"
					connectionSocket.send(ack_msg.encode())
					print(f"✅ {ack_msg}")
					next_id+=1

		print(f"🏁 Arquivo <{arquivo}> recebido com sucesso")
		connectionSocket.send(b"Arquivo recebido")

	except Exception as erro:
		print(f"❌ Erro ao receber arquivo: {erro}")

	finally:
		connectionSocket.close()
		print("Conexão encerrada\n")