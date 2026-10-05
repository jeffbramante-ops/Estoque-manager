# Aluno 1 - Diego

empresa = {
    "nome": "Estoque Fácil",
    "cnpj": "12.345.678/0001-00",
    "cidade": "São Paulo",
    "quantidade": "Equipe de Estoque"
}

produtos = [
    {
        "codigo": 1,
        "nome": "Teclado",
        "categoria":'Periféricos'
        "quantidade": 10
    },
    {
        "codigo": 2,
        "nome": "Mouse",
        "categoria": "Periféricos",
        "quantidade":15
    },
    {
        "codigo": 3,
        "nome": "Moinitor",
        "categoria": "Eletrônicas",
        "quantidade": 5
    },
    {
        "codigo": 4,
        "nome": "Notebook",
        "categoria": "Computadores",
        "quantidade": 8
    }
]

# Aluno 2: Lucca Coelho da Silva
# Matriz 2D de estado do estoque

matriz_estoque = [
    ["Teclado", 20, "Estoque normal"],
    ["Mouse", 15, "Estoque normal"],
    ["Monitor", 5, "Estoque baixo"],
    ["Noteook", 8, "Estoque normal"]
]

def mostrar_matriz():
    print("\n=== MATRIZ 2D DO ESTOQUE ===")

    print(f"{'Produto':<15}
    {'Quantidade':<12}
    {'Estado':<20}")
    print("-" * 50)

    for linha in matriz_estoque:
        print(f"{linha[0]:<15}
        {linha[1]:<12} {linha[2]:<20}")

def atualizar_matriz():
    matriz_estoque.clear()

    for produto in produtos:
    
    quantidade = produto ["quantidade"]

    if quantidade == 0:
        estado = "sem estoque"
    elif quantidade <= 5:
        estado = "Estoque baixo"
    else
        estado = "Estoque normal"

    matriz_estoque.append([
        produto["nome"],
        quantidade,
        estado
    ])
