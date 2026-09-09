import sqlite3

class BD:

    def __init__(self):
        self.con = sqlite3.connect("filmes.db", check_same_thread=False)
        cursor = self.con.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS filmes(id integer primary key, nome, idade, filme, categoria, nota)')
        self.con.commit()
        cursor.close()

    def __del__(self):
        self.con.close()

    def inserir(self, nome, idade, filme, categoria, nota):
        cursor = self.con.cursor()
        cursor.execute('INSERT INTO filmes(nome, idade, filme, categoria, nota) VALUES(?, ?, ?, ?, ?)', (nome, idade, filme, categoria, nota))
        if (cursor.rowcount > 0):
            self.con.commit()
            id = cursor.lastrowid
        else:
            id = None
        cursor.close()
        return id

    def buscarUm(self, id):
        cursor = self.con.cursor()
        cursor.execute('SELECT * FROM filmes WHERE id = ?', (id,))
        dado = cursor.fetchone()
        cursor.close()
        return dado

    def atualizar(self, id, nome, idade, filme, categoria, nota):
        cursor = self.con.cursor()
        cursor.execute('UPDATE filmes SET nome = ?, idade = ?, filme = ?, categoria = ?, nota = ? WHERE id = ?', (nome, idade, filme, categoria, nota, id))
        sucesso = cursor.rowcount > 0
        if sucesso:
            self.con.commit()
        cursor.close()
        return sucesso

    def deletar(self, id):
        cursor = self.con.cursor()
        cursor.execute('DELETE FROM filmes WHERE id = ?', (id,))
        sucesso = cursor.rowcount > 0
        if sucesso:
            self.con.commit()
        cursor.close()
        return sucesso
