import uuid
import json

ESTATISTICA_PARA = 500 #estatistica para 10 concursos
NUMERO_BLOCOS = 5
NUMERO_JOGOS = 14
#NUMEROS_DA_SORTE = ['05', '16', '09']
NUMEROS_DA_SORTE = []
ACERTOS = 14
distribuicao = {0:5, 1:4, 2:3, 3:2, 4:1} #para cartão de 15 escolhas
#distribuicao = {0:5, 1:5, 2:4, 3:1, 4:0} #para cartão de 15 escolhas
JOGO = '1957'

def teste01():
	import xmltodict
	import json
	with open('d_lotfac.htm') as xml_file:
		my_dict=xmltodict.parse(xml_file.read())
	xml_file.close()


	#json_data=json.dumps(my_dict)
	#print(json_data)

	with open('result.json', 'w') as fp:
		json.dump(my_dict, fp)


def teste02():
	from bs4 import BeautifulSoup

	soup = BeautifulSoup(open("d_lotfac.htm"), "html.parser")

	records = []
	headers = []
	for row in soup.findAll("tr"):
		cells = row.findAll("td")
		if len(cells) == 0:
			for header in row.findAll("th"):
				headers += [header.find(text=True)]
		else:
			data = {}
			for k, cell in enumerate(cells):
				data[headers[k]] = cell.find(text=True)
			records += [data]

	with open('result.json', 'w') as fp:
		json.dump(records, fp)


def converter_para_json():
	from bs4 import BeautifulSoup
	import json

	soup = BeautifulSoup(open("d_lotfac.htm"), "html.parser")

	records = []
	headers = []
	for row in soup.findAll("tr"):
		cells = row.findAll("td", {'rowspan': True})
		if len(cells) == 0:
			for header in row.findAll("th"):
				headers += [header.find(text=True)]
		else:
			data = {}
			for k, cell in enumerate(cells):
				data[headers[k]] = cell.find(text=True)
			records += [data]

	with open('result.json', 'w') as fp:
		json.dump(records, fp)


def teste04():
	import json
	
	with open('result.json') as f:
		data = json.load(f)

	for concurso in data:
		print(concurso.get('Concurso'),  
			concurso.get('Bola1'), 
			concurso.get('Bola2'),
			concurso.get('Bola3'),
			concurso.get('Bola4'),
			concurso.get('Bola5'),
			concurso.get('Bola6'), 
			concurso.get('Bola7'),
			concurso.get('Bola8'),
			concurso.get('Bola9'),
			concurso.get('Bola10'),
			concurso.get('Bola11'),
			concurso.get('Bola12'),
			concurso.get('Bola13'),
			concurso.get('Bola14'),
			concurso.get('Bola15'),
			concurso.get('Data Sorteio'),
			concurso.get('Arrecadacao_Total'),
			concurso.get('Ganhadores_15_Números'),
			concurso.get('Ganhadores_14_Números'),
			concurso.get('Ganhadores_13_Números'),
			concurso.get('Ganhadores_12_Números'),
			concurso.get('Ganhadores_11_Números'),
			concurso.get('Valor_Rateio_15_Números'),
			concurso.get('Valor_Rateio_14_Números'),
			concurso.get('Valor_Rateio_13_Números'),
			concurso.get('Valor_Rateio_12_Números'),
			concurso.get('Valor_Rateio_11_Números'),

		)  


def teste05():
	import json
	
	with open('result.json') as f:
		data_json = json.load(f)

	concursos = {}
	for concurso_json in data_json:
		numero_concurso = concurso_json.get('Concurso')
		bolas = [] 
		for numero_bola in range(1, 16):
			bolas.append( concurso_json.get('Bola%s' % numero_bola) )
		data_sorteio = concurso_json.get('Data Sorteio')
		arrecadacao_total = concurso_json.get('Arrecadacao_Total')
		ganhadores = concurso_json.get('Ganhadores_15_Números')

		bolas_ordenadas = sorted( bolas )
	
		concursos[numero_concurso] = dict(
			numero_concurso=numero_concurso,
			bolas=bolas,
			bolas_ordenadas=bolas_ordenadas,
			data_sorteio=data_sorteio,
			arrecadacao_total=arrecadacao_total,
			ganhadores=ganhadores,
			)

	print(len(concursos))
	print(concursos['1950'])


def carregar_concursos():
	import json
	
	with open('result.json') as f:
		data_json = json.load(f)

	concursos = {}
	for concurso_json in data_json:
		try:
			numero_concurso = concurso_json.get('Concurso')
			bolas = [] 
			for numero_bola in range(1, 16):
				bolas.append( concurso_json.get('Bola%s' % numero_bola) )
			data_sorteio = concurso_json.get('Data Sorteio')
			arrecadacao_total = concurso_json.get('Arrecadacao_Total')
			ganhadores = concurso_json.get('Ganhadores_15_Números')

			bolas_ordenadas = sorted( bolas )
		
			concursos[numero_concurso] = dict(
				numero_concurso=numero_concurso,
				bolas=bolas,
				bolas_ordenadas=bolas_ordenadas,
				data_sorteio=data_sorteio,
				arrecadacao_total=arrecadacao_total,
				ganhadores=ganhadores,
				)
		except:
			print(concurso_json)

	return concursos

