from urllib.parse import unquote_plus

from utils import load_template, build_response
from database import Database, Note

db = Database('banco')


def extrair_params(request):
    request = request.replace('\r', '')
    corpo = request.split('\n\n')[1]
    params = {}
    for chave_valor in corpo.split('&'):
        chave, valor = chave_valor.split('=', 1)
        params[unquote_plus(chave)] = unquote_plus(valor)
    return params


def index(request):
    if request.startswith('POST'):
        params = extrair_params(request)
        db.add(Note(title=params['titulo'], content=params['detalhes']))
        return build_response(code=303, reason='See Other', headers='Location: /')

    note_template = load_template('components/note.html')
    notes_li = [
        note_template.format(id=nota.id, title=nota.title, details=nota.content)
        for nota in db.get_all()
    ]
    notes = '\n'.join(notes_li)
    return build_response(body=load_template('index.html').format(notes=notes))


def confirmar_exclusao(route):
    try:
        nota_id = int(route.split('/')[1])
    except (ValueError, IndexError):
        return nao_encontrado()
    nota = db.get(nota_id)
    if nota is None:
        return nao_encontrado()
    nota_id = int(route.split('/')[1])
    nota = db.get(nota_id)
    if nota is None:
        return build_response(code=303, reason='See Other', headers='Location: /')
    pagina = load_template('confirmar_exclusao.html')
    return build_response(body=pagina.format(id=nota.id, title=nota.title, details=nota.content))


def excluir(request):
    params = extrair_params(request)
    db.delete(int(params['id']))
    return build_response(code=303, reason='See Other', headers='Location: /')

def editar(route):
    try:
        nota_id = int(route.split('/')[1])
    except (ValueError, IndexError):
        return nao_encontrado()
    nota = db.get(nota_id)
    if nota is None:
        return nao_encontrado()
    nota_id = int(route.split('/')[1])
    nota = db.get(nota_id)
    if nota is None:
        return build_response(code=303, reason='See Other', headers='Location: /')
    pagina = load_template('editar.html')
    return build_response(body=pagina.format(id=nota.id, title=nota.title, details=nota.content))


def salvar_edicao(request):
    params = extrair_params(request)
    nota = Note(
        id=int(params['id']),
        title=params['titulo'],
        content=params['detalhes'],
    )
    db.update(nota)
    return build_response(code=303, reason='See Other', headers='Location: /')

def nao_encontrado():
    pagina = load_template('404.html')
    return build_response(body=pagina, code=404, reason='Not Found')