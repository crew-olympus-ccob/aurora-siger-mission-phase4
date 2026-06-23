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

Cada execução gera um cenário diferente com base em valores aleatórios dos sensores.

---

## Exemplo de uso (valores variam a cada execução)

**Dijkstra — rota de envio de energia de ENE para LAB:**

Entrada (módulo de origem selecionado pelo operador):
```
Módulo de origem: ENE
```

Saída do sistema:
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

Entrada (módulo com falha selecionado pelo operador):
```
Módulo com falha: CTR
```

Saída do sistema:
```
  Simulando falha: Centro de Controle (CTR)
  Consumo retirado  : 15.0 kW
  Prioridade        : 4/5

  Verificando conectividade após a falha...
  Rede permanece conectada. 7 modulos em operacao.

  MODULO CRITICO EM FALHA! Acionar protocolo de emergencia imediatamente.
```

---

## Modelagem matemática

| Variável | Significado |
|---|---|
| C(t) | consumo total da colônia no mês t (kW) |
| C0 | consumo inicial dos módulos ativos (kW) |
| alpha | taxa de crescimento mensal (0.05 = 5% ao mês) |
| t | tempo em meses desde a ativação da colônia |

```
C(t) = C0 * e^(alpha * t)
```

Com alpha = 0.05, o consumo dobra em aproximadamente 14 meses — definindo o prazo máximo para expansão da capacidade de geração de energia.

---

## Estrutura do código

```
codigo_fonte.py
├── Bloco 1 — Estruturas de dados da infraestrutura
├── Bloco 2 — Construção do grafo (matriz e lista de adjacência)
├── Bloco 3 — Algoritmos de rede (BFS, DFS, Dijkstra, detecção de pontes)
├── Bloco 4 — Modelagem matemática e otimização
├── Bloco 5 — Sustentabilidade e governança (ESG)
├── Bloco 6 — Simulações operacionais
├── Bloco 7 — Funções de exibição
└── Bloco 8 — Menu principal
```
