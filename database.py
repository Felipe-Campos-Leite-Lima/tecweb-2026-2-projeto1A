import sqlite3

from dataclasses import dataclass

@dataclass
class Note:
    id: int = None
    title: str = None
    content: str = ''

class Database:
    def __init__(self,banco):
        self.banco = banco
        self.conn = sqlite3.connect(banco +'.db')

        self.conn.execute("""CREATE TABLE IF NOT EXISTS note ( id INTEGER PRIMARY KEY,
                                            title TEXT,
                                            content TEXT NOT NULL );""")

    def add(self,note:Note):
        self.conn.execute(f'INSERT INTO note (title,content) VALUES ("{note.title}","{note.content}");')
        self.conn.commit()

    def get_all(self):
        cursor = self.conn.execute("SELECT id, title, content FROM note")
        resultado = []
        for linha in cursor:
            id = linha[0]
            title = linha[1]
            content = linha[2]  
            nota = Note(id = id, title=title, content=content)
            resultado.append(nota)
        return resultado    

    def update(self, entry:Note):
        self.conn.execute(f'UPDATE note SET title = "{entry.title}", content = "{entry.content}" WHERE id = {entry.id} ')
        self.conn.commit()
        
    def delete(self, note_id):
        self.conn.execute(f'DELETE FROM note WHERE id = {note_id}')
        self.conn.commit()
        