import os
import shutil

pasta_origem1 = 'data/train'
pasta_origem2 = 'data/test'
pasta_destino = 'data/merged'  

os.makedirs(pasta_destino, exist_ok=True)

contador = 1  

def processar_pasta(pasta_origem):
    """
    Move e renomeia imagens de uma pasta de origem para uma pasta de destino.

    Esta função percorre todos os arquivos da pasta especificada, identifica imagens
    com extensões comuns ('.png', '.jpg', '.jpeg', '.bmp', '.gif'), e as move para
    a pasta de destino (`pasta_destino`), renomeando-as de forma sequencial no formato:
    `img_1`, `img_2`, etc., mantendo a extensão original.

    Parâmetros:
        pasta_origem (str): Caminho da pasta de onde as imagens serão movidas.

    Observações:
        - A numeração é controlada pela variável global `contador`.
        - As imagens são removidas da pasta original, pois é utilizado `shutil.move()`.
        - O script cria automaticamente a pasta de destino, caso ela não exista.

    Exemplo de uso:
        >>> processar_pasta("data/train")
        Copiado: data/train/foto1.jpg -> data/merged/img_1.jpg
    """
    global contador
    for arquivo in os.listdir(pasta_origem):
        if arquivo.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            novo_nome = f'img_{contador}{os.path.splitext(arquivo)[1]}'  
            caminho_origem = os.path.join(pasta_origem, arquivo)
            caminho_destino = os.path.join(pasta_destino, novo_nome)
            shutil.move(caminho_origem, caminho_destino)  
            print(f'Copiado: {caminho_origem} -> {caminho_destino}')
            contador += 1

# Processa as pastas de treino e teste
processar_pasta(pasta_origem1)
processar_pasta(pasta_origem2)

print(f'Total de imagens processadas: {contador - 1}')
