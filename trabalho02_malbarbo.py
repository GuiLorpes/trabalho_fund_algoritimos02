import sys
from dataclasses import dataclass

def main():
    if len(sys.argv) < 2:
        print('Nenhum nome de arquivo informado.')
        sys.exit(1)
    if len(sys.argv) > 2:
        print('Muitos parâmetro. Informe apenas um nome de arquivo.')
        sys.exit(1)
    jogos = le_arquivo(sys.argv[1])

    # Pergunta 1
    lista_jogos = jogos_jogados(jogos)
    tabela = tabela_times(lista_jogos)
    ordenar_tabela(tabela)
    print_tabela(tabela)
    
    # Pergunta 2
    melhor_aprov = melhor_aproveitamento(tabela, lista_jogos)
    print(f'O time com melhor aproveitamento foi o {melhor_aprov.nome} com um \
aproveitamento de {melhor_aprov.aproveitamento}%')

    # Pergunta 3
    melhor_def = melhor_defesa(tabela, lista_jogos)
    print(f'O time com a defesa menos vazada foi o {melhor_def.nome} com apenas\
 {melhor_def.gols_tomados} gols sofridos')

# TODO: solução da pergunta 1

# Pergunta 1: Qual a classificação dos times no campeonato?

# Analise
# 
# Primeiro pegar o nome de cada time, e colocar em seu devido tipo enumerado,
# caso o time ja tiver um com seu nome, ignorar, depois, vamos verificar jogo
# por jogo para fazer o saldo dos gols, enquanto isso verificar a quantia de 
# vitorias e empates para somar os pontos, e por fim retornar a tabela em ordem.
#  
# Tipos de dados:
# 
# Vamos ter uma lista como entrada com os jogos, e na saida o tipo composto dos
# times. 

@dataclass
class TimeDeFutebol:
    '''
    Informações de um time de futebol, nome, pontuação, numero de vitorias,
    saldo de gols e aproveitamento.
    '''
    nome: str
    pontos: int
    num_vitorias: int
    saldo_gols: int
    aproveitamento: float
    gols_tomados: int

@dataclass
class JogosJogados:
    '''
    Informações de um jogo de um campeonato, time anfitriao, gols do time 
    anfitriao, time convidado, gols do time convidado, se terminou em empate, e
    quem venceu caso não tenha empatado
    '''
    anfitriao: str
    gols_anfitriao: int
    convidado: str
    gols_convidado: int

# Criar uma lista de jogos

def jogos_jogados (jogos: list[str]) -> list[JogosJogados]:
    '''
    Verifica o nome dos times nos *jogos* e coloca-os em uma lista.
    Exemplos
    >>> lista = ['Sao-Paulo 1 Atletico-MG 2', 'Flamengo 2 Palmeiras 1',
    ... 'Flamengo 2 Atletico-MG 2']
    >>> jogos_jogados(lista)
    [JogosJogados(anfitriao='Sao-Paulo', gols_anfitriao=1, convidado=\
'Atletico-MG', gols_convidado=2), \
JogosJogados(anfitriao='Flamengo', gols_anfitriao=2, convidado='Palmeiras', \
gols_convidado=1), \
JogosJogados(anfitriao='Flamengo', gols_anfitriao=2, convidado=\
'Atletico-MG', gols_convidado=2)]
    '''
    if jogos == []:
        jogos_campeonato: list[JogosJogados] = []
    else:
        times = []
        gols = []
        f = 0
        c = 0
        while f < len(jogos[0]):
            if jogos[0][f] == ' ' and jogos[0][c:f] != '' and not \
                eh_numero(jogos[0][c:f]):
                if jogos[0][c] == ' ':
                    times.append(jogos[0][c+1:f])    
                else:
                    times.append(jogos[0][c:f])
                t = f
                c = t
                f = c + 1
            if jogos[0][c] == ' ' and jogos[0][c:f] != '' and \
                eh_numero(jogos[0][f]):
                f += 1
                gols.append(int(jogos[0][c:f]))
                c = f
            f += 1
        jogos_campeonato = [(JogosJogados(times[0],gols[0],times[1],gols[1]))]\
              + jogos_jogados(jogos[1:])
    return jogos_campeonato

def eh_numero(s: str) -> bool:
    '''
    Verifica se uma string *s* é um numero.
    '''
    numeros = '0123456789'
    numero = False
    i = 0
    while i < 10 and not numero:
        if numeros[i] == s:
            numero = True
        i += 1
    return numero
 
# Arrumar no tipo de dados   

