import socket
import banco
import struct
import sys

class CRUD:

    def __init__(self):
        self.banco = banco.BD()
        self.escutador = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        endereco = ('',50004)
        self.escutador.bind(endereco)

    def escutarConexoes(self):

        try:
            self.escutador.listen(1)
            dados, _ = self.escutador.accept()
            conectado = True
            while conectado:
                op = int.from_bytes(dados.recv(1),'big')
                if op == 5:
                    conectado = False
                else:
                    self.processarRequisicoes(op, dados)
            dados.close()
        except KeyboardInterrupt:
            self.escutador.close()
            sys.exit(-1)

    def processarRequisicoes(self, op, dados:socket.socket):
        match op:
            case 1:
                tam_nome = int.from_bytes(dados.recv(1),'big')
                nome = dados.recv(tam_nome).decode()
                idade = int.from_bytes(dados.recv(1),'big')
                tam_filme = int.from_bytes(dados.recv(1),'big')
                filme = dados.recv(tam_filme).decode()
                tam_categoria = int.from_bytes(dados.recv(1),'big')
                categoria = dados.recv(tam_categoria).decode()
                nota = struct.unpack(">d", dados.recv(8))
                id = self.create(nome, idade, filme, categoria, nota[0])
                resposta = op.to_bytes(1,'big') + id.to_bytes(2,'big',signed=True)
                dados.send(resposta)

            case 2:
                id = int.from_bytes(dados.recv(1),'big')
                ret = self.read(id)
                if ret is not None:
                    nome_b = ret[1].encode()
                    filme_b = ret[3].encode()
                    categoria_b = ret[4].encode()
                    mensagem = op.to_bytes(1,'big') + ret[0].to_bytes(2,'big',signed=True)
                    mensagem = mensagem + len(nome_b).to_bytes(1,'big') + nome_b
                    mensagem = mensagem + ret[2].to_bytes(1,'big')
                    mensagem = mensagem + len(filme_b).to_bytes(1,'big') + filme_b
                    mensagem = mensagem + len(categoria_b).to_bytes(1,'big') + categoria_b
                    mensagem = mensagem + struct.pack(">d", ret[5])
                else:
                    id_resp = -1
                    mensagem = op.to_bytes(1,'big') + id_resp.to_bytes(2,'big',signed=True)
                dados.send(mensagem)

            case 3:
                id = int.from_bytes(dados.recv(1),'big')
                tam_nome = int.from_bytes(dados.recv(1),'big')
                nome = dados.recv(tam_nome).decode()
                idade = int.from_bytes(dados.recv(1),'big')
                tam_filme = int.from_bytes(dados.recv(1),'big')
                filme = dados.recv(tam_filme).decode()
                tam_categoria = int.from_bytes(dados.recv(1),'big')
                categoria = dados.recv(tam_categoria).decode()
                nota = struct.unpack(">d", dados.recv(8))
                sucesso = self.update(id, nome, idade, filme, categoria, nota[0])
                resposta = op.to_bytes(1,'big') + (1 if sucesso else 0).to_bytes(1,'big')
                dados.send(resposta)

            case 4:
                id = int.from_bytes(dados.recv(1),'big')
                sucesso = self.delete(id)
                resposta = op.to_bytes(1,'big') + (1 if sucesso else 0).to_bytes(1,'big')
                dados.send(resposta)


    def create(self, nome, idade, filme, categoria, nota):
        return self.banco.inserir(nome, idade, filme, categoria, nota)

    def read(self, id):
        return self.banco.buscarUm(id)

    def update(self, id, nome, idade, filme, categoria, nota):
        return self.banco.atualizar(id, nome, idade, filme, categoria, nota)

    def delete(self, id):
        return self.banco.deletar(id)


def main():

    c = CRUD()
    while True:
        c.escutarConexoes()

if __name__ == '__main__':
    main()
