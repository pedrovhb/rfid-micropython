# -*- coding: UTF-8 -*-

# Lê a lista de tags registrados e os bota em lista_rfid.
# A lista consistem em UIDs dos tags registrados separados por uma barra / 
# O primeiro elemento na lista é o tag mestre; se ele for lido, o próximo tag lido será adicionado à lista
def ler_lista_rfid():
	arquivo_rfid = open('lista_rfid.txt', 'r')
	lista_rfid = arquivo_rfid.read().split('/')
	rfid_mestre = lista_rfid[0]
	arquivo_rfid.close()
	return lista_rfid



# Verifica se foi detectado um cartão ou tag no último ciclo; se sim, retornamos seu identificador único. Se não, retornamos None.
def ler_tag(rdr):

	tag_lido = None

	(rfid_stat, tag_type) = rdr.request(rdr.REQIDL)

	if rfid_stat == rdr.OK:

		(rfid_stat, raw_uid) = rdr.anticoll()

		if rfid_stat == rdr.OK:
			
			# Pegar identificador único como string e enviá-lo via MQTT
			tag_lido = "%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])

	return tag_lido
			
# Cadastra próxima tag inserida e retorna versão atualizada de lista de tags registradas
def cadastrar_tag(rdr):

	lista_rfid = ler_lista_rfid()

	while True:

		tag_lido = ler_tag(rdr)

		if tag_lido is not None:
			tag_cadastrado = None
			# Se o tag lido não for nulo e não estiver na lista de rfid...
			if tag_lido not in lista_rfid:
				# Abrir lista em modo append (adicionar)
				arquivo_rfid = open('lista_rfid.txt', 'a')
				# Adicionar barra e identificador único
				arquivo_rfid.write('/{}'.format(tag_lido))
				arquivo_rfid.close()
				tag_cadastrado = tag_lido
			# Retorna lista atualizada e tag cadastrado, ou None se o cadastro for cancelado
			return ler_lista_rfid(), tag_cadastrado