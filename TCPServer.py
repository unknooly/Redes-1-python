from socket import socket,AF_INET,SOCK_STREAM
from os import system

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("",serverPort))
serverSocket.listen(1)
print("Servidor funcionando\n")

while True:
	connectionSocket,addr = serverSocket.accept()
	print(f"🔗 Conectado com {addr}")

	buffer={}

	try:
		try:
			header=connectionSocket.recv(1024).decode("utf-8")
			arquivo=header.split(":",1)[1].strip()
			print(f"Arquivo <{arquivo}> está vindo")
		except Exception as erroHeader:
			print(f"Erro ao receber header: {erroHeader}")

		try:
			connectionSocket.send(b"ACK inicial")
		except Exception as erroInicial:
			print(f"Erro ao enviar ACK inicial: {erroInicial}")

		while True:
			try:
				header=connectionSocket.recv(4)
				if not header:
					break
				pacote_id=int.from_bytes(header,"big")
			except Exception as erroHeader:
				print(f"Erro ao receber pacote: {erroHeader}")

			try:
				payload=connectionSocket.recv(1024)
				if not payload:
					break
			except Exception as erroPayload:
				print(f"Erro ao receber payload: {erroPayload}")

			buffer[pacote_id]=payload

			ack_msg=f"ACK nº {pacote_id}"
			try:
				connectionSocket.send(ack_msg.encode())
				print(f"✅ {ack_msg}")
			except Exception as erroACK:
				print(f"Erro ao enviar ACK")

		print(f"🏁 Arquivo <{arquivo}> recebido com sucesso")
		connectionSocket.send(b"Arquivo recebido")

	except Exception as erro:
		print(f"❌ Erro ao receber arquivo: {erro}")

	finally:
		connectionSocket.close()
		system(f"mkdir -p ./files")
		with open(f"./files/{arquivo}","wb") as f:
			for pac_id in sorted(buffer.keys()):
				f.write(buffer[pac_id])
		print("Conexão encerrada\n")