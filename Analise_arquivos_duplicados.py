import hashlib
import os


def find_duplicate_images(folder):
    """
    Busca e identifica imagens duplicadas em uma pasta.

    Esta função percorre todos os arquivos da pasta especificada,
    calcula o hash MD5 do conteúdo de cada arquivo e verifica se já existe
    algum arquivo com o mesmo hash, o que indica que são duplicatas.

    Parâmetros:
        folder (str): Caminho para a pasta onde estão os arquivos a serem verificados.

    Saída:
        Imprime no console o nome de cada par de arquivos duplicados encontrados.

    Exemplo de uso:
        >>> find_duplicate_images("dataset")
        Duplicata: img_5.png e img_2.png
    """
    hashes = {}
    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)
        if os.path.isfile(path):
            with open(path, 'rb') as f:
                file_hash = hashlib.md5(f.read()).hexdigest()
                if file_hash in hashes:
                    print(f"Duplicata: {filename} e {hashes[file_hash]}")
                hashes[file_hash] = filename

find_duplicate_images("dataset")