import csv
from pathlib import Path
from modelos import Deteccao, ImagemAnotada

def ler_anotacoes_csv(caminho_csv):
    #--------------------------------------------------------------------------------------------------------------
    # Lê o arquivo CSV de anotações, converte os valores para inteirose agrupa as detecções por nome de imagem.
    anotacoes_por_imagem = {}
    
    caminho = Path(caminho_csv)

    # Abre as anotacoes com codificação UTF-8
    with open(caminho, mode='r', encoding='utf-8') as arquivo:
        leitor = csv.DictReader(arquivo)
        
        for linha in leitor:
            try:
                nome_imagem = linha['imagem']

                #converte o numeros para inteiros
                classe_id = int(linha['classe_id'])
                x_min = int(linha['x_min'])
                y_min = int(linha['y_min'])
                x_max = int(linha['x_max'])
                y_max = int(linha['y_max'])
            except (KeyError, TypeError, ValueError) as erro:
                # Linha com campo ausente ou valor não numérico
                raise ValueError(f"linha {leitor.line_num} do CSV inválida ({erro})")
            
            # cria o objeto de detecção da linha atual
            deteccao = Deteccao(classe_id, x_min, y_min, x_max, y_max)
            
            # Agrupa as caixas pelo nome da imagem
            if nome_imagem not in anotacoes_por_imagem:
                anotacoes_por_imagem[nome_imagem] = []
            anotacoes_por_imagem[nome_imagem].append(deteccao)
            
    return anotacoes_por_imagem

#----------------------------------------------------------------------------
#Cria a lista de objetos ImagemAnotada ordenados alfabeticamente.
def carregar_imagens_anotadas(diretorio_dados):
        
    caminho_csv = Path(diretorio_dados) / "anotacoes.csv"
    dados_agrupados = ler_anotacoes_csv(caminho_csv)
    
    imagens_anotadas = []
    
    # Ordena as chaves alfabeticamente
    for nome_imagem in sorted(dados_agrupados.keys()):
        deteccoes = dados_agrupados[nome_imagem]
        
        # Cria o objeto ImagemAnotada contendo o nome e a lista de detecções
        imagem_obj = ImagemAnotada(nome_imagem, deteccoes)
        imagens_anotadas.append(imagem_obj)
        
    return imagens_anotadas