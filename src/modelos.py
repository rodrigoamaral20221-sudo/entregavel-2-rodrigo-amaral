import cv2
from pathlib import Path

#-----------------------------------------------------------------------------
#Define oque é uma deteccao / BoundingBox       
class Deteccao:
    def __init__(self, classe_id, x_min, y_min, x_max, y_max):
  
        self.classe_id = classe_id
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max

    def desenhar(self, imagem):
    #Recebe uma imagem e desenha a sua própria caixa

        # Define as cores das clases
        if self.classe_id == 0:
            cor = (0, 255, 0)   # Verde
        else:
            cor = (255, 0, 0)   # Azul
            
        # Desenha a BoudingBox na imagem
        cv2.rectangle(imagem, (self.x_min, self.y_min), (self.x_max, self.y_max), cor, 2)
        
        #Adiciona uma etiqueta com a classe acima da caixa
        texto = f"ID: {self.classe_id}"
        posicao_texto = (self.x_min, max(self.y_min - 10, 10))
        cv2.putText(imagem, texto, posicao_texto, cv2.FONT_HERSHEY_SIMPLEX, 0.5, cor, 1, cv2.LINE_AA)


class ImagemAnotada:
    def __init__(self, nome_arquivo: str, deteccoes: list = None):
        #Armazena o nome da imagem e a lista de objetos Deteccao dela.
        
        self.nome_arquivo = nome_arquivo
        self.deteccoes = deteccoes if deteccoes is not None else []

    def adicionar_deteccao(self, deteccao: Deteccao):
       #Adiciona um novo objeto detecção à lista desta imagem.
    
        self.deteccoes.append(deteccao)

    def gerar_copia_com_caixas(self, pasta_imagens):
        #Gera uma cópia da imagem original com todas as BoudinBox desenhadas, usando o metodo desenhar de cada box
       
        caminho_completo = Path(pasta_imagens) / self.nome_arquivo
        
        # Lê a imagem original
        imagem = cv2.imread(str(caminho_completo))
        if imagem is None:
            raise FileNotFoundError(f"não foi possível ler a imagem '{caminho_completo}'")

        # Valida se as coordenadas respeitam o tamanho da imagem
        altura, largura = imagem.shape[:2]
        for deteccao in self.deteccoes:
            if not (0 <= deteccao.x_min < deteccao.x_max < largura and 0 <= deteccao.y_min < deteccao.y_max < altura):
                raise ValueError(
                    f"coordenadas inválidas ({deteccao.x_min}, {deteccao.y_min}, {deteccao.x_max}, {deteccao.y_max}) "
                    f"para a imagem de {largura}x{altura}"
                )

        # Cria uma cópia para preservar a imagem de entrada intacta
        imagem_copia = imagem.copy()
        
        # passa sobre todas as detecções e desenha cada uma na cópia da imagem
        for deteccao in self.deteccoes:
            deteccao.desenhar(imagem_copia)
            
        return imagem_copia