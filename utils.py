def extract_route(requisicao):
    route = requisicao.split()[1].removeprefix('/')
    print(f'rota extraída: {route}')
    return route

r = '''GET /img/logo-getit.png HTTP/1.1
Host: 0.0.0.0:8080
Connection: keep-alive
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36
Accept: image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8
Referer: http://0.0.0.0:8080/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9,pt;q=0.8
'''

extract_route(r)

def read_file(filepath):
    with open(filepath, 'rb') as arquivo:
        return arquivo.read()


def load_data(arquivo):
    
    