def tabela_times(jogos: list[JogosJogados]) -> list[TimeDeFutebol]:
    '''
    Cria uma lista de tipo de dados para os times nos *jogos*, adicionando o 
    nome, o saldo de gols, verifica qual dos times ganhou ou se houve empate, e
    adiciona os pontos e caso houve vitoria tambem o adiciona.
    Exemplo
    >>> lista = ['Sao-Paulo 1 Atletico-MG 2', 'Flamengo 2 Palmeiras 1',
    ... 'Flamengo 2 Atletico-MG 2']
    >>> jogos = jogos_jogados(lista)
    >>> tabela_times(jogos)
    [TimeDeFutebol(nome='Sao-Paulo', pontos=0, num_vitorias=0, saldo_gols=-1, \
aproveitamento=0.0, gols_tomados=2), \
TimeDeFutebol(nome='Atletico-MG', pontos=4, num_vitorias=1, saldo_gols=1, \
aproveitamento=0.0, gols_tomados=3), \
TimeDeFutebol(nome='Flamengo', pontos=4, num_vitorias=1, saldo_gols=1, \
aproveitamento=0.0, gols_tomados=3), \
TimeDeFutebol(nome='Palmeiras', pontos=0, num_vitorias=0, saldo_gols=-1, \
aproveitamento=0.0, gols_tomados=2)]
    '''
    tabela: list[TimeDeFutebol] = []
    for i in range(len(jogos)):
        if tabela == [] or not nome_repetido(tabela, jogos[i].anfitriao):
            tabela.append(TimeDeFutebol(jogos[i].anfitriao, 0, 0, 0, 0.0, 0))
        if not nome_repetido(tabela, jogos[i].convidado):
            tabela.append(TimeDeFutebol(jogos[i].convidado, 0, 0, 0, 0.0, 0))
    for jogo in jogos:
        saldo_anft = jogo.gols_anfitriao - jogo.gols_convidado
        saldo_conv = jogo.gols_convidado - jogo.gols_anfitriao
        j = 0
        while tabela[j].nome != jogo.anfitriao:
                j += 1
        tabela[j].saldo_gols += saldo_anft
        tabela[j].gols_tomados += jogo.gols_convidado
        if saldo_anft > 0:
            tabela[j].num_vitorias += 1
            tabela[j].pontos += 3
        if saldo_anft == 0:
            tabela[j].pontos += 1
        k = 0
        while tabela[k].nome != jogo.convidado:
            k += 1
        tabela[k].saldo_gols += saldo_conv
        tabela[k].gols_tomados += jogo.gols_anfitriao
        if saldo_conv > 0:
            tabela[k].num_vitorias += 1
            tabela[k].pontos += 3
        if saldo_conv == 0:
            tabela[k].pontos += 1
    return tabela
    
def nome_repetido(lst: list[TimeDeFutebol], time: str) -> bool:
    '''
    Verifica se o time de futebol já está na lista *lst*.
    '''
    repetido = False
    i = 0
    while i < len(lst) and not repetido:
        if lst[i].nome == time:
            repetido = True
        i += 1
    return repetido

# Organizar a tabela 

def ordenar_tabela(tabela: list[TimeDeFutebol]) -> None:
    '''
    Organiza a *tabela* em ordem de maior ponto, caso empatar nos pontos, o 
    desempate será pela quantia de vitorias, caso empatar também, o desempate
    será usando o saldo de gols, e caso empatar novamente, o desempate será por
    ordem alfabética.
    Exemplos
    >>> lista = ['Sao-Paulo 1 Atletico-MG 2', 'Flamengo 2 Palmeiras 1',
    ... 'Flamengo 2 Atletico-MG 2','Sao-Paulo 3 Palmeiras 0', 
    ... 'Fluminense 2 Maringá 0', 'Maringá 0 Fluminense 0',
    ... 'Cuiaba 2 Corinthians 2', 'Corinthians 0 Cuiaba 0',
    ... 'Corinthians 0 Palmeiras 0']
    >>> jogos = jogos_jogados(lista)
    >>> tabela = tabela_times(jogos)
    >>> ordenar_tabela(tabela)
    >>> tabela
    [TimeDeFutebol(nome='Fluminense', pontos=4, num_vitorias=1, saldo_gols=2, \
aproveitamento=0.0, gols_tomados=0), \
TimeDeFutebol(nome='Atletico-MG', pontos=4, num_vitorias=1, saldo_gols=1, \
aproveitamento=0.0, gols_tomados=3), \
TimeDeFutebol(nome='Flamengo', pontos=4, num_vitorias=1, saldo_gols=1, \
aproveitamento=0.0, gols_tomados=3), \
TimeDeFutebol(nome='Sao-Paulo', pontos=3, num_vitorias=1, saldo_gols=2, \
aproveitamento=0.0, gols_tomados=2), \
TimeDeFutebol(nome='Corinthians', pontos=3, num_vitorias=0, saldo_gols=0, \
aproveitamento=0.0, gols_tomados=2), \
TimeDeFutebol(nome='Cuiaba', pontos=2, num_vitorias=0, saldo_gols=0, \
aproveitamento=0.0, gols_tomados=2), \
TimeDeFutebol(nome='Maringá', pontos=1, num_vitorias=0, saldo_gols=-2, \
aproveitamento=0.0, gols_tomados=2), \
TimeDeFutebol(nome='Palmeiras', pontos=1, num_vitorias=0, saldo_gols=-4, \
aproveitamento=0.0, gols_tomados=5)]
    ''' 
    for i in range (len(tabela) - 1):
        j_max = i
        for j in range(i + 1, len(tabela)):
            if condicao(tabela[j], tabela[j_max]):
                j_max = j
        t = tabela[i]
        tabela[i] = tabela[j_max]
        tabela[j_max] = t

