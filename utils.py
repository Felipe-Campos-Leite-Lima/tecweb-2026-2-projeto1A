import json
from pathlib import Path

CUR_DIR = Path(__file__).parent


def extract_route(requisicao):
    return requisicao.split()[1].removeprefix('/')


def read_file(filepath):
    with open(filepath, 'rb') as arquivo:
        return arquivo.read()


def load_data(nome_arquivo):
    filepath = CUR_DIR / 'data' / nome_arquivo
    with open(filepath, 'r', encoding='utf-8') as arquivo:
        return json.load(arquivo)


def load_template(nome_arquivo):
    filepath = CUR_DIR / 'templates' / nome_arquivo
    with open(filepath, 'r', encoding='utf-8') as arquivo:
        return arquivo.read()


def add_note(nota):
    notas = load_data('notes.json')
    notas.append(nota)
    filepath = CUR_DIR / 'data' / 'notes.json'
    with open(filepath, 'w', encoding='utf-8') as arquivo:
        json.dump(notas, arquivo, ensure_ascii=False, indent=2)

def build_response(body='', code=200, reason='OK', headers=''):
    response = f'HTTP/1.1 {code} {reason}\n'
    if headers:
        response += f'{headers}\n'
    response += '\n'
    return response.encode() + body.encode()