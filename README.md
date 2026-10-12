# Entregável 2

**Autor:** Rodrigo Amaral de Castro Valente

## Objetivo

Visualizador de imagens com antoações de bouding box. O programa lê as coordenadas das bounding boxes de um arquivo CSV, transforma cada anotação em um objeto e usa um loop com OpenCV para desenhar e exibir as caixas sobre as imagens fornecidas.

Para cada imagem, o progrma:
- desenha as caixas na resolução original, com uma cor por classe (verde para a classe 0 e azul para a classe 1);
- salva a imagem anotada em `resultados/`, com o mesmo nome do arquivo original;
- exibe a imagem em uma janela do OpenCV, com o nome da imagem e a legenda das cores;
- mostra no terminal o nome da imagem atual e a quantidade de caixas desenhadas.

## Dependências
- Python 3
- opencv-python (listado em `requirements.txt`)

## Como executar

A partir da raiz do repositório (Linux ou WSL com suporte gráfico):

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python src/main.py
```

## Controles do visualizador

| Tecla | Ação |
|-------|------|
| Espaço | Avança para a próxima imagem. Ao chegar na última, as janelas são fechadas. |
| `q` | Encerra o programa. A imagem atual já foi salva; as demais não são geradas. |
| Outras teclas | Mantêm a imagem atual na tela. |

## Estrutura do projeto

```
.
├── src/
│   ├── main.py        # programa principal: função main() e loop de visualização
│   ├── modelos.py     # classes Deteccao e ImagemAnotada
│   └── arquivos.py    # funções de leitura do CSV e organização dos objetos
├── dados/
│   ├── anotacoes.csv  # anotações (entrada do programa)
│   └── imagens/       # dez imagens originais
├── resultados/        # imagens anotadas geradas na execução
├── evidencias/        # capturas do terminal e do visualizador
├── requirements.txt
└── README.md
```

## Classes

- **`Deteccao`**: armazena `classe_id`, `x_min`, `y_min`, `x_max` e `y_max` de uma bounding box. Possui o método `desenhar(imagem)`, que recebe uma imagem e desenha a própria caixa com OpenCV, usando verde para a classe 0 e azul para a classe 1, além do rótulo `ID: n`.
- **`ImagemAnotada`**: armazena o nome do arquivo da imagem e a lista de objetos `Deteccao` associados a ela. O método `adicionar_deteccao` inclui uma caixa na lista, e `gerar_copia_com_caixas` lê a imagem, cria uma cópia (preservando a original) e chama o método `desenhar` de cada detecção.

## Leitura dos dados e tratamento de erros

`arquivos.py` lê `dados/anotacoes.csv` (UTF-8, separador vírgula), converte os campos numéricos para inteiros e agrupa as caixas pelo nome da imagem, independentemente da ordem das linhas. As imagens são percorridas em ordem alfabética.

Se o CSV ou uma imagem não puderem ser lidos, se uma linha tiver campos inválidos ou se as coordenadas não respeitarem `0 ≤ x_min < x_max < largura` e `0 ≤ y_min < y_max < altura`, o programa mostra uma mensagem de erro clara e encerra.

## Observações

- As caixas são desenhadas na resolução original. Quando a imagem é maior que 1280×720, apenas a cópia usada para exibição é reduzida; o arquivo salvo em `resultados/` mantém o tamanho original.
- A legenda e o nome da imagem aparecem somente na janela de exibição, não nas imagens salvas.