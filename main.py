import ast
import csv
import re
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
ARQUIVO_DADOS = BASE_DIR / "dados.csv"

empresa = {
    "nome": "Estoque Fácil",
    "cnpj": "12.345.678/0001-00",
    "cidade": "São Paulo",
    "equipe": "Equipe de Estoque",
}

produtos = []
matriz_estoque = []


def carregar_dados():
    global empresa

    empresa_default = {
        "nome": "Estoque Fácil",
        "cnpj": "12.345.678/0001-00",
        "cidade": "São Paulo",
        "equipe": "Equipe de Estoque",
    }
    empresa.update(empresa_default)
    produtos.clear()

    if not ARQUIVO_DADOS.exists():
        return

    try:
        conteudo = ARQUIVO_DADOS.read_text(encoding="utf-8").strip()
        if not conteudo:
            return

        dados = None
        if "dados=" in conteudo:
            dados = ast.literal_eval(conteudo.split("=", 1)[1].strip())
        else:
            with ARQUIVO_DADOS.open("r", encoding="utf-8", newline="") as arquivo:
                dados = [linha for linha in csv.reader(arquivo) if linha and any(item.strip() for item in linha)]

        if not isinstance(dados, list):
            return

        linhas = [linha for linha in dados if isinstance(linha, list) and any(str(item).strip() for item in linha)]
        if not linhas:
            return

        empresa["nome"] = str(linhas[1][0]).strip() if len(linhas) > 1 and linhas[1] else empresa["nome"]

        for indice, linha in enumerate(linhas[1:], start=1):
            if len(linha) < 3:
                continue

            nome_produto = str(linha[1]).strip()
            quantidade = str(linha[2]).strip()
            if not nome_produto:
                continue

            codigo = indice
            if len(linha) > 4:
                codigo_match = re.search(r"\d+", str(linha[4]).strip())
                if codigo_match:
                    codigo = int(codigo_match.group())

            try:
                qtd = int(quantidade)
            except ValueError:
                qtd = 0

            produtos.append(
                {
                    "codigo": codigo,
                    "nome": nome_produto,
                    "categoria": "Geral",
                    "quantidade": qtd,
                }
            )
    except (SyntaxError, ValueError, TypeError, OSError):
        empresa.update(empresa_default)
        produtos.clear()


carregar_dados()


def mostrar_empresa():
    print("\n=== DADOS DA EMPRESA ===")
    for campo, valor in empresa.items():
        print(f"{campo.capitalize()}: {valor}")


def mostrar_produtos():
    print("\n=== PRODUTOS ===")
    if not produtos:
        print("Nenhum produto cadastrado.")
        return

    for produto in produtos:
        print(
            f"Código: {produto['codigo']} | {produto['nome']} | "
            f"Categoria: {produto['categoria']} | "
            f"Quantidade: {produto['quantidade']}"
        )


def ler_inteiro(mensagem, minimo=0):
    while True:
        try:
            valor = int(input(mensagem))
            if valor < minimo:

                print(f"Digite um número maior ou igual a {minimo}.")
                continue
            return valor
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")


def localizar_produto():
    codigo = ler_inteiro("Digite o código do produto: ", minimo=1)
    for produto in produtos:
        if produto["codigo"] == codigo:
            return produto
    print("Produto não encontrado.")
    return None


def buscar_produto():
    produto = localizar_produto()
    if produto:
        print(
            f"Código: {produto['codigo']} | {produto['nome']} | "
            f"Categoria: {produto['categoria']} | "
            f"Quantidade: {produto['quantidade']}"
        )


def adicionar_produto():
    nome = input("Nome do produto: ").strip()
    if not nome:
        print("O nome do produto não pode ficar vazio.")
        return

    categoria = input("Categoria: ").strip()
    if not categoria:
        print("A categoria não pode ficar vazia.")
        return

    quantidade = ler_inteiro("Quantidade inicial: ")
    codigo = max((produto["codigo"] for produto in produtos), default=0) + 1
    produtos.append(
        {
            "codigo": codigo,
            "nome": nome,
            "categoria": categoria,
            "quantidade": quantidade,
        }
    )
    print(f"Produto cadastrado com o código {codigo}.")


def entrada_estoque():
    produto = localizar_produto()
    if produto:
        quantidade = ler_inteiro("Quantidade de entrada: ", minimo=1)
        produto["quantidade"] += quantidade
        print(f"Estoque atualizado: {produto['quantidade']} unidades.")


def saida_estoque():
    produto = localizar_produto()
    if not produto:
        return

    quantidade = ler_inteiro("Quantidade de saída: ", minimo=1)
    if quantidade > produto["quantidade"]:
        print("Saída não realizada: quantidade maior que o estoque disponível.")
        return

    produto["quantidade"] -= quantidade
    print(f"Estoque atualizado: {produto['quantidade']} unidades.")


def atualizar_matriz():
    matriz_estoque.clear()
    for produto in produtos:
        quantidade = produto["quantidade"]
        if quantidade == 0:
            estado = "Sem estoque"
        elif quantidade <= 5:
            estado = "Estoque baixo"
        else:
            estado = "Estoque normal"
        matriz_estoque.append([produto["nome"], quantidade, estado])


def mostrar_matriz():
    atualizar_matriz()
    print("\n=== MATRIZ 2D DO ESTOQUE ===")
    print(f"{'Produto':<15}{'Quantidade':<12}{'Estado':<20}")
    print("-" * 47)
    for nome, quantidade, estado in matriz_estoque:
        print(f"{nome:<15}{quantidade:<12}{estado:<20}")


def verificar_estoque_baixo():
    baixos = [produto for produto in produtos if produto["quantidade"] <= 5]
    print("\n=== ESTOQUE BAIXO ===")
    if not baixos:
        print("Nenhum produto com estoque baixo.")
        return

    for produto in baixos:
        estado = "Sem estoque" if produto["quantidade"] == 0 else "Estoque baixo"
        print(f"{produto['nome']}: {produto['quantidade']} unidades ({estado})")


def menu():
    while True:
        print("\n" + "=" * 50)
        print("       CONTROLE DE ESTOQUE - ESTOQUE FÁCIL")
        print("=" * 50)
        print("1 - Mostrar dados da empresa")
        print("2 - Mostrar produtos")
        print("3 - Mostrar matriz 2D do estoque")
        print("4 - Buscar produto")
        print("5 - Adicionar produto")
        print("6 - Entrada de estoque")
        print("7 - Saída de estoque")
        print("8 - Verificar estoque baixo")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            mostrar_empresa()
        elif opcao == "2":
            mostrar_produtos()
        elif opcao == "3":
            mostrar_matriz()
        elif opcao == "4":
            buscar_produto()
        elif opcao == "5":
            adicionar_produto()
        elif opcao == "6":
            entrada_estoque()
        elif opcao == "7":
            saida_estoque()
        elif opcao == "8":
            verificar_estoque_baixo()
        elif opcao == "0":
            print("\nSistema encerrado. Obrigado por utilizar o Estoque Fácil!")
            break
        else:
            print("Opção inválida. Digite uma opção entre 0 e 8.")


if __name__ == "__main__":
    menu()