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


def index(erro=''):
    note_template = load_template('components/note.html')
    notes_li = [
        note_template.format(id=nota.id, title=nota.title, details=nota.content,
                             fav_icone='⭐' if nota.favorite else '☆',
                             fav_classe='favorita' if nota.favorite else '')
        for nota in db.get_all()
    ]
    notes = '\n'.join(notes_li)
    if erro:
        erro_html = f'<p class="form-erro">{erro}</p>'
    else:
        erro_html = ''
    pagina = load_template('index.html')
    return build_response(body=pagina.format(notes=notes, erro=erro_html))


def create(request):
    params = extrair_params(request)
    titulo = params.get('titulo', '').strip()
    detalhes = params.get('detalhes', '').strip()
    if not titulo or not detalhes:
        return index(erro='Preencha o título e o conteúdo da anotação.')
    db.add(Note(title=titulo, content=detalhes))
    return build_response(code=303, reason='See Other', headers='Location: /')


def favoritar(request):
    params = extrair_params(request)
    db.alternar_favorito(int(params['id']))
    return build_response(code=303, reason='See Other', headers='Location: /')


def confirmar_exclusao(route):
    try:
        nota_id = int(route.split('/')[1])
    except (ValueError, IndexError):
        return nao_encontrado()
    nota = db.get(nota_id)
    if nota is None:
        return nao_encontrado()
    pagina = load_template('confirmar_exclusao.html')
    return build_response(body=pagina.format(id=nota.id, title=nota.title,
                                             details=nota.content))


def excluir(request):
    params = extrair_params(request)
    db.delete(int(params['id']))
    return build_response(code=303, reason='See Other', headers='Location: /')


def pagina_edicao(nota, erro=''):
    if erro:
        erro_html = f'<p class="form-erro">{erro}</p>'
    else:
        erro_html = ''
    pagina = load_template('editar.html')
    return build_response(body=pagina.format(id=nota.id, title=nota.title,
                                             details=nota.content,
                                             erro=erro_html))


def editar(route):
    try:
        nota_id = int(route.split('/')[1])
    except (ValueError, IndexError):
        return nao_encontrado()
    nota = db.get(nota_id)
    if nota is None:
        return nao_encontrado()
    return pagina_edicao(nota)


def salvar_edicao(request):
    params = extrair_params(request)
    nota_id = int(params['id'])
    titulo = params.get('titulo', '').strip()
    detalhes = params.get('detalhes', '').strip()
    nota = Note(id=nota_id, title=titulo, content=detalhes)
    if not titulo or not detalhes:
        return pagina_edicao(nota, erro='Preencha o título e o conteúdo da anotação.')
    db.update(nota)
    return build_response(code=303, reason='See Other', headers='Location: /')


def nao_encontrado():
    pagina = load_template('404.html')
    return build_response(body=pagina, code=404, reason='Not Found')