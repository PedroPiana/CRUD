import socket
import struct

dados = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dados.connect(('localhost',50004))

op = None

while op != 5:

    op = int(input('\nDigite 1 para criar, 2 para ler, 3 para atualizar, 4 para deletar, 5 para sair: '))
    match op:
        case 1:
            nome = input('Nome da pessoa: ')
            idade = int(input('Idade: '))
            filme = input('Filme favorito: ')
            categoria = input('Categoria: ')
            nota = float(input('Nota do filme: '))
            nome_b = nome.encode()
            filme_b = filme.encode()
            categoria_b = categoria.encode()
            mensagem = op.to_bytes(1,'big') + len(nome_b).to_bytes(1,'big')
            mensagem = mensagem + nome_b + idade.to_bytes(1,'big')
            mensagem = mensagem + len(filme_b).to_bytes(1,'big') + filme_b
            mensagem = mensagem + len(categoria_b).to_bytes(1,'big') + categoria_b
            mensagem = mensagem + struct.pack(">d", nota)
            dados.send(mensagem)
            dados.recv(1)
            id = int.from_bytes(dados.recv(2),'big',signed=True)
            if id > 0:
                print('Inserido com id', str(id))
            else:
                print('Erro de inserção')

        case 2:
            id = int(input('Digite id: '))
            mensagem = op.to_bytes(1,'big') + id.to_bytes(1,'big')
            dados.send(mensagem)
            dados.recv(1)
            id = int.from_bytes(dados.recv(2),'big',signed=True)
            if id > 0:
                tam_nome = int.from_bytes(dados.recv(1),'big')
                nome = dados.recv(tam_nome).decode()
                idade = int.from_bytes(dados.recv(1),'big')
                tam_filme = int.from_bytes(dados.recv(1),'big')
                filme = dados.recv(tam_filme).decode()
                tam_categoria = int.from_bytes(dados.recv(1),'big')
                categoria = dados.recv(tam_categoria).decode()
                nota = struct.unpack(">d", dados.recv(8))
                print('Nome:', nome)
                print('Idade:', idade)
                print('Filme favorito:', filme)
                print('Categoria:', categoria)
                print('Nota:', nota[0])
            else:
                print('não encontrado')

        case 3:
            id = int(input('Digite id: '))
            nome = input('Novo nome: ')
            idade = int(input('Nova idade: '))
            filme = input('Novo filme favorito: ')
            categoria = input('Nova categoria: ')
            nota = float(input('Nova nota: '))
            nome_b = nome.encode()
            filme_b = filme.encode()
            categoria_b = categoria.encode()
            mensagem = op.to_bytes(1,'big') + id.to_bytes(1,'big')
            mensagem = mensagem + len(nome_b).to_bytes(1,'big') + nome_b
            mensagem = mensagem + idade.to_bytes(1,'big')
            mensagem = mensagem + len(filme_b).to_bytes(1,'big') + filme_b
            mensagem = mensagem + len(categoria_b).to_bytes(1,'big') + categoria_b
            mensagem = mensagem + struct.pack(">d", nota)
            dados.send(mensagem)
            dados.recv(1)
            sucesso = int.from_bytes(dados.recv(1),'big')
            if sucesso == 1:
                print('Atualizado com sucesso')
            else:
                print('Erro ao atualizar (id não encontrado?)')

        case 4:
            id = int(input('Digite id: '))
            mensagem = op.to_bytes(1,'big') + id.to_bytes(1,'big')
            dados.send(mensagem)
            dados.recv(1)
            sucesso = int.from_bytes(dados.recv(1),'big')
            if sucesso == 1:
                print('Deletado com sucesso')
            else:
                print('Erro ao deletar (id não encontrado?)')

        case 5:
            mensagem = op.to_bytes(1,'big')
            dados.send(mensagem)
            print('Saindo...')

dados.close()
