import os
import pathlib
import pandas as pd

def ler_arquivo (nome_arquivo):
    arq = definir_arquivo(nome_arquivo)
    df_turma = None
    try:
        df_turma = pd.read_csv(arq, sep=",", encoding="UTF-8", header=None)
    except:
        print("Erro ao abrir o arquivo")
        exit()
    return df_turma.values.tolist()

def definir_arquivo (nome_arquivo):
    dir_corrente = os.path.dirname(__file__)
    arquivo = os.path.join(dir_corrente, nome_arquivo)
    return arquivo

# codigo antigo
def gravar_arquivo(produtos):
    '''
    Grava os dados dos produtos em um arquivo produtos.csv
    '''
    dir_current = pathlib.Path(__file__).parent.resolve()
    arq = str(dir_current) + "//produtos.csv"
    try:
        with open(arq, "w", encoding="UTF-8") as arquivo:
            for produto in produtos:
                linha = f"{produto[0]},{produto[1]},{produto[2]},{produto[3]}\n"
                arquivo.write(linha)
    except:
        print("Erro ao salvar arquivo.")

