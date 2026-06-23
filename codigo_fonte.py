# =============================================================================
#  SIGIC — SISTEMA INTELIGENTE DE GERENCIAMENTO DA INFRAESTRUTURA DA COLÔNIA
#  Aurora Siger | FIAP — Ciência da Computação — Fase 4
#  Grupo: Gabriel, Lucas, Matheus, Miguel e Pedro
# =============================================================================

import math
import os
import random
from collections import deque


def limpar():
    # aguarda confirmação do usuário e limpa o terminal antes de voltar ao menu
    input("\n  Pressione Enter para voltar ao menu...")
    os.system("cls" if os.name == "nt" else "clear")


# =============================================================================
#  BLOCO 1 — ESTRUTURAS DE DADOS DA INFRAESTRUTURA
#
#  Justificativa das estruturas escolhidas:
#    - Dicionário (módulos): acesso direto por chave, ideal para recuperar
#      atributos de qualquer módulo sem varredura sequencial.
#    - Lista de tuplas (arestas): conexões físicas são fixas após a construção
#      da base; tuplas impedem alterações acidentais.
#    - Lista de listas (matriz_adj): matriz 8x8 — adequada para o tamanho
#      da rede e permite acesso O(1) entre pares de módulos.
#    - Dicionário de listas (lista_adj): eficiente para percorrer vizinhos
#      em BFS, DFS e Dijkstra sem varrer colunas zeradas da matriz.
# =============================================================================

def gerar_modulos():
    # gera os módulos com valores operacionais aleatórios dentro de faixas reais
    # a cada execução os sensores retornam leituras diferentes — simulando
    # condições variadas da colônia; os valores de consumo e status mudam
    # a cada inicialização, representando leituras dinâmicas dos sensores da base
    return {
        "HAB": {
            "nome":             "Habitação",
            "consumo_kw":       round(random.uniform(15.0, 22.0), 1),
            "prioridade":       4,
            "armazenamento_kw": 0.0,
            "freq_comunicacao": "Baixa",
            "status":           random.choices(["ATIVO", "ALERTA"], weights=[90, 10])[0],
            "descricao":        "Acomodação da tripulação e suporte básico à sobrevivência"
        },
        "MED": {
            "nome":             "Suporte Médico",
            "consumo_kw":       round(random.uniform(9.0, 15.0), 1),
            "prioridade":       5,
            "armazenamento_kw": 0.0,
            "freq_comunicacao": "Alta",
            "status":           random.choices(["ATIVO", "ALERTA"], weights=[95, 5])[0],
            "descricao":        "Atendimento médico e monitoramento da saúde da tripulação"
        },
        "OXI": {
            "nome":             "Produção de Oxigênio",
            "consumo_kw":       round(random.uniform(18.0, 26.0), 1),
            "prioridade":       5,
            "armazenamento_kw": round(random.uniform(20.0, 50.0), 1),
            "freq_comunicacao": "Média",
            "status":           random.choices(["ATIVO", "ALERTA"], weights=[93, 7])[0],
            "descricao":        "Geração e distribuição de oxigênio para toda a base"
        },
        "CTR": {
            "nome":             "Centro de Controle",
            "consumo_kw":       round(random.uniform(12.0, 18.0), 1),
            "prioridade":       4,
            "armazenamento_kw": 0.0,
            "freq_comunicacao": "Alta",
            "status":           random.choices(["ATIVO", "ALERTA"], weights=[92, 8])[0],
            "descricao":        "Monitoramento e gerenciamento das operações da colônia"
        },
        "ENE": {
            "nome":             "Armazenamento de Energia",
            "consumo_kw":       round(random.uniform(3.0, 7.0), 1),
            "prioridade":       5,
            "armazenamento_kw": 500.0,
            "carga_pct":        round(random.uniform(20.0, 100.0), 1),
            "freq_comunicacao": "Média",
            "status":           random.choices(["ATIVO", "ALERTA"], weights=[95, 5])[0],
            "descricao":        "Armazena energia produzida pelos sistemas solar e eólico"
        },
        "AGR": {
            "nome":             "Agricultura",
            "consumo_kw":       round(random.uniform(15.0, 25.0), 1),
            "prioridade":       2,
            "armazenamento_kw": 0.0,
            "freq_comunicacao": "Baixa",
            "status":           random.choices(["ATIVO", "ALERTA", "MANUTENÇÃO"], weights=[80, 12, 8])[0],
            "descricao":        "Produção de alimentos e suporte à sustentabilidade da colônia"
        },
        "LAB": {
            "nome":             "Laboratório Científico",
            "consumo_kw":       round(random.uniform(10.0, 18.0), 1),
            "prioridade":       2,
            "armazenamento_kw": 0.0,
            "freq_comunicacao": "Alta",
            "status":           random.choices(["ATIVO", "ALERTA", "MANUTENÇÃO"], weights=[82, 12, 6])[0],
            "descricao":        "Pesquisas e análises de materiais e condições marcianas"
        },
        "COM": {
            "nome":             "Comunicação",
            "consumo_kw":       round(random.uniform(8.0, 13.0), 1),
            "prioridade":       3,
            "armazenamento_kw": 0.0,
            "freq_comunicacao": "Alta",
            "status":           random.choices(["ATIVO", "ALERTA"], weights=[88, 12])[0],
            "descricao":        "Troca de dados entre módulos e comunicação com a Terra"
        }
    }


