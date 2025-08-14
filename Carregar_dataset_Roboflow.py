from roboflow import Roboflow

def upload_dataset_roboflow():
    """
    Faz o upload de um conjunto de dados para o Roboflow.

    Esta função conecta-se à conta do Roboflow usando uma chave de API,
    seleciona o projeto desejado e realiza o upload das imagens contidas
    na pasta especificada.

    Observações:
        - É necessário ter uma conta no Roboflow e criar um projeto previamente.
        - O nome do workspace e do projeto devem corresponder aos existentes na conta.
        - A pasta informada deve conter as imagens ou estar no formato aceito pelo Roboflow.

    Fluxo:
        1. Conecta ao Roboflow utilizando a API key.
        2. Acessa o workspace e o projeto especificado.
        3. Envia as imagens da pasta `data_final` para o projeto.

    Exemplo de uso:
        >>> upload_dataset_roboflow()
        Upload concluído para o projeto 'dataset-cyst-sop-ps0dk'.
    """
    rf = Roboflow(api_key="uZirVj6CEwmzqPSrvHNd")  
    project = rf.workspace("meu-espao-de-trabalho").project("dataset-cyst-sop-ps0dk")
    project.upload(
        "data_final", 
    )

upload_dataset_roboflow()
