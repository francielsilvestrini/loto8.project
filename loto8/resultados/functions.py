import json
import logging
import locale
from zipfile import ZipFile
from datetime import datetime
from bs4 import BeautifulSoup
from .models import Resultado

def converter_para_json(file):
    if '.zip' in file.name:
        print(file)
        with ZipFile(file) as zip_file:
            with zip_file.open('d_lotfac.htm') as f:
                soup = BeautifulSoup(f, "html.parser")
    else:
        soup = BeautifulSoup(file, "html.parser")

    records = []
    headers = []
    for row in soup.findAll("tr"):
        cells = row.findAll("td", {'rowspan': True})
        if len(cells) == 0:
            for header in row.findAll("th"):
                titulo = header.find(text=True)
                headers += [titulo]
        else:
            valores = []
            for cell in cells:
                valores.append( cell.find(text=True) )

            if len(valores) < len(headers):
                valores.insert(19, '')
                valores.insert(19, '')

            data = {headers[i]: valor for i, valor in enumerate(valores)}

            records += [data]

    #with open('result.json', 'w') as fp:
    #	json.dump(records, fp)
    return json.dumps(records)


def to_datetime(s):
    dt = datetime.strptime(s, '%d/%m/%Y').date()
    return dt


def to_float(s):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    return locale.atof(s)


def carregar_concursos(json_data):
    concursos_json = json.loads(json_data)

    concursos = {}
    for concurso_json in concursos_json:
        bolas = []
        for numero_bola in range(1, 16):
            bolas.append(concurso_json.get('Bola%s' % str(numero_bola)))
        bolas_ordenadas = sorted(bolas)

        numero_concurso = int(concurso_json.get('Concurso'))

        concursos[numero_concurso] = dict(            
            concurso=numero_concurso,
            bola_01 = int(bolas_ordenadas[0]),
            bola_02 = int(bolas_ordenadas[1]),
            bola_03 = int(bolas_ordenadas[2]),
            bola_04 = int(bolas_ordenadas[3]),
            bola_05 = int(bolas_ordenadas[4]),
            bola_06 = int(bolas_ordenadas[5]),
            bola_07 = int(bolas_ordenadas[6]),
            bola_08 = int(bolas_ordenadas[7]),
            bola_09 = int(bolas_ordenadas[8]),
            bola_10 = int(bolas_ordenadas[9]),
            bola_11 = int(bolas_ordenadas[10]),
            bola_12 = int(bolas_ordenadas[11]),
            bola_13 = int(bolas_ordenadas[12]),
            bola_14 = int(bolas_ordenadas[13]),
            bola_15 = int(bolas_ordenadas[14]),
            data_sorteio = to_datetime(concurso_json.get('Data Sorteio')),

            arrecadacao_total = to_float(concurso_json.get('Arrecadacao_Total')),
            ganhadores_15_numeros = int(concurso_json.get('Ganhadores_15_Números')),
            ganhadores_14_numeros = int(concurso_json.get('Ganhadores_14_Números')),
            ganhadores_13_numeros = int(concurso_json.get('Ganhadores_13_Números')),
            ganhadores_12_numeros = int(concurso_json.get('Ganhadores_12_Números')),
            ganhadores_11_numeros = int(concurso_json.get('Ganhadores_11_Números')),
            valor_rateio_15_numeros = to_float(concurso_json.get('Valor_Rateio_15_Números')),
            valor_rateio_14_numeros = to_float(concurso_json.get('Valor_Rateio_14_Números')),
            valor_rateio_13_numeros = to_float(concurso_json.get('Valor_Rateio_13_Números')),
            valor_rateio_12_numeros = to_float(concurso_json.get('Valor_Rateio_12_Números')),
            valor_rateio_11_numeros = to_float(concurso_json.get('Valor_Rateio_11_Números')),
        )
    return concursos


def atualizar_novos_resultados(concursos):
    ultimo_concurso = Resultado.objects.ultimo_concurso()
    novos = 0
    for num_concurso in filter(lambda x: int(x) > ultimo_concurso, concursos):
        concurso = concursos[num_concurso]
    
        Resultado.objects.get_or_create(
            concurso=num_concurso, 
            defaults=concurso,
        )
        novos += 1
            
    return 0