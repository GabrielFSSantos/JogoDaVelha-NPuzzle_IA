from math import inf as infinity
from random import choice
import platform
import time
from os import system

HUMANO = -1
COMP = +1
tabuleiro = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]

def avaliacao(estado):
    
    if vitoria(estado, COMP):
        placar = +1
    elif vitoria(estado, HUMANO):
        placar = -1
    else:
        placar = 0

    return placar

def vitoria(estado, jogador):
    win_estado = [
        [estado[0][0], estado[0][1], estado[0][2]],
        [estado[1][0], estado[1][1], estado[1][2]],
        [estado[2][0], estado[2][1], estado[2][2]],
        [estado[0][0], estado[1][0], estado[2][0]],
        [estado[0][1], estado[1][1], estado[2][1]],
        [estado[0][2], estado[1][2], estado[2][2]],
        [estado[0][0], estado[1][1], estado[2][2]],
        [estado[2][0], estado[1][1], estado[0][2]],
    ]
    if [jogador, jogador, jogador] in win_estado:
        return True
    else:
        return False

def fim_jogo(estado):
    return vitoria(estado, HUMANO) or vitoria(estado, COMP)

def celulas_vazias(estado):
    celulas = []
    for x, row in enumerate(estado):
        for y, cell in enumerate(row):
            if cell == 0: celulas.append([x, y])
    return celulas

def movimento_valido(x, y):
    if [x, y] in celulas_vazias(tabuleiro):
        return True
    else:
        return False

def exec_movimento(x, y, jogador):
    if movimento_valido(x, y):
        tabuleiro[x][y] = jogador
        return True
    else:
        return False

def minimax(estado, profundidade, jogador):

    if jogador == COMP:
        melhor = [-1, -1, -infinity]
    else:
        melhor = [-1, -1, +infinity]

    if profundidade == 0 or fim_jogo(estado):
        placar = avaliacao(estado)
        return [-1, -1, placar]

    for cell in celulas_vazias(estado):
        x, y = cell[0], cell[1]
        estado[x][y] = jogador
        placar = minimax(estado, profundidade - 1, -jogador)
        estado[x][y] = 0
        placar[0], placar[1] = x, y

        if jogador == COMP:
            if placar[2] > melhor[2]:
                melhor = placar
        else:
            if placar[2] < melhor[2]:
                melhor = placar
    return melhor

def limpa_console():
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')

def exibe_tabuleiro(estado, comp_escolha, humano_escolha):
    print('----------------')
    for row in estado:
        print('\n----------------')
        for cell in row:
            if cell == +1:
                print('|', comp_escolha, '|', end='')
            elif cell == -1:
                print('|', humano_escolha, '|', end='')
            else:
                print('|', ' ', '|', end='')
    print('\n----------------')

def IA_vez(comp_escolha, humano_escolha):
    profundidade = len(celulas_vazias(tabuleiro))
    if profundidade == 0 or fim_jogo(tabuleiro):
        return

    limpa_console()
    print('Vez do Computador [{}]'.format(comp_escolha))
    exibe_tabuleiro(tabuleiro, comp_escolha, humano_escolha)

    if profundidade == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move = minimax(tabuleiro, profundidade, COMP)
        x, y = move[0], move[1]

    exec_movimento(x, y, COMP)
    time.sleep(1)

def HUMANO_vez(comp_escolha, humano_escolha):

    profundidade = len(celulas_vazias(tabuleiro))
    if profundidade == 0 or fim_jogo(tabuleiro):
        return

    movimento = -1
    movimentos = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    limpa_console()
    print('Vez do HUMANO [{}]'.format(humano_escolha))
    exibe_tabuleiro(tabuleiro, comp_escolha, humano_escolha)

    while (movimento < 1 or movimento > 9):
        try:
            movimento = int(input('Use numero (1..9): '))
            coord = movimentos[movimento]
            tenta_movimento = exec_movimento(coord[0], coord[1], HUMANO)

            if tenta_movimento == False:
                print('Movimento Inválido')
                movimento = -1
        except KeyboardInterrupt:
            print('Tchau!')
            exit()
        except:
            print('Escolha Inválida!')

def main():

    limpa_console()
    humano_escolha = ''
    comp_escolha = ''
    primeiro = ''

    while humano_escolha != 'O' and humano_escolha != 'X':
        try:
            print('')
            humano_escolha = input('Escolha X or O\n: ').upper()
        except KeyboardInterrupt:
            print('Tchau!')
            exit()
        except:
            print('Escolha Errada')

    if humano_escolha == 'X':
        comp_escolha = 'O'
    else:
        comp_escolha = 'X'

    limpa_console()
    while primeiro != 'S' and primeiro != 'N':
        try:
            primeiro = input('Primeiro a Iniciar?[s/n]: ').upper()
        except KeyboardInterrupt:
            print('Tchau!')
            exit()
        except:
            print('Escolha Errada!')

    while len(celulas_vazias(tabuleiro)) > 0 and not fim_jogo(tabuleiro):
        if primeiro == 'N':
            IA_vez(comp_escolha, humano_escolha)
            primeiro = ''

        HUMANO_vez(comp_escolha, humano_escolha)
        IA_vez(comp_escolha, humano_escolha)

    if vitoria(tabuleiro, HUMANO):
        limpa_console()
        print('Vez do HUMANO [{}]'.format(humano_escolha))
        exibe_tabuleiro(tabuleiro, comp_escolha, humano_escolha)
        print('Você Venceu!')
    elif vitoria(tabuleiro, COMP):
        limpa_console()
        print('Vez do Computador [{}]'.format(comp_escolha))
        exibe_tabuleiro(tabuleiro, comp_escolha, humano_escolha)
        print('Você Perdeu!')
    else:
        limpa_console()
        exibe_tabuleiro(tabuleiro, comp_escolha, humano_escolha)
        print('Empate!')

    exit()

if __name__ == '__main__':
    main()