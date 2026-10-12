import sys
from pathlib import Path
import cv2
from arquivos import carregar_imagens_anotadas

# Tamanho máximo da janela de exibição (a imagem salva continua na resolução original)
LARGURA_MAX_TELA = 1280
ALTURA_MAX_TELA = 720

def main():
    # Define os caminhos base utilizando pathlib
    diretorio_raiz = Path(__file__).resolve().parent.parent
    pasta_dados = diretorio_raiz / "dados"
    pasta_resultados = diretorio_raiz / "resultados"
    pasta_imagens = pasta_dados / "imagens"

    print("Carregando anotações e organizando imagens...")

    # Carrega a lista de objetos ImagemAnotada
    try:
        imagens_anotadas = carregar_imagens_anotadas(pasta_dados)
    except (OSError, ValueError) as erro:
        sys.exit(f"Erro ao ler as anotações: {erro}")

    # Garante que a pasta de resultados existe
    pasta_resultados.mkdir(exist_ok=True)

    print(f"Total de imagens carregadas para processamento: {len(imagens_anotadas)}")
    print("Controles do usuario: Pressione ESPAÇO para ir para a próxima imagem, ou 'q' para sair.\n")

    # Loop pelas imagens anotadas
    for img_anotada in imagens_anotadas:
        nome_arquivo = img_anotada.nome_arquivo
        quantidade_BBox = len(img_anotada.deteccoes)

        # Mostra no terminal o nome da imagem atual e a quantidade de bouding Box
        print(f"Imagem atual: {nome_arquivo} | Quantidade de Bounding Box: {quantidade_BBox}")

        # Gera a cópia da imagem com todas as caixas desenhadas
        try:
            imagem_com_caixas = img_anotada.gerar_copia_com_caixas(pasta_imagens)
        except (OSError, ValueError) as erro:
            cv2.destroyAllWindows()
            sys.exit(f"Erro ao processar a imagem {nome_arquivo}: {erro}")

        #Salva a imagem processada na pasta de resultados
        caminho_saida = pasta_resultados / nome_arquivo
        cv2.imwrite(str(caminho_saida), imagem_com_caixas)

        #Se precisar redimensionar apenas para caber na tela de exibição sem alterar a resolução original salva
        altura, largura = imagem_com_caixas.shape[:2]
        escala = min(1.0, LARGURA_MAX_TELA / largura, ALTURA_MAX_TELA / altura)
        imagem_exibicao = imagem_com_caixas.copy()
        if escala < 1.0:
            imagem_exibicao = cv2.resize(imagem_exibicao, None, fx=escala, fy=escala, interpolation=cv2.INTER_AREA)

        # Escreve o nome da imagem e a legenda das cores na janela (apenas na cópia de exibição)
        cv2.rectangle(imagem_exibicao, (0, 0), (260, 75), (0, 0, 0), -1)
        cv2.putText(imagem_exibicao, nome_arquivo, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(imagem_exibicao, "ID 0 = verde", (10, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
        cv2.putText(imagem_exibicao, "ID 1 = azul", (10, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
        
        # Exibe a imagem
        titulo_janela = f"Visualizador - {nome_arquivo}"
        cv2.imshow(titulo_janela, imagem_exibicao)

        # Loop para o controle do usuario
        encerrar_programa = False
        while True:
            # Espera indefinidamente por uma tecla
            tecla = cv2.waitKey(0) & 0xFF

            # Tecla 'q' encerra o programa
            if tecla == ord('q'):
                print("\nEncerramento solicitado pelo usuario ('q'). Fechando...")
                encerrar_programa = True
                break
            
            # Tecla Espaço avança para a próxima imagem
            elif tecla == ord(' '):
                break

        # Fecha a janela atual antes de avançar
        cv2.destroyAllWindows()

        if encerrar_programa:
            break

    print("\nProcessamento concluído com sucesso!")

if __name__ == "__main__":
    main()