def condicao(t1: TimeDeFutebol, t2: TimeDeFutebol) -> bool:
    ''' Define se será necessario ordenar a lista '''
    return  t1.pontos > t2.pontos or \
            (t1.pontos == t2.pontos and t1.num_vitorias > t2.num_vitorias) or \
            (t1.pontos == t2.pontos and t1.num_vitorias == t2.num_vitorias and \
             t1.saldo_gols > t2.saldo_gols) or (t1.pontos == t2.pontos and \
            t1.num_vitorias == t2.num_vitorias and t1.saldo_gols == \
            t2.saldo_gols and t1.nome < t2.nome)

def print_tabela(tabela: list[TimeDeFutebol]) -> None:
    '''
    Imprime no terminal a *tabela* com a devida formatação.
    Exemplo:
    Flamengo    6 2  2
    Atletico-MG 3 1  0
    Palmeiras   1 0 -1
    Sao-Paulo   1 0 -1 
    '''
    espaco_nome = 0
    espaco_pontos = 0
    espaco_vitorias = 0
    espaco_gols = 0
    for time in tabela:
        if len(time.nome) > espaco_nome:
            espaco_nome = len(time.nome)
        if len(str(time.pontos)) > espaco_pontos:
            espaco_pontos = len(str(time.pontos))
        if len(str(time.num_vitorias)) > espaco_vitorias:
            espaco_vitorias = len(str(time.num_vitorias))
        if len(str(time.saldo_gols)) > espaco_gols:
            espaco_gols = len(str(time.saldo_gols))
    for time in tabela:
        nome = time.nome + ' ' * (espaco_nome - len(time.nome))
        pontos = ' ' * (espaco_pontos - len(str(time.pontos))) + \
            str(time.pontos)
        vitorias = ' ' * (espaco_vitorias - len(str(time.num_vitorias))) + \
            str(time.num_vitorias)
        saldo_gols = ' ' * (espaco_gols - len(str(time.saldo_gols))) + \
            str(time.saldo_gols)
        print(f'{nome} {pontos} {vitorias} {saldo_gols}')
        
# TODO: solução da pergunta 2

# Pergunta 2: Qual o time com melhor aproveitamento jogando como anfitrião?
# 
# Analise
# 
# Identificar a quantia de vezes que um time hospedou as partidas e determinar
# o aproveitamento dele, fazer isso com a lista dos times, e então retornar o
# time com melhor aproveitamento.
# 
# Tipo de dados
# 
# Lista do time de futebol, e a lista dos jogos, para retornar o nome de um dos
# times.

def melhor_aproveitamento(tabela: list[TimeDeFutebol], jogos: list[JogosJogados]) \
    -> TimeDeFutebol:
    '''
    Calcula o aproveitamento dos times da *tabela* jogando como anfitrioes nos
    *jogos* e verifica qual teve o melhor aproveitamento.
    Exemplo
    >>> lista = ['Sao-Paulo 1 Atletico-MG 2', 'Flamengo 2 Palmeiras 1',
    ... 'Flamengo 2 Atletico-MG 2', 'Sao-Paulo 0 Palmeiras 2']
    >>> jogos = jogos_jogados(lista)
    >>> tabela = tabela_times(jogos)
    >>> melhor_aproveitamento(tabela, jogos).nome
    'Flamengo'
    '''
    melhor_time = tabela[0]
    for time in tabela:
        pontos_anfitriao = pontos_como_anfitriao(time.nome, jogos)
        jogos_anfitriao = frequencia_anfitriao(time.nome, jogos)
        if jogos_anfitriao != 0:
            time.aproveitamento = round(((pontos_anfitriao / \
                                          (jogos_anfitriao * 3)) * 100),2)
        if time.aproveitamento > melhor_time.aproveitamento:
                melhor_time = time
    return melhor_time

