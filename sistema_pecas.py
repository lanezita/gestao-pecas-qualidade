"""
Sistema de Gestão de Peças, Qualidade e Armazenamento
=======================================================

Trabalho da disciplina Algoritmos e Lógica de Programação (UniFECAF).

Simula, em Python, a inspeção automática de qualidade de peças em uma linha
de montagem industrial: cadastro de peças, avaliação de aprovação/reprovação
segundo critérios de qualidade, armazenamento das peças aprovadas em caixas
de capacidade limitada e geração de relatórios consolidados.

Autor: Elaine Fernandes
"""

# ---------------------------------------------------------------------------
# CONSTANTES (critérios de qualidade e regras de armazenamento)
# ---------------------------------------------------------------------------

PESO_MINIMO = 95.0      # gramas
PESO_MAXIMO = 105.0     # gramas
CORES_ACEITAS = ("azul", "verde")
COMPRIMENTO_MINIMO = 10.0   # cm
COMPRIMENTO_MAXIMO = 20.0   # cm
CAPACIDADE_CAIXA = 10        # peças por caixa


# ---------------------------------------------------------------------------
# FUNÇÕES DE APOIO (entrada de dados com validação)
# ---------------------------------------------------------------------------

def ler_float(mensagem):
    """Lê um número decimal do usuário, repetindo a pergunta até um valor válido."""
    while True:
        valor = input(mensagem).strip().replace(",", ".")
        try:
            return float(valor)
        except ValueError:
            print("  -> Valor inválido. Digite um número (ex: 98.5).")


def ler_texto_nao_vazio(mensagem):
    """Lê um texto do usuário, repetindo a pergunta enquanto estiver vazio."""
    while True:
        valor = input(mensagem).strip()
        if valor:
            return valor
        print("  -> Este campo não pode ficar em branco.")


# ---------------------------------------------------------------------------
# REGRA DE NEGÓCIO: avaliação de qualidade da peça
# ---------------------------------------------------------------------------

def avaliar_peca(peso, cor, comprimento):
    """
    Avalia se uma peça atende aos critérios de qualidade.

    Retorna uma tupla (aprovada, motivos):
        aprovada -> True se todos os critérios forem atendidos, False caso contrário.
        motivos  -> lista de strings explicando cada critério não atendido
                    (lista vazia se a peça foi aprovada).
    """
    motivos = []

    if not (PESO_MINIMO <= peso <= PESO_MAXIMO):
        motivos.append(
            f"Peso fora do padrão ({peso}g; esperado entre {PESO_MINIMO}g e {PESO_MAXIMO}g)"
        )

    if cor.strip().lower() not in CORES_ACEITAS:
        motivos.append(
            f"Cor não aceita ('{cor}'; esperado azul ou verde)"
        )

    if not (COMPRIMENTO_MINIMO <= comprimento <= COMPRIMENTO_MAXIMO):
        motivos.append(
            f"Comprimento fora do padrão ({comprimento}cm; esperado entre "
            f"{COMPRIMENTO_MINIMO}cm e {COMPRIMENTO_MAXIMO}cm)"
        )

    aprovada = len(motivos) == 0
    return aprovada, motivos


# ---------------------------------------------------------------------------
# FUNCIONALIDADE 1: Cadastrar nova peça
# ---------------------------------------------------------------------------

def cadastrar_peca(estado):
    """
    Solicita os dados de uma nova peça, avalia sua qualidade e a direciona
    para a lista de aprovadas (armazenando-a em uma caixa) ou de reprovadas.
    """
    print("\n--- Cadastro de Nova Peça ---")

    id_peca = ler_texto_nao_vazio("ID da peça: ")

    # Verifica se o id já foi usado (em aprovadas ou reprovadas)
    todas = estado["pecas_aprovadas"] + estado["pecas_reprovadas"]
    if any(p["id"] == id_peca for p in todas):
        print(f"  -> Já existe uma peça cadastrada com o ID '{id_peca}'. Cadastro cancelado.")
        return

    peso = ler_float("Peso (g): ")
    cor = ler_texto_nao_vazio("Cor: ")
    comprimento = ler_float("Comprimento (cm): ")

    aprovada, motivos = avaliar_peca(peso, cor, comprimento)

    peca = {
        "id": id_peca,
        "peso": peso,
        "cor": cor,
        "comprimento": comprimento,
    }

    if aprovada:
        peca["caixa"] = None  # será preenchido ao entrar em uma caixa
        estado["pecas_aprovadas"].append(peca)
        armazenar_em_caixa(estado, peca)
        print(f"  -> Peça '{id_peca}' APROVADA e armazenada.")
    else:
        peca["motivos"] = motivos
        estado["pecas_reprovadas"].append(peca)
        print(f"  -> Peça '{id_peca}' REPROVADA. Motivo(s): {'; '.join(motivos)}")


