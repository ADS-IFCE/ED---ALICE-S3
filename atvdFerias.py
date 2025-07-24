import random


def iniciar_grade(n_linhas, n_colunas, inicial=' '):
    return tuple(tuple(inicial for _ in range(n_colunas)) for _ in range(n_linhas))


def n_colunas(grade):
    return len(grade[0])


def n_linhas(grade):
    return len(grade)


def print2D(grade):
    for linha in grade:
        print(''.join(linha))
    print()


def indice_valido(grade, linha, coluna):
    return 0 <= linha < n_linhas(grade) and 0 <= coluna < n_colunas(grade)


def acessar(grade, linha, coluna):
    if indice_valido(grade, linha, coluna):
        return grade[linha][coluna]
    return None


def alterar(grade, linha, coluna, valor):
    if not indice_valido(grade, linha, coluna):
        return grade
    nova_grade = tuple(
        tuple(
            valor if (i, j) == (linha, coluna) else grade[i][j]
            for j in range(n_colunas(grade))
        )
        for i in range(n_linhas(grade))
    )
    return nova_grade


# Jogo da cobra

def encontrar_cobra(grade):
    cabeca = None
    corpo = []

    for i in range(n_linhas(grade)):
        for j in range(n_colunas(grade)):
            if grade[i][j] == '@':
                cabeca = (i, j)
            elif grade[i][j] == 'C':
                corpo.append((i, j))

    corpo = ordenar_corpo(cabeca, corpo)
    return cabeca, corpo


def ordenar_corpo(cabeca, corpo):
    """Ordena o corpo da cobra da cabeça à cauda."""
    if not corpo:
        return []

    ordenado = []
    visitados = set()
    atual = cabeca

    while True:
        vizinhos = [(atual[0] + dx, atual[1] + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]
        prox = next((p for p in vizinhos if p in corpo and p not in visitados), None)
        if not prox:
            break
        ordenado.append(prox)
        visitados.add(prox)
        atual = prox

    return ordenado


def mover(pos, direcao):
    movimentos = {
        'w': (-1, 0),  # cima
        's': (1, 0),  # baixo
        'a': (0, -1),  # esquerda
        'd': (0, 1),  # direita
    }
    dx, dy = movimentos[direcao]
    return (pos[0] + dx, pos[1] + dy)


def gerar_alimento(grade):
    vazios = [
        (i, j)
        for i in range(n_linhas(grade))
        for j in range(n_colunas(grade))
        if grade[i][j] == ' '
    ]
    if vazios:
        pos = random.choice(vazios)
        return alterar(grade, pos[0], pos[1], '*')
    return grade


def mover_cobra(grade, direcao, pontuacao):
    cabeca, corpo = encontrar_cobra(grade)
    nova_cabeca = mover(cabeca, direcao)

    if not indice_valido(grade, *nova_cabeca):
        return grade, pontuacao, True

    conteudo = acessar(grade, *nova_cabeca)
    if conteudo in ('#', 'C'):
        return grade, pontuacao, True

    comeu = conteudo == '*'
    if comeu:
        pontuacao += 1

    novo_corpo = [cabeca] + corpo
    if not comeu:
        novo_corpo.pop()

    # Limpa a cobra antiga
    for x, y in [cabeca] + corpo:
        grade = alterar(grade, x, y, ' ')

    # Desenha corpo novo
    for x, y in novo_corpo:
        grade = alterar(grade, x, y, 'C')

    # Desenha cabeça
    grade = alterar(grade, nova_cabeca[0], nova_cabeca[1], '@')

    if comeu:
        grade = gerar_alimento(grade)

    return grade, pontuacao, False


# -----------------------
# LOOP DO JOGO
# -----------------------

def jogar():
    linhas, colunas = 10, 20
    grade = iniciar_grade(linhas, colunas)

    # Adiciona paredes
    for i in range(linhas):
        grade = alterar(grade, i, 0, '#')
        grade = alterar(grade, i, colunas - 1, '#')
    for j in range(colunas):
        grade = alterar(grade, 0, j, '#')
        grade = alterar(grade, linhas - 1, j, '#')

    # Cobra inicial
    grade = alterar(grade, 5, 7, 'C')
    grade = alterar(grade, 5, 8, '@')

    # Alimento inicial
    grade = alterar(grade, 3, 8, '*')

    pontuacao = 0
    fim = False

    print("🎮 Bem-vindo ao Snake!")
    print("Use as teclas W (cima), A (esquerda), S (baixo), D (direita).")
    print("Digite Q para sair.\n")

    while not fim:
        print2D(grade)
        print(f"🍎 Pontuação: {pontuacao}")
        comando = input("➡️ Movimento (w/a/s/d): ").lower()
        if comando == 'q':
            print("👋 Jogo encerrado pelo jogador.")
            break
        if comando not in ('w', 'a', 's', 'd'):
            print("❗ Movimento inválido. Use apenas w/a/s/d.")
            continue

        grade, pontuacao, fim = mover_cobra(grade, comando, pontuacao)

    print("\n💀 Fim de jogo!")
    print(f"🏆 Sua pontuação final foi: {pontuacao}")


# Inicia o jogo
jogar()