def montar_estatistica():
	concursos = carregar_concursos()

	lista_concursos = []
	for numero_concurso in concursos.keys():
		lista_concursos.append(numero_concurso)
	lista_concursos.sort(reverse=True)
	#print(lista_concursos)

	if ESTATISTICA_PARA == 0:
		lista_concursos_analise = lista_concursos
	else:
		lista_concursos_analise = lista_concursos[:ESTATISTICA_PARA] 
	#print(lista_concursos_analise)

	concurso_peso = {}
	peso = 1.0
	concursos_por_bloco = len(lista_concursos_analise) // NUMERO_BLOCOS
	fator = peso / NUMERO_BLOCOS
	bloco = 1
	for i, numero in enumerate(lista_concursos_analise):
		if i > 0 and i % concursos_por_bloco == 0:
			bloco += 1
			peso = round(peso - fator, 2)
			if peso <= 0.0:
				peso = fator

		concurso_peso[numero] = (peso, bloco)
		#print(i, numero, peso, bloco)

	cartao = {}
	for bola in range(1,26):
		cartao[format(bola, '02d')] = dict(
			numero=format(bola, '02d'),
			pontuacao=0.0, 
			recorrencia=0, 
			concursos=[], 
			concursos_analisados=len(lista_concursos_analise),
			percentual_recorrencia=0.0
		)

	for numero_concurso in lista_concursos_analise:
		concurso = concursos[numero_concurso]

		for bola in concurso['bolas_ordenadas']:
			cartao_numero = cartao[bola]

			cartao_numero['pontuacao'] = round(cartao_numero['pontuacao'] + concurso_peso[numero_concurso][0], 2)
			cartao_numero['recorrencia'] += 1
			cartao_numero['concursos'].append(numero_concurso)
			cartao_numero['percentual_recorrencia'] = round(cartao_numero['recorrencia'] / cartao_numero['concursos_analisados'], 4) 
	
	#for key, item in cartao.items():
	#	print(key, 'recorrencia:', item['recorrencia'], 'pontuacao:', item['pontuacao'])
	return cartao

from random import sample

def montar_jogos():
	estatistica = montar_estatistica()

	indice = []
	for item in estatistica.values():
		key_index = '{:08.2f}'.format(item['pontuacao']) + '{:04d}'.format(item['recorrencia']) + item['numero'] 
		indice.append((key_index, item['numero']))
	indice_ordenado = sorted(indice, reverse=True)

	potes = []
	potes.append( [n for k, n in indice_ordenado[0:5]] )
	potes.append( [n for k, n in indice_ordenado[5:10]] )
	potes.append( [n for k, n in indice_ordenado[10:15]] )
	potes.append( [n for k, n in indice_ordenado[15:20]] )
	potes.append( [n for k, n in indice_ordenado[20:25]] )

	jogos = []

	while len(jogos) < NUMERO_JOGOS:
		jogo = []
		for i, dist in distribuicao.items():
			if dist == 0:
				continue
			pote = potes[i]

			for numero in sample(pote, k=dist):
				jogo.append(numero)
		
		numero_sorte = [n for n in filter(lambda x: x not in jogo, NUMEROS_DA_SORTE)]
		if len(numero_sorte) > 0:
			del jogo[- len(numero_sorte):]
			jogo += numero_sorte

		novo_jogo = sorted(jogo)
		if novo_jogo not in jogos:
			jogos.append(novo_jogo)

	#for jogo in jogos:
	#	print(jogo)
	return jogos

def teste08():
	cartoes = montar_jogos()
	concursos = carregar_concursos()

	for i, jogo in enumerate(cartoes):
		print()
		print('{:04d}'.format(i), jogo)
		for k, item in concursos.items():
			acertos = [n for n in filter(lambda x: x in item['bolas'], jogo)]
			if len(acertos) >= ACERTOS:
				print('{:04d}'.format(int(k)), item['bolas'])
				print('{:04d}'.format(len(acertos)), acertos)
				print()

def gerar_cartoes():
	cartoes = montar_jogos()

	with open('cartao-%s.json' % {str(uuid.uuid4())} , 'w') as fp:
		json.dump(cartoes, fp, indent=4)

	for cartao in cartoes:
		print(cartao)

def teste09():
	with open("cartao-{'4a0c8552-00a5-407a-8d6f-aaafd80f2ce4'}.json") as f:
		data_json = json.load(f)

	RESULTADO = [
		'01','02','04','05','09',
		'12','14','15','16','19',
		'20','22','23','24','25']
	for cartao  in data_json:
		acertos = [n for n in filter(lambda x: x in RESULTADO, cartao)]
		if len(acertos) >= 10:
			print(cartao, len(acertos), acertos)
		else:
			print(cartao)

if __name__ == '__main__':
	#converter_para_json()
	gerar_cartoes()
	#teste04()