def armazenar_em_caixa(estado, peca):
    """
    Adiciona uma peça aprovada à caixa atualmente em aberto.
    Quando a caixa atinge a capacidade máxima, ela é fechada e uma nova
    caixa (vazia) é iniciada automaticamente.
    """
    numero_caixa = len(estado["caixas_fechadas"]) + 1
    peca["caixa"] = numero_caixa
    estado["caixa_atual"].append(peca)

    if len(estado["caixa_atual"]) == CAPACIDADE_CAIXA:
        estado["caixas_fechadas"].append(estado["caixa_atual"])
        estado["caixa_atual"] = []
        print(f"  -> Caixa #{numero_caixa} atingiu a capacidade máxima e foi FECHADA.")


# ---------------------------------------------------------------------------
# FUNCIONALIDADE 2: Listar peças aprovadas/reprovadas
# ---------------------------------------------------------------------------

def listar_pecas(estado):
    print("\n--- Listar Peças ---")
    print("1. Aprovadas")
    print("2. Reprovadas")
    print("3. Todas")
    opcao = input("Escolha uma opção: ").strip()

    if opcao == "1":
        _imprimir_aprovadas(estado["pecas_aprovadas"])
    elif opcao == "2":
        _imprimir_reprovadas(estado["pecas_reprovadas"])
    elif opcao == "3":
        _imprimir_aprovadas(estado["pecas_aprovadas"])
        _imprimir_reprovadas(estado["pecas_reprovadas"])
    else:
        print("  -> Opção inválida.")


def _imprimir_aprovadas(pecas_aprovadas):
    print(f"\nPeças aprovadas ({len(pecas_aprovadas)}):")
    if not pecas_aprovadas:
        print("  Nenhuma peça aprovada até o momento.")
        return
    for p in pecas_aprovadas:
        print(
            f"  ID: {p['id']:<6} | Peso: {p['peso']}g | Cor: {p['cor']:<8} "
            f"| Comprimento: {p['comprimento']}cm | Caixa: {p['caixa']}"
        )


def _imprimir_reprovadas(pecas_reprovadas):
    print(f"\nPeças reprovadas ({len(pecas_reprovadas)}):")
    if not pecas_reprovadas:
        print("  Nenhuma peça reprovada até o momento.")
        return
    for p in pecas_reprovadas:
        print(
            f"  ID: {p['id']:<6} | Peso: {p['peso']}g | Cor: {p['cor']:<8} "
            f"| Comprimento: {p['comprimento']}cm"
        )
        for motivo in p["motivos"]:
            print(f"      motivo: {motivo}")


# ---------------------------------------------------------------------------
# FUNCIONALIDADE 3: Remover peça cadastrada
# ---------------------------------------------------------------------------

def remover_peca(estado):
    """
    Remove uma peça cadastrada pelo ID.

    Regra de negócio: peças que já estão em uma caixa FECHADA não podem ser
    removidas (a caixa já foi lacrada/expedida). Peças reprovadas ou peças
    aprovadas ainda na caixa em aberto podem ser removidas normalmente.
    """
    print("\n--- Remover Peça ---")
    id_peca = ler_texto_nao_vazio("Informe o ID da peça a remover: ")

    # Procura entre as reprovadas
    for p in estado["pecas_reprovadas"]:
        if p["id"] == id_peca:
            estado["pecas_reprovadas"].remove(p)
            print(f"  -> Peça reprovada '{id_peca}' removida com sucesso.")
            return

    # Procura entre as aprovadas
    for p in estado["pecas_aprovadas"]:
        if p["id"] == id_peca:
            if p["caixa"] is not None and p in estado["caixa_atual"]:
                estado["pecas_aprovadas"].remove(p)
                estado["caixa_atual"].remove(p)
                print(f"  -> Peça aprovada '{id_peca}' removida com sucesso.")
            else:
                print(
                    f"  -> A peça '{id_peca}' já está em uma caixa FECHADA "
                    f"(caixa #{p['caixa']}) e não pode ser removida."
                )
            return

    print(f"  -> Nenhuma peça encontrada com o ID '{id_peca}'.")


