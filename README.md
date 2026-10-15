# Sistema de Gestão de Peças, Qualidade e Armazenamento

Trabalho da disciplina **Algoritmos e Lógica de Programação** — UniFECAF.

Protótipo em Python que simula a inspeção automática de qualidade de peças
em uma linha de montagem industrial, substituindo a conferência manual por
uma lógica automatizada de aprovação/reprovação, armazenamento em caixas e
geração de relatórios.

## Funcionamento

O sistema funciona por um **menu interativo em terminal** com 6 opções,
que ficam em loop até o usuário escolher sair. Todos os dados são mantidos
em memória durante a execução (listas e dicionários Python), sem banco de
dados externo.

### 1. Cadastrar nova peça

Pede o `id`, `peso` (g), `cor` e `comprimento` (cm) da peça e avalia
automaticamente se ela é **aprovada** ou **reprovada**, segundo os critérios:

| Critério     | Faixa aceita           |
|--------------|-------------------------|
| Peso         | entre 95g e 105g         |
| Cor          | azul ou verde            |
| Comprimento  | entre 10cm e 20cm        |

A peça só é aprovada se **todos** os três critérios forem atendidos. Se
algum critério falhar, a peça é reprovada e o sistema registra o(s)
motivo(s) da reprovação (uma peça pode falhar em mais de um critério ao
mesmo tempo).

IDs duplicados são bloqueados: se você tentar cadastrar um `id` já usado
por outra peça, o cadastro é cancelado com um aviso.

Peças aprovadas são automaticamente colocadas na **caixa em aberto**. Cada
caixa comporta até **10 peças**; ao atingir esse limite, a caixa é fechada
e uma nova caixa vazia é iniciada para as próximas peças aprovadas.

### 2. Listar peças aprovadas/reprovadas

Permite listar apenas as aprovadas, apenas as reprovadas, ou ambas. Peças
reprovadas mostram o(s) motivo(s) da reprovação; peças aprovadas mostram
em qual caixa foram armazenadas.

### 3. Remover peça cadastrada

Remove uma peça pelo `id`. Regra de negócio adotada: peças que já estão em
uma **caixa fechada** não podem ser removidas (a caixa já foi lacrada,
como aconteceria em um processo real de expedição). Peças reprovadas ou
peças aprovadas que ainda estão na caixa em aberto podem ser removidas
normalmente.

### 4. Listar caixas fechadas

Mostra cada caixa já fechada, com a quantidade e os IDs das peças que ela
contém, além do status da caixa atualmente em aberto (quantas peças ela já
tem e quantas faltam para fechar).

### 5. Gerar relatório final

Mostra um resumo consolidado:
- Total de peças aprovadas
- Total de peças reprovadas, com a contagem de ocorrências por motivo
- Quantidade de caixas fechadas
- Status da caixa em aberto
- Total de caixas utilizadas (fechadas + a caixa em aberto, se houver peças nela)

### 6. Sair

Encerra o programa.

## Como rodar o programa

Pré-requisito: **Python 3.8+** instalado (não usa nenhuma biblioteca externa).

1. Baixe/clone este repositório.
2. Abra um terminal na pasta do projeto.
3. Execute:

```bash
python3 sistema_pecas.py
```

4. Use os números do menu para navegar entre as opções.

## Exemplo de entrada e saída

**Cadastrando uma peça aprovada:**

```
Escolha uma opção: 1

--- Cadastro de Nova Peça ---
ID da peça: p1
Peso (g): 100
Cor: azul
Comprimento (cm): 15
  -> Peça 'p1' APROVADA e armazenada.
```

**Cadastrando uma peça reprovada (peso fora do padrão):**

```
Escolha uma opção: 1

--- Cadastro de Nova Peça ---
ID da peça: p2
Peso (g): 130
Cor: verde
Comprimento (cm): 12
  -> Peça 'p2' REPROVADA. Motivo(s): Peso fora do padrão (130.0g; esperado entre 95.0g e 105.0g)
```

**Relatório final, após cadastrar 12 peças (10 aprovadas na caixa 1, 1 aprovada na caixa 2, 2 reprovadas):**

```
Escolha uma opção: 5

=========== RELATÓRIO FINAL ===========
Total de peças aprovadas : 11
Total de peças reprovadas: 2

Motivos de reprovação:
  - Peso fora do padrão (130.0g; esperado entre 95.0g e 105.0g): 1 ocorrência(s)
  - Cor não aceita ('amarela'; esperado azul ou verde): 1 ocorrência(s)

Caixas fechadas         : 1
Caixa em aberto          : 1 (1/10 peças)
Total de caixas utilizadas: 2
========================================
```

## Estrutura do código

- `avaliar_peca()` — regra de negócio que decide aprovação/reprovação.
- `cadastrar_peca()` / `armazenar_em_caixa()` — cadastro e lógica de
  enchimento/fechamento de caixas.
- `listar_pecas()`, `remover_peca()`, `listar_caixas_fechadas()`,
  `gerar_relatorio()` — demais opções do menu.
- `main()` — laço principal do menu interativo.

Todo o estado do sistema (peças aprovadas, reprovadas, caixa em aberto e
caixas fechadas) é mantido em um único dicionário `estado`, passado por
referência entre as funções — o que evita variáveis globais e deixa
explícito quais dados cada função manipula.
