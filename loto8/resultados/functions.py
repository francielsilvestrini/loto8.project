from bs4 import BeautifulSoup
import json
import logging


def converter_para_json(file):
    soup = BeautifulSoup(file, "html.parser")

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

    # with open('result.json', 'w') as fp:
    #	json.dump(records, fp)
    return json.dumps(records)


def carregar_concursos(json_data):
    # with open('result.json') as f:
    #	data_json = json.load(f)

    concursos = {}
    for concurso_json in json_data:
        numero_concurso = concurso_json.get('concurso')
        bolas = []
        for numero_bola in range(1, 16):
            bolas.append(concurso_json.get('bola%s' % numero_bola))
        data_sorteio = concurso_json.get('data sorteio')
        arrecadacao_total = concurso_json.get('arrecadacao_total')
        ganhadores = concurso_json.get('ganhadores_15_números')

        bolas_ordenadas = sorted(bolas)

        concursos[numero_concurso] = dict(
            numero_concurso=numero_concurso,
            bolas=bolas,
            bolas_ordenadas=bolas_ordenadas,
            data_sorteio=data_sorteio,
            arrecadacao_total=arrecadacao_total,
            ganhadores=ganhadores,
        )
    return concursos