# ---------------------------------------------------------------------------
# FUNCIONALIDADE 4: Listar caixas fechadas
# ---------------------------------------------------------------------------

def listar_caixas_fechadas(estado):
    print("\n--- Caixas Fechadas ---")
    caixas = estado["caixas_fechadas"]

    if not caixas:
        print("  Nenhuma caixa foi fechada até o momento.")
    else:
        for numero, caixa in enumerate(caixas, start=1):
            ids = ", ".join(p["id"] for p in caixa)
            print(f"  Caixa #{numero}: {len(caixa)} peças -> [{ids}]")

    # Mostra também a caixa em aberto, para contexto
    em_aberto = estado["caixa_atual"]
    numero_atual = len(caixas) + 1
    if em_aberto:
        ids = ", ".join(p["id"] for p in em_aberto)
        print(
            f"\n  Caixa #{numero_atual} (EM ABERTO): {len(em_aberto)}/{CAPACIDADE_CAIXA} "
            f"peças -> [{ids}]"
        )
    else:
        print(f"\n  Caixa #{numero_atual} (em aberto): vazia.")


# ---------------------------------------------------------------------------
# FUNCIONALIDADE 5: Gerar relatório final
# ---------------------------------------------------------------------------

def gerar_relatorio(estado):
    print("\n=========== RELATÓRIO FINAL ===========")

    total_aprovadas = len(estado["pecas_aprovadas"])
    total_reprovadas = len(estado["pecas_reprovadas"])
    caixas_fechadas = len(estado["caixas_fechadas"])
    caixa_aberta = 1 if estado["caixa_atual"] else 0

    print(f"Total de peças aprovadas : {total_aprovadas}")
    print(f"Total de peças reprovadas: {total_reprovadas}")

    if total_reprovadas:
        print("\nMotivos de reprovação:")
        contagem_motivos = {}
        for p in estado["pecas_reprovadas"]:
            for motivo in p["motivos"]:
                contagem_motivos[motivo] = contagem_motivos.get(motivo, 0) + 1
        for motivo, qtd in contagem_motivos.items():
            print(f"  - {motivo}: {qtd} ocorrência(s)")

    print(f"\nCaixas fechadas         : {caixas_fechadas}")
    print(f"Caixa em aberto          : {caixa_aberta} "
          f"({len(estado['caixa_atual'])}/{CAPACIDADE_CAIXA} peças)")
    print(f"Total de caixas utilizadas: {caixas_fechadas + caixa_aberta}")
    print("========================================")


# ---------------------------------------------------------------------------
# MENU PRINCIPAL
# ---------------------------------------------------------------------------

def exibir_menu():
    print("\n===== SISTEMA DE GESTÃO DE PEÇAS =====")
    print("1. Cadastrar nova peça")
    print("2. Listar peças aprovadas/reprovadas")
    print("3. Remover peça cadastrada")
    print("4. Listar caixas fechadas")
    print("5. Gerar relatório final")
    print("6. Sair")


def main():
    # Estado do sistema: guarda todas as estruturas de dados em um único
    # dicionário, que é passado por referência entre as funções.
    estado = {
        "pecas_aprovadas": [],   # lista de dicts
        "pecas_reprovadas": [],  # lista de dicts
        "caixa_atual": [],       # lista de dicts (caixa em aberto)
        "caixas_fechadas": [],   # lista de listas de dicts
    }

    print("Bem-vindo(a) ao Sistema de Gestão de Peças, Qualidade e Armazenamento!")

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_peca(estado)
        elif opcao == "2":
            listar_pecas(estado)
        elif opcao == "3":
            remover_peca(estado)
        elif opcao == "4":
            listar_caixas_fechadas(estado)
        elif opcao == "5":
            gerar_relatorio(estado)
        elif opcao == "6":
            print("\nEncerrando o sistema. Até logo!")
            break
        else:
            print("  -> Opção inválida. Escolha um número entre 1 e 6.")


if __name__ == "__main__":
    main()
