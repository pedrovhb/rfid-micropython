# -*- coding: UTF-8 -*-

# O sta_if é a interface para estação, roteador em que o ESP se conecta
sta_if = network.WLAN(network.STA_IF)

# O ap_if é a interface de ponto de acesso, que outros dispositivos usam para se conectar ao ESP
ap_if = network.WLAN(network.AP_IF)
ap_if.config(essid=b'RFID MicroPython', authmode=network.AUTH_WPA_WPA2_PSK, password=b'sua-senha')

# Conectar-se a nossa rede
sta_ssid = 'Nome-da-Sua-Rede'
sta_pwd = 'Senha-da-Sua-Rede'
sta_if.active(True)
sta_if.connect(sta_ssid, sta_pwd)

# Esperar conexão
while not sta_if.isconnected():
	pass

# Ler a lista RFID. O código mestre é o primeiro da lista.
lista_rfid = rfid_nersd.ler_lista_rfid()
rfid_mestre = lista_rfid[0]

# Criar objeto leitor de RFID
rdr = mfrc522.MFRC522(0, 2, 4, 5, 14)

# Criar o cliente MQTT. Os parâmetros são o nome do cliente e o endereço do broker, respectivamente.
c =  umqtt_simple.MQTTClient('cliente_rfid_nersd', 'iot.eclipse.org')
c.connect()

while True:

	uid = rfid_nersd.ler_tag(rdr)

	if uid is None:
		pass

	elif uid == rfid_mestre:
		print('Aproxime o tag a ser cadastrado.\n')
		lista_rfid, tag_cadastrado = rfid_nersd.cadastrar_tag(rdr)
		if tag_cadastrado is None:
			print('Cadastro cancelado.\n')
			c.publish('/nersd/rfid', 'cadastro-cancelado')
		else:
			print('Cadastro realizado com sucesso. UID: {}\n'.format(tag_cadastrado))
			c.publish('/nersd/rfid', '{}-cadastro'.format(tag_cadastrado))

	else:
		if uid in lista_rfid:
			# <ABRIR PORTA>
			print('Entrada permitida. UID: {}\n'.format(uid))
			c.publish('/nersd/rfid', '{}-permitido'.format(uid))
		else:
			# Acesso negado
			print('Acesso negado. UID: {}\n'.format(uid))
			c.publish('/nersd/rfid', '{}-negado'.format(uid))
	
			