# lista de tuplas com as arestas fixas da rede — (módulo_A, módulo_B, distância_metros)
# a infraestrutura física da colônia não muda entre execuções
arestas = [
    ("HAB", "MED",  50),
    ("HAB", "OXI",  30),
    ("HAB", "CTR",  80),
    ("HAB", "ENE",  55),
    ("HAB", "COM",  75),
    ("CTR", "ENE",  40),
    ("CTR", "COM",  60),
    ("CTR", "LAB",  70),
    ("ENE", "OXI",  35),
    ("ENE", "AGR",  90),
    ("ENE", "MED",  45),
    ("OXI", "MED",  40),
    ("AGR", "LAB",  65),
]

# lista de IDs para indexação numérica da matriz de adjacência
ids_modulos = ["HAB", "MED", "OXI", "CTR", "ENE", "AGR", "LAB", "COM"]
n           = len(ids_modulos)

# mapeamento ID -> índice numérico
indice = {mod_id: i for i, mod_id in enumerate(ids_modulos)}


# =============================================================================
#  BLOCO 2 — CONSTRUÇÃO DO GRAFO: MATRIZ E LISTA DE ADJACÊNCIA
# =============================================================================

def construir_grafo():
    # matriz n x n inicializada com zeros (0 = sem ligação)
    matriz_adj = [[0] * n for _ in range(n)]

    # dicionário de listas de (vizinho, peso)
    lista_adj = {mod_id: [] for mod_id in ids_modulos}

    for (a, b, dist) in arestas:
        ia, ib = indice[a], indice[b]

        # preenche a matriz de forma simétrica (grafo não direcionado)
        matriz_adj[ia][ib] = dist
        matriz_adj[ib][ia] = dist

        # preenche a lista de adjacência nos dois sentidos
        lista_adj[a].append((b, dist))
        lista_adj[b].append((a, dist))

    return matriz_adj, lista_adj


# =============================================================================
#  BLOCO 3 — ALGORITMOS DE REDE
# =============================================================================

def bfs(lista_adj, origem):
    # busca em largura usando fila (deque) — visita módulos por nível de distância
    visitados = {origem}
    fila      = deque([(origem, 0)])
    ordem     = []

    while fila:
        atual, nivel = fila.popleft()
        ordem.append((atual, nivel))

        for (vizinho, _peso) in sorted(lista_adj[atual], key=lambda x: x[0]):
            if vizinho not in visitados:
                visitados.add(vizinho)
                fila.append((vizinho, nivel + 1))

    return ordem


def dfs(lista_adj, origem):
    # busca em profundidade iterativa usando pilha
    visitados = set()
    pilha     = [origem]
    ordem     = []

    while pilha:
        atual = pilha.pop()
        if atual not in visitados:
            visitados.add(atual)
            ordem.append(atual)

            for (vizinho, _) in sorted(lista_adj[atual], key=lambda x: x[0], reverse=True):
                if vizinho not in visitados:
                    pilha.append(vizinho)

    return ordem


def detectar_pontes(lista_adj):
    # algoritmo de Tarjan para encontrar pontes (conexões críticas) do grafo
    # uma ponte é uma aresta cuja remoção desconecta parte da rede
    visitado = {}
    disc     = {}
    low      = {}
    pai      = {}
    pontes   = []
    timer    = [0]

    def _dfs(u):
        visitado[u] = True
        disc[u]     = low[u] = timer[0]
        timer[0]   += 1

        for (v, _) in lista_adj[u]:
            if not visitado.get(v, False):
                pai[v] = u
                _dfs(v)
                low[u] = min(low[u], low[v])
                # se low[v] > disc[u], não há caminho alternativo: é uma ponte
                if low[v] > disc[u]:
                    pontes.append((u, v))
            elif v != pai.get(u):
                low[u] = min(low[u], disc[v])

    for mod in ids_modulos:
        if not visitado.get(mod, False):
            pai[mod] = None
            _dfs(mod)

    return pontes


def dijkstra(lista_adj, origem):
    # algoritmo de Dijkstra com seleção linear (O(V^2)) — adequado para V=8
    INF   = float('inf')
    dist  = {mod: INF  for mod in ids_modulos}
    prev  = {mod: None for mod in ids_modulos}
    dist[origem]  = 0
    nao_visitados = set(ids_modulos)

    while nao_visitados:
        # seleciona o vértice não visitado com menor distância acumulada
        u = min(nao_visitados, key=lambda v: dist[v])
        if dist[u] == INF:
            break
        nao_visitados.remove(u)

        for (v, peso) in lista_adj[u]:
            if v in nao_visitados:
                nova = dist[u] + peso
                if nova < dist[v]:   # relaxamento da aresta
                    dist[v] = nova
                    prev[v] = u

    return dist, prev


def reconstruir_caminho(prev, destino):
    # reconstrói o caminho a partir do dicionário prev do Dijkstra
    caminho = []
    atual   = destino
    while atual is not None:
        caminho.append(atual)
        atual = prev[atual]
    caminho.reverse()
    return caminho


# =============================================================================
#  BLOCO 4 — MODELAGEM MATEMÁTICA E OTIMIZAÇÃO
#
#  Fenômeno modelado: crescimento exponencial do consumo energético da colônia
#
#  Fórmula:  C(t) = C0 * e^(alpha * t)
#
#  Variáveis:
#    C(t)  = consumo total da colônia no mês t (kW)
#    C0    = consumo inicial (soma dos módulos ativos no início da missão)
#    alpha = taxa de crescimento mensal (alpha = 0.05 -> 5% ao mês)
#    t     = tempo em meses desde a ativação da Aurora Siger
#
#  Análise qualitativa:
#    A derivada dC/dt = C0 * alpha * e^(alpha*t) é sempre positiva para alpha > 0,
#    ou seja, o consumo cresce de forma acelerada com o tempo.
#    A função é convexa para cima: a taxa de crescimento aumenta a cada mês.
#    Ponto crítico: quando C(t) atinge a capacidade máxima de geração,
#    a colônia entra em déficit energético. Esse ponto é calculado por:
#      t_critico = ln(Geracao_maxima / C0) / alpha
#
#  Relação com a Aurora Siger:
#    Com alpha = 0.05, o consumo dobra em t = ln(2)/0.05 ~= 14 meses.
#    Isso significa que novos painéis solares devem ser instalados antes
#    do mês 14 para evitar apagões na colônia.
# =============================================================================

def modelagem_consumo(modulos, alpha=0.05):
    C0 = sum(m["consumo_kw"] for m in modulos.values() if m["status"] == "ATIVO")

    previsoes = []
    for t in range(25):
        ct = C0 * math.exp(alpha * t)
        previsoes.append((t, round(ct, 2)))

    return C0, alpha, previsoes


def calcular_eficiencia(dist_dijkstra, origem, modulos):
    # eficiência de distribuição: eta = 1 - (perda_total / demanda_total)
    # fator de perda: 0.001 kW por metro de cabo (1 W/m)
    fator_perda   = 0.001

    demanda_total = sum(
        m["consumo_kw"]
        for k, m in modulos.items()
        if m["status"] == "ATIVO" and k != origem
    )
    perda_total   = sum(
        dist_dijkstra[dest] * fator_perda
        for dest in ids_modulos
        if dist_dijkstra[dest] != float('inf') and dest != origem
    )

    if demanda_total == 0:
        return 0.0, 0.0, 0.0

    eta = max(0.0, 1.0 - perda_total / demanda_total)
    return round(eta * 100, 2), round(perda_total, 2), round(demanda_total, 2)


