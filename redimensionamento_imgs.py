from PIL import Image
import os

def redimensionar_imagens(pasta_origem, pasta_final):
    """
    Redimensiona todas as imagens de uma pasta para 225x225 pixels.

    Esta função percorre todos os arquivos da pasta de origem, abre cada imagem
    utilizando a biblioteca Pillow (PIL), redimensiona para 225x225 pixels e salva
    na pasta de destino mantendo o nome original do arquivo.

    Parâmetros:
        pasta_origem (str): Caminho da pasta contendo as imagens originais.
        pasta_final (str): Caminho da pasta onde as imagens redimensionadas serão salvas.

    Observações:
        - A pasta de destino deve existir antes de executar a função.
        - O redimensionamento não mantém a proporção da imagem original.
        - Formatos suportados dependem do Pillow (JPEG, PNG, BMP, etc.).

    Exemplo de uso:
        >>> redimensionar_imagens("data_origem", "data_final")
        Imagem salva: data_final/img1.jpg
    """
    for img in os.listdir(pasta_origem):
        caminho = os.path.join(pasta_origem, img)
        imagem = Image.open(caminho)
        imagem_redimensionada = imagem.resize((225, 225))
        caminho_final = os.path.join(pasta_final, img)
        imagem_redimensionada.save(caminho_final)
        print(f"Imagem salva: {caminho_final}")

# Exemplo de execução
pasta_origem = r"C:\Users\Acer\Downloads\data_origem"
pasta_final = r"C:\Users\Acer\Downloads\data_final"
redimensionar_imagens(pasta_origem, pasta_final)
