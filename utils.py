import json
from pathlib import Path

CUR_DIR = Path(__file__).parent


def extract_route(requisicao):
    return requisicao.split()[1].removeprefix('/')


def read_file(filepath):
    with open(filepath, 'rb') as arquivo:
        return arquivo.read()


def load_template(nome_arquivo):
    filepath = CUR_DIR / 'templates' / nome_arquivo
    with open(filepath, 'r', encoding='utf-8') as arquivo:
        return arquivo.read()

def build_response(body='', code=200, reason='OK', headers=''):
    response = f'HTTP/1.1 {code} {reason}\n'
    if headers:
        response += f'{headers}\n'
    response += '\n'
    return response.encode() + body.encode()