# =============================================================================
#  BLOCO 5 — SUSTENTABILIDADE E GOVERNANÇA (ESG)
# =============================================================================

def relatorio_esg(lista_adj, modulos):
    consumo_total       = sum(m["consumo_kw"] for m in modulos.values() if m["status"] == "ATIVO")
    armazenamento_total = sum(m["armazenamento_kw"] for m in modulos.values())
    autonomia           = armazenamento_total / consumo_total if consumo_total > 0 else 0

    criticos    = sorted(
        [(k, v) for k, v in modulos.items() if v["prioridade"] >= 4],
        key=lambda x: -x[1]["prioridade"]
    )
    pontes      = detectar_pontes(lista_adj)
    baixa_prior = [(k, v) for k, v in modulos.items() if v["prioridade"] <= 2]
    economia    = sum(v["consumo_kw"] * 0.30 for _, v in baixa_prior)
    densidade   = len(arestas) / (n * (n - 1) // 2)
    _, alpha, _ = modelagem_consumo(modulos)
    t_duplo     = math.log(2) / alpha

    print("\n" + "=" * 60)
    print("  RELATÓRIO ESG — SUSTENTABILIDADE E GOVERNANÇA")
    print("=" * 60)

    print("\n  [1] USO SUSTENTÁVEL DE ENERGIA")
    print(f"  Consumo total         : {consumo_total:.1f} kW")
    print(f"  Armazenamento total   : {armazenamento_total:.1f} kWh")
    print(f"  Autonomia estimada    : {autonomia:.1f} horas")
    print(f"  Consumo dobra em      : aproximadamente {t_duplo:.0f} meses (alpha={alpha})")
    print(f"  Meta de geração       : >= {consumo_total * 1.2:.1f} kW (margem de 20%)")
    print(f"  -> Ampliar painéis solares antes do mês {t_duplo:.0f}.")

    print("\n  [2] PRIORIZAÇÃO DE SISTEMAS CRÍTICOS")
    for (k, v) in criticos:
        print(f"  Prioridade {v['prioridade']}/5 - {v['nome']} ({k}) - {v['status']}")
    print(f"  -> Esses módulos recebem energia primeiro em qualquer emergência.")

    print("\n  [3] CONEXÕES CRÍTICAS DA REDE (PONTES)")
    if pontes:
        for (a, b) in pontes:
            print(f"  ATENÇÃO: {modulos[a]['nome']} ({a}) <-> {modulos[b]['nome']} ({b})")
        print(f"  -> Instalar conexões redundantes nesses {len(pontes)} pontos.")
    else:
        print(f"  Nenhuma ponte detectada. A rede possui redundância adequada.")

    print("\n  [4] EXPANSÃO ORGANIZADA DA COLÔNIA")
    print(f"  Módulos atuais        : {len(modulos)}")
    print(f"  Conexões da rede      : {len(arestas)}")
    print(f"  Densidade da rede     : {densidade:.1%} das conexões possíveis")
    print(f"  -> Adicionar módulos de geração antes de ampliar os de consumo.")

    print("\n  [5] GOVERNANÇA TECNOLÓGICA")
    score = max(0, 100 - len(pontes) * 12)
    print(f"  Score de resiliência  : {score}/100")
    print(f"  Pontos de falha       : {len(pontes)}")
    print(f"  -> Decisões críticas passam obrigatoriamente pelo CTR.")
    print(f"  -> Dijkstra garante rotas otimizadas a cada ciclo de análise.")

    print("\n  [6] REDUÇÃO DE DESPERDÍCIOS")
    print(f"  Módulos baixa prioridade : {[v['nome'] for _, v in baixa_prior]}")
    print(f"  Economia com corte 30%   : {economia:.1f} kW")
    print(f"  Representa               : {economia / consumo_total * 100:.1f}% do consumo total")
    print(f"  -> Em emergência, desligar AGR e LAB libera {economia:.1f} kW imediatos.")

    limpar()


# =============================================================================
#  BLOCO 6 — SIMULAÇÕES OPERACIONAIS
# =============================================================================

def simular_rota_energia(lista_adj, modulos):
    # simula o envio de energia do módulo ENE para um destino via Dijkstra
    print("\n" + "-" * 60)
    print("  SIMULAÇÃO: ROTA DE ENVIO DE ENERGIA (Dijkstra)")
    print("-" * 60)
    print("\n  Módulos de destino disponíveis:")
    for k, v in modulos.items():
        if k != "ENE":
            print(f"  [{k}] {v['nome']}  |  Status: {v['status']}")

    destino = input("\n  Módulo de destino (sigla): ").strip().upper()
    if destino not in modulos or destino == "ENE":
        print("  Módulo inválido.")
        return

    dist, prev = dijkstra(lista_adj, "ENE")

    if dist[destino] == float('inf'):
        print(f"  Sem rota disponível para {modulos[destino]['nome']}.")
        return

    caminho = reconstruir_caminho(prev, destino)
    perda   = dist[destino] * 0.001

    print(f"\n  Rota mais eficiente (Dijkstra):")
    print(f"  {' -> '.join(caminho)}")
    print(f"\n  Distância total    : {dist[destino]} metros")
    print(f"  Perda estimada     : {perda:.2f} kW  (1 W/m de cabo)")
    print(f"  Demanda do destino : {modulos[destino]['consumo_kw']:.1f} kW")
    print(f"  Energia entregue   : {modulos[destino]['consumo_kw'] - perda:.2f} kW")

    eta, _, _ = calcular_eficiencia(dist, "ENE", modulos)
    print(f"\n  Eficiência de distribuição da rede (a partir de ENE): {eta:.2f}%")

    limpar()


def simular_falha_modulo(lista_adj, modulos):
    # simula a falha de um módulo e verifica o impacto na conectividade da rede
    print("\n" + "-" * 60)
    print("  SIMULAÇÃO: FALHA DE MÓDULO")
    print("-" * 60)
    print("\n  Módulos disponíveis:")
    for k, v in modulos.items():
        print(f"  [{k}] {v['nome']}  |  Prioridade: {v['prioridade']}/5  |  Status: {v['status']}")

    mod_falha = input("\n  Módulo com falha (sigla): ").strip().upper()
    if mod_falha not in modulos:
        print("  Módulo inválido.")
        return

    print(f"\n  Simulando falha: {modulos[mod_falha]['nome']} ({mod_falha})")
    print(f"  Consumo retirado  : {modulos[mod_falha]['consumo_kw']:.1f} kW")
    print(f"  Prioridade        : {modulos[mod_falha]['prioridade']}/5")

    # reconstrói lista de adjacência sem o módulo com falha
    lista_sem = {
        mod: [(v, p) for (v, p) in viz if v != mod_falha]
        for mod, viz in lista_adj.items()
        if mod != mod_falha
    }

    # verifica conectividade com BFS a partir do primeiro módulo restante
    restantes = [m for m in ids_modulos if m != mod_falha]
    if not restantes:
        return

    resultado_bfs = bfs(lista_sem, restantes[0])
    visitados     = {m for (m, _) in resultado_bfs}
    isolados      = [m for m in restantes if m not in visitados]

    print(f"\n  Verificando conectividade após a falha...")

    if isolados:
        print(f"\n  ALERTA: {len(isolados)} módulo(s) isolado(s):")
        for iso in isolados:
            print(f"  -> {modulos[iso]['nome']} ({iso})  |  Prioridade: {modulos[iso]['prioridade']}/5")
        criticos_isolados = [m for m in isolados if modulos[m]["prioridade"] >= 4]
        if criticos_isolados:
            print(f"\n  EMERGÊNCIA: módulos críticos sem conexão! Protocolo de rota alternativa.")
    else:
        print(f"  Rede permanece conectada. {len(restantes)} módulos em operação.")

    if modulos[mod_falha]["prioridade"] >= 4:
        print(f"\n  MÓDULO CRÍTICO EM FALHA! Acionar protocolo de emergência imediatamente.")
    else:
        print(f"\n  Módulo não crítico. Operação reduzida sem risco imediato.")

    limpar()


# =============================================================================
#  BLOCO 7 — FUNÇÕES DE EXIBIÇÃO
# =============================================================================

def exibir_painel(modulos):
    # painel geral com o estado atual de todos os módulos da colônia
    print("\n" + "=" * 60)
    print("  AURORA SIGER — PAINEL DE CONTROLE DA COLÔNIA")
    print("=" * 60)

    consumo_total = sum(m["consumo_kw"] for m in modulos.values() if m["status"] == "ATIVO")
    carga_ene     = modulos["ENE"].get("carga_pct", 0.0)
    energia_disp  = modulos["ENE"]["armazenamento_kw"] * (carga_ene / 100)

    print(f"\n  [ENERGIA]")
    print(f"  Carga das baterias    : {carga_ene:.1f}%")
    print(f"  Energia disponível    : {energia_disp:.1f} kWh")
    print(f"  Consumo total ativo   : {consumo_total:.1f} kW")

    if carga_ene < 30.0 and consumo_total > energia_disp:
        print(f"\n  [ALERTA CRÍTICO] Baterias críticas e consumo elevado.")
    elif carga_ene < 50.0:
        print(f"\n  [AVISO] Baterias abaixo de 50%. Priorizar recarga.")
    else:
        print(f"\n  [OK] Balanço energético estável.")

    print(f"\n  [MÓDULOS OPERACIONAIS]")
    print(f"  {'Nome':<28} {'Consumo':>8}  {'Prior.':>6}  Status")
    print(f"  {'-'*28} {'-'*8}  {'-'*6}  ------")
    for k, m in modulos.items():
        consumo_str = f"{m['consumo_kw']:.1f} kW" if m["status"] != "MANUTENÇÃO" else "  ---  "
        print(f"  {m['nome']:<28} {consumo_str:>8}  {m['prioridade']:>6}  {m['status']}")

    limpar()


def exibir_rede(matriz_adj, modulos):
    print("\n" + "=" * 60)
    print("  REDE DA COLÔNIA — AURORA SIGER")
    print("=" * 60)

    print(f"\n  Módulos (vértices) : {n}")
    print(f"  Conexões (arestas) : {len(arestas)}")

    print("""
  Diagrama de adjacencia da rede (distancias em metros):

  [HAB] ---30m--- [OXI] ---35m--- [ENE] ---90m--- [AGR]
    |               |               |                |
   50m             40m             45m              65m
    |               |               |                |
  [MED] ----------[MED]          [MED]            [LAB]
    |
   80m--- [CTR] ---40m--- [ENE]
            |               |
           60m             55m--- [HAB]
            |
          [COM]
            |
           70m--- [LAB]

  Resumo das conexoes diretas por modulo:
  HAB : OXI(30)  MED(50)  ENE(55)  CTR(80)  COM(75)
  OXI : HAB(30)  ENE(35)  MED(40)
  ENE : OXI(35)  CTR(40)  MED(45)  HAB(55)  AGR(90)
  MED : OXI(40)  ENE(45)  HAB(50)
  CTR : ENE(40)  COM(60)  LAB(70)  HAB(80)
  AGR : ENE(90)  LAB(65)
  LAB : AGR(65)  CTR(70)
  COM : CTR(60)  HAB(75)
""")

    print("  CONEXÕES:")
    print(f"  {'Módulo A':<28} {'Módulo B':<28} {'Dist.':>6}")
    print(f"  {'-'*28} {'-'*28} {'-'*6}")
    for (a, b, dist) in sorted(arestas, key=lambda x: x[2]):
        print(f"  {modulos[a]['nome']:<28} {modulos[b]['nome']:<28} {dist:>4} m")

    print("\n  MATRIZ DE ADJACÊNCIA (distâncias em metros; 0 = sem ligação):")
    print()
    header = "       " + "".join(f"{mid:>5}" for mid in ids_modulos)
    print(f"  {header}")
    for i, mid in enumerate(ids_modulos):
        linha = f"  {mid:>5} " + "".join(f"{matriz_adj[i][j]:>5}" for j in range(n))
        print(linha)

    limpar()


def consultar_modulo(lista_adj, modulos):
    print("\n  Módulos disponíveis:")
    for k, v in modulos.items():
        print(f"  [{k}] {v['nome']}  |  Status: {v['status']}")

    escolha = input("\n  Selecione o módulo (sigla): ").strip().upper()
    if escolha not in modulos:
        print("  Módulo não encontrado.")
        return

    m = modulos[escolha]
    print("\n" + "-" * 60)
    print(f"  MÓDULO: {m['nome']} ({escolha})")
    print("-" * 60)
    print(f"  Descrição             : {m['descricao']}")
    print(f"  Consumo energético    : {m['consumo_kw']:.1f} kW")
    print(f"  Prioridade operacional: {m['prioridade']}/5")
    print(f"  Armazenamento         : {m['armazenamento_kw']:.1f} kWh")
    if "carga_pct" in m:
        print(f"  Carga atual           : {m['carga_pct']:.1f}%")
    print(f"  Freq. de comunicação  : {m['freq_comunicacao']}")
    print(f"  Status                : {m['status']}")

    print(f"\n  Conexões diretas:")
    for (v, d) in sorted(lista_adj[escolha], key=lambda x: x[1]):
        print(f"  -> {modulos[v]['nome']:<28} ({v})  {d} m")

    limpar()


def executar_bfs(lista_adj, modulos):
    print("\n" + "-" * 60)
    print("  BFS — BUSCA EM LARGURA")
    print("-" * 60)
    print("\n  Módulos disponíveis como origem:")
    for k, v in modulos.items():
        print(f"  [{k}] {v['nome']}")

    origem = input("\n  Módulo de origem: ").strip().upper()
    if origem not in modulos:
        print("  Módulo inválido.")
        return

    resultado = bfs(lista_adj, origem)

    print(f"\n  BFS a partir de: {modulos[origem]['nome']} ({origem})")
    print(f"\n  {'Ordem':<6} {'Nível':<7} {'ID':<6} {'Nome'}")
    print(f"  {'-'*6} {'-'*7} {'-'*6} {'-'*28}")
    for i, (mod, nivel) in enumerate(resultado, 1):
        print(f"  {i:<6} {nivel:<7} {mod:<6} {modulos[mod]['nome']}")

    print(f"\n  Módulos alcançados : {len(resultado)}/{n}")
    print(f"  Grafo              : {'CONECTADO' if len(resultado) == n else 'DESCONECTADO'}")

    limpar()


def executar_dfs(lista_adj, modulos):
    print("\n" + "-" * 60)
    print("  DFS — BUSCA EM PROFUNDIDADE + CONEXÕES CRÍTICAS")
    print("-" * 60)
    print("\n  Módulos disponíveis como origem:")
    for k, v in modulos.items():
        print(f"  [{k}] {v['nome']}")

    origem = input("\n  Módulo de origem: ").strip().upper()
    if origem not in modulos:
        print("  Módulo inválido.")
        return

    ordem = dfs(lista_adj, origem)

    print(f"\n  DFS a partir de: {modulos[origem]['nome']} ({origem})")
    print(f"\n  {'Passo':<7} {'ID':<6} {'Nome'}")
    print(f"  {'-'*7} {'-'*6} {'-'*28}")
    for i, mod in enumerate(ordem, 1):
        print(f"  {i:<7} {mod:<6} {modulos[mod]['nome']}")

    print(f"\n  Detectando conexões críticas (pontes)...")
    pontes = detectar_pontes(lista_adj)
    if pontes:
        print(f"\n  Pontes encontradas ({len(pontes)}):")
        for (a, b) in pontes:
            print(f"  {modulos[a]['nome']} ({a}) <-> {modulos[b]['nome']} ({b})")
        print(f"\n  -> Recomendado instalar conexões redundantes nesses trechos.")
    else:
        print(f"  Nenhuma ponte detectada. Rede com redundância adequada.")

    limpar()


def executar_dijkstra(lista_adj, modulos):
    print("\n" + "-" * 60)
    print("  DIJKSTRA — CAMINHOS MÍNIMOS")
    print("-" * 60)
    print("\n  Módulos disponíveis como origem:")
    for k, v in modulos.items():
        print(f"  [{k}] {v['nome']}")

    origem = input("\n  Módulo de origem: ").strip().upper()
    if origem not in modulos:
        print("  Módulo inválido.")
        return

    dist, prev = dijkstra(lista_adj, origem)

    print(f"\n  Distâncias mínimas a partir de: {modulos[origem]['nome']} ({origem})")
    print(f"\n  {'Dest.':<6} {'Nome':<28} {'Dist.':>8}  Caminho")
    print(f"  {'-'*6} {'-'*28} {'-'*8}  {'-'*30}")
    for dest in ids_modulos:
        if dest == origem:
            continue
        d       = dist[dest]
        caminho = reconstruir_caminho(prev, dest)
        d_str   = f"{d} m" if d != float('inf') else "inacessível"
        print(f"  {dest:<6} {modulos[dest]['nome']:<28} {d_str:>8}  {' -> '.join(caminho)}")

    eta, perda, demanda = calcular_eficiencia(dist, origem, modulos)
    print(f"\n  Eficiência de distribuição : {eta:.2f}%")
    print(f"  Perda total estimada       : {perda:.2f} kW")
    print(f"  Demanda total dos destinos : {demanda:.2f} kW")

    limpar()


def exibir_modelagem(modulos):
    C0, alpha, previsoes = modelagem_consumo(modulos)
    t_duplo = math.log(2) / alpha
    geracao_instalada = C0 * 1.5
    t_limite = math.log(geracao_instalada / C0) / alpha

    print("\n" + "=" * 60)
    print("  MODELAGEM MATEMÁTICA — CONSUMO ENERGÉTICO")
    print("=" * 60)

    print(f"\n  Fórmula: C(t) = C0 * e^(alpha * t)")
    print(f"\n  C0    = {C0:.2f} kW  (consumo inicial dos módulos ativos)")
    print(f"  alpha = {alpha}    (taxa de crescimento: {alpha*100:.0f}% ao mês)")
    print(f"\n  Derivada: dC/dt = {C0:.2f} * {alpha} * e^({alpha}*t)")
    print(f"  Sempre positiva para alpha > 0: crescimento acelerado.")
    print(f"\n  O consumo dobra em t = ln(2)/{alpha} = {t_duplo:.1f} meses.")
    print(f"  Geração instalada estimada : {geracao_instalada:.1f} kW (150% do consumo inicial)")
    print(f"  Capacidade esgotada em     : t ~= {t_limite:.1f} meses")
    print(f"  -> Instalar nova capacidade de geração antes do mês {math.ceil(t_limite)}.")

    print(f"\n  {'Mês':>5}  {'C(t) kW':>12}  Variação")
    print(f"  {'-'*5}  {'-'*12}  {'-'*12}")
    for i, (t, ct) in enumerate(previsoes[:13]):
        var = f"+{ct - previsoes[i-1][1]:.2f} kW" if i > 0 else "   ---"
        obs = ""
        if t == 0:
            obs = "<- ativação"
        elif t == int(round(t_duplo)):
            obs = "<- consumo dobra!"
        print(f"  {t:>5}  {ct:>10.2f} kW  {var:<14}  {obs}")

    limpar()


# =============================================================================
#  BLOCO 8 — MENU PRINCIPAL
# =============================================================================

def menu():
    # gera os dados operacionais dos módulos a cada execução
    modulos = gerar_modulos()
    matriz_adj, lista_adj = construir_grafo()

    while True:
        print("\n" + "=" * 60)
        print("  SIGIC — SISTEMA INTELIGENTE DE GERENCIAMENTO DA")
        print("          INFRAESTRUTURA DA COLÔNIA")
        print("  Aurora Siger  |  FIAP  |  Ciência da Computação  |  Fase 4")
        print("=" * 60)
        print()
        print("  [1] Painel geral da colônia")
        print("  [2] Visualizar rede")
        print("  [3] Consultar módulo")
        print("  [4] BFS — Busca em Largura")
        print("  [5] DFS — Busca em Profundidade")
        print("  [6] Dijkstra — Caminho Mínimo")
        print("  [7] Modelagem Matemática — Consumo Energético")
        print("  [8] Simulação: Rota de Envio de Energia")
        print("  [9] Simulação: Falha de Módulo")
        print("  [0] Relatório ESG — Sustentabilidade e Governança")
        print("  [S] Sair")
        print()

        opcao = input("  Selecione uma opção: ").strip()

        if opcao == "1":
            exibir_painel(modulos)
        elif opcao == "2":
            exibir_rede(matriz_adj, modulos)
        elif opcao == "3":
            consultar_modulo(lista_adj, modulos)
        elif opcao == "4":
            executar_bfs(lista_adj, modulos)
        elif opcao == "5":
            executar_dfs(lista_adj, modulos)
        elif opcao == "6":
            executar_dijkstra(lista_adj, modulos)
        elif opcao == "7":
            exibir_modelagem(modulos)
        elif opcao == "8":
            simular_rota_energia(lista_adj, modulos)
        elif opcao == "9":
            simular_falha_modulo(lista_adj, modulos)
        elif opcao == "0":
            relatorio_esg(lista_adj, modulos)
        elif opcao.upper() == "S":
            print("\n  Encerrando SIGIC. Aurora Siger — missão em andamento.")
            print()
            break
        else:
            print("  Opção inválida. Tente novamente.")


if __name__ == "__main__":
    menu()
