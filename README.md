# Aurora Siger — SIGIC: Sistema Inteligente de Gerenciamento da Infraestrutura da Colônia (Fase 4)

**FIAP | Ciência da Computação | Grupo:** Gabriel, Lucas, Matheus, Miguel e Pedro

---

## Descrição

Sistema computacional desenvolvido para representar e otimizar a infraestrutura da colônia Aurora Siger em Marte. A rede da base é modelada como um grafo, onde cada módulo é um vértice e cada conexão física é uma aresta com peso. O sistema permite visualizar a rede, consultar módulos, calcular rotas otimizadas e simular situações operacionais diretamente pelo terminal.

---

## Funcionalidades

| Bloco | Função |
|---|---|
| Estruturas de dados | Dicionário de módulos, lista de tuplas (arestas), matriz e lista de adjacência |
| BFS | Busca em largura a partir de qualquer módulo, com nível de cada vértice |
| DFS | Busca em profundidade iterativa + detecção de pontes (conexões críticas) |
| Dijkstra | Cálculo de caminhos mínimos e eficiência de distribuição de energia |
| Modelagem matemática | Crescimento exponencial do consumo: C(t) = C0 * e^(alpha * t) |
| Simulações | Rota de envio de energia, falha de módulo e impacto na conectividade |
| ESG | Relatório de sustentabilidade, resiliência da rede e governança |

---

## Como executar

Requer apenas **Python 3** — sem dependências externas.

```bash
python codigo_fonte.py
```

---

## Módulos da colônia

| ID | Nome | Consumo (kW) | Prioridade |
|---|---|---|---|
| HAB | Habitação | 18.5 | 4/5 |
| MED | Suporte Médico | 12.0 | 5/5 |
| OXI | Produção de Oxigênio | 22.0 | 5/5 |
| CTR | Centro de Controle | 15.0 | 4/5 |
| ENE | Armazenamento de Energia | 5.0 | 5/5 |
| AGR | Agricultura | 20.0 | 2/5 |
| LAB | Laboratório Científico | 14.0 | 2/5 |
| COM | Comunicação | 10.0 | 3/5 |

Módulos com **prioridade ≥ 4** (MED, OXI, ENE, HAB, CTR) são considerados críticos e recebem energia prioritária em qualquer emergência.

### Descrição dos módulos

| ID | Descrição |
|---|---|
| HAB | Onde a tripulação mora e descansa. Parte essencial da sobrevivência da colônia. |
| MED | Cuida da saúde da tripulação. Atende doenças e ferimentos. |
| OXI | Gera o ar que todos respiram. Sem ele, não há vida na base. |
| ENE | Armazena e distribui energia para toda a colônia. Mantém tudo funcionando. |
| CTR | Monitora e controla todos os sistemas. Funciona como o cérebro da colônia. |
| COM | Liga os módulos entre si e com a Terra. Mantém a comunicação geral. |
| AGR | Produz alimentos para a tripulação. Garante a alimentação da colônia. |
| LAB | Realiza pesquisas e testes. Contribui para o desenvolvimento da missão. |

---

## Exemplo de uso

**Dijkstra — rota de envio de energia de ENE para LAB:**

```
Distancias minimas a partir de: Armazenamento de Energia (ENE)

  Dest.  Nome                         Dist.    Caminho
  ------ ---------------------------- -------- ----------------------------
  HAB    Habitacao                      55 m   ENE -> HAB
  MED    Suporte Medico                 45 m   ENE -> MED
  OXI    Producao de Oxigenio           35 m   ENE -> OXI
  CTR    Centro de Controle             40 m   ENE -> CTR
  AGR    Agricultura                    90 m   ENE -> AGR
  LAB    Laboratorio Cientifico        110 m   ENE -> CTR -> LAB
  COM    Comunicacao                   100 m   ENE -> CTR -> COM

  Eficiencia de distribuicao : 99.57%
```

**Simulação de falha do módulo CTR:**

```
  Simulando falha: Centro de Controle (CTR)
  Consumo retirado  : 15.0 kW
  Prioridade        : 4/5

  Verificando conectividade após a falha...
  Rede permanece conectada. 7 módulos em operação.

  MÓDULO CRÍTICO EM FALHA! Acionar protocolo de emergência imediatamente.
```

---

## Modelagem matemática

O crescimento do consumo energético da colônia é modelado por uma função exponencial:

```
C(t) = C0 * e^(alpha * t)

C0    = consumo inicial dos módulos ativos (kW)
alpha = taxa de crescimento mensal (0.05 = 5% ao mês)
t     = tempo em meses desde a ativação da colônia
```

Com alpha = 0.05, o consumo dobra em aproximadamente 14 meses — definindo o prazo máximo para expansão da capacidade de geração de energia.

---

## Estrutura do código

```
codigo_fonte.py
├── Bloco 1 — Estruturas de dados da i