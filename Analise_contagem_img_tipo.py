import os
from collections import defaultdict

def contar_e_listar_jpeg(pasta):
    """
    Conta a quantidade de arquivos por extensão em uma pasta e lista arquivos .jpeg.

    Esta função percorre todos os arquivos da pasta informada, contabiliza a quantidade
    de arquivos para cada extensão encontrada e retorna separadamente a lista de arquivos
    com extensão `.jpeg`.

    Parâmetros:
        pasta (str): Caminho para a pasta onde os arquivos serão analisados.

    Retorno:
        tuple:
            - dict: Um dicionário com a contagem de arquivos por extensão.
            - list: Uma lista contendo os nomes dos arquivos com extensão `.jpeg`.

    Exemplo de uso:
        >>> resultados, jpegs = contar_e_listar_jpeg("data")
        >>> print(resultados)
        {'.png': 120, '.jpeg': 15}
        >>> print(jpegs)
        ['foto1.jpeg', 'imagem2.jpeg']
    """
    contador = defaultdict(int)
    arquivos_jpeg = []  
    
    for arquivo in os.listdir(pasta):
        caminho_completo = os.path.join(pasta, arquivo)
        if os.path.isfile(caminho_completo):
            extensao = os.path.splitext(arquivo)[1].lower()
            contador[extensao] += 1
            
            if extensao == '.jpeg':  
                arquivos_jpeg.append(arquivo)
    
    return contador, arquivos_jpeg


# Exemplo de execução
pasta = 'data'
resultados, jpegs = contar_e_listar_jpeg(pasta)

print("Quantidade de arquivos por tipo:")
for extensao, quantidade in resultados.items():
    print(f"{extensao}: {quantidade} arquivo(s)")

print("\nArquivos .jpeg encontrados:")
for arquivo in jpegs:
    print(arquivo)