def frequencia_anfitriao(time: str, jogos: list[JogosJogados]) -> int:
    '''
    Verifica a quantia de vezes que um *time* hospedou *jogos* no campeonato.
    Exemplo:
    >>> lista = ['Sao-Paulo 1 Atletico-MG 2', 'Flamengo 2 Palmeiras 1',
    ... 'Flamengo 2 Atletico-MG 2', 'Sao-Paulo 0 Palmeiras 2']
    >>> jogos = jogos_jogados(lista)
    >>> frequencia_anfitriao('Flamengo', jogos)
    2
    '''
    if jogos == []:
        freq = 0
    else:
        if time == jogos[0].anfitriao:
            freq = 1 + frequencia_anfitriao(time, jogos[1:])
        else:
            freq = frequencia_anfitriao(time, jogos[1:])
    return freq

def pontos_como_anfitriao(time: str, jogos: list[JogosJogados]) -> int:
    '''
    Calcula a quantia de pontos que o *time* fez nos *jogos* como anfitriao e
    adiciona essa quantia no Tipo de dados
    Exemplo:
    >>> lista = ['Sao-Paulo 1 Atletico-MG 2', 'Flamengo 2 Palmeiras 1',
    ... 'Flamengo 2 Atletico-MG 2', 'Sao-Paulo 0 Palmeiras 2']
    >>> time1 = TimeDeFutebol('Flamengo', 4, 1, 1, 0.0, 3)
    >>> time2 = TimeDeFutebol('Palmeiras', 3, 1, 1, 0.0, 2)
    >>> jogos = jogos_jogados(lista)
    >>> pontos_como_anfitriao(time1.nome, jogos)
    4
    >>> pontos_como_anfitriao(time2.nome, jogos)
    0
    '''
    if jogos == []:
        pontos = 0
    else:
        saldo_anft = jogos[0].gols_anfitriao - jogos[0].gols_convidado
        if time == jogos[0].anfitriao:
            if saldo_anft > 0:
                pontos = 3 + pontos_como_anfitriao(time, jogos[1:])
            elif saldo_anft == 0:
                pontos = 1 + pontos_como_anfitriao(time, jogos[1:])
            else:
                pontos = pontos_como_anfitriao(time, jogos[1:])
        else: # time != jogos[0].anfitriao
            pontos = pontos_como_anfitriao(time, jogos[1:])
    return pontos

# TODO: solução da pergunta 3

# Pergunta 3: Qual o time com a defesa menos vazada?

# Analise
# 
# Identificar os jogos que o time jogou, somar a quantia de gols tomados,
# e retornar o time com menor gols sofridos
# 
# Tipos de dados:
#
# Lista de jogos e um time em forma de string como resposta 

def melhor_defesa(tabela: list[TimeDeFutebol], jogos: list[JogosJogados]) \
    -> TimeDeFutebol:
    '''
    Verifica os *jogos* que o time da *tabela* jogou, soma a quantia de gols
    sofridos pelo time, e retorna o time com menos gols tomados
    Exemplo
    >>> lista = ['Sao-Paulo 1 Atletico-MG 2', 'Flamengo 2 Palmeiras 1',
    ... 'Flamengo 2 Atletico-MG 2', 'Sao-Paulo 0 Palmeiras 2']
    >>> jogos = jogos_jogados(lista)
    >>> tabela = tabela_times(jogos)
    >>> melhor_defesa(tabela, jogos).nome
    'Palmeiras'
    '''
    melhor = tabela[0]
    for i in range (1, len(tabela)):
        if tabela[i].gols_tomados < melhor.gols_tomados:
            melhor = tabela[i]
    return melhor

def le_arquivo(nome: str) -> list[str]:
    '''
    Lê o conteúdo do arquivo *nome* e devolve uma lista onde cada elemento
    representa uma linha.
    Por exemplo, se o conteúdo do arquivo for
    Sao-Paulo 1 Atletico-MG 2
    Flamengo 2 Palmeiras 1
    a resposta produzida é
    [‘Sao-Paulo 1 Atletico-MG 2’, ‘Flamengo 2 Palmeiras 1’]
    '''
    try:
        with open(nome) as f:
            return f.readlines()
    except IOError as e:
        print(f'Erro na leitura do arquivo "{nome}": {e.errno} - {e.strerror}.');
        sys.exit(1)

if __name__ == '__main__':
    main()
