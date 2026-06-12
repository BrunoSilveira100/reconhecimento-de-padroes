# Da Criação da Imagem ao Reconhecimento de Padrões

Projeto acadêmico de Processamento Digital de Imagens que implementa um fluxo completo para leitura, diagnóstico, correção, processamento, segmentação e reconhecimento de formas geométricas.

A aplicação foi desenvolvida em Python com OpenCV, NumPy e Matplotlib. O sistema analisa imagens contendo círculos, quadrados e triângulos, aplica técnicas de melhoria visual, localiza os objetos e gera imagens e relatórios com os resultados encontrados.

## Sumário

- [Objetivos](#objetivos)
- [Funcionalidades](#funcionalidades)
- [Fluxo de processamento](#fluxo-de-processamento)
- [Tecnologias utilizadas](#tecnologias-utilizadas)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Instalação](#instalação)
- [Preparação das imagens](#preparação-das-imagens)
- [Execução](#execução)
- [Técnicas implementadas](#técnicas-implementadas)
- [Reconhecimento das formas](#reconhecimento-das-formas)
- [Resultados gerados](#resultados-gerados)
- [Relatórios](#relatórios)
- [Testes](#testes)
- [Relação com o trabalho acadêmico](#relação-com-o-trabalho-acadêmico)
- [Limitações conhecidas](#limitações-conhecidas)
- [Possíveis melhorias](#possíveis-melhorias)

## Objetivos

O objetivo principal é demonstrar, de maneira prática, as etapas fundamentais de um sistema de visão computacional:

1. receber imagens de entrada;
2. analisar suas características visuais;
3. identificar problemas de brilho, contraste e ruído;
4. aplicar correções automáticas;
5. executar técnicas clássicas de processamento digital;
6. separar os objetos do fundo;
7. localizar e classificar formas geométricas;
8. calcular características dos objetos;
9. apresentar os resultados visualmente;
10. gerar relatórios para análise e documentação.

O tema escolhido foi **formas geométricas**, com reconhecimento de círculos, quadrados e triângulos.

## Funcionalidades

- leitura automática de imagens da pasta `imagens/`;
- suporte a PNG, JPG, JPEG, BMP, TIFF e WEBP;
- diagnóstico de imagem escura ou excessivamente clara;
- identificação de baixo contraste e presença de ruído;
- correções automáticas independentes para cada problema;
- conversão para tons de cinza;
- ajuste de brilho e contraste;
- aplicação de filtro Gaussiano;
- equalização de histograma;
- redução de ruído com Non-local Means;
- detecção de bordas pelo algoritmo Canny;
- binarização automática pelo método de Otsu;
- limpeza da máscara com operações morfológicas;
- localização de contornos externos;
- reconhecimento de círculos, quadrados e triângulos;
- cálculo de área, perímetro e circularidade;
- desenho de contornos, caixas delimitadoras e rótulos;
- comparação entre a imagem original e o resultado final;
- geração de relatório individual para cada imagem;
- geração de relatório consolidado;
- criação de imagens controladas para demonstração;
- testes automatizados do pipeline.

## Fluxo de processamento

O programa executa o seguinte pipeline para cada imagem:

```text
Imagem de entrada
      |
      v
Diagnóstico visual
      |
      v
Correção automática
      |
      v
Conversão para tons de cinza
      |
      v
Ajuste de brilho e contraste
      |
      v
Filtro Gaussiano e equalização
      |
      v
Redução de ruído
      |
      v
Detecção de bordas
      |
      v
Segmentação e limpeza da máscara
      |
      v
Detecção de contornos
      |
      v
Classificação das formas
      |
      v
Imagens anotadas e relatórios
```

Cada etapa é salva separadamente, permitindo acompanhar visualmente as alterações realizadas pelo sistema.

## Tecnologias utilizadas

| Tecnologia | Utilização |
|---|---|
| Python | Linguagem principal do projeto |
| OpenCV | Processamento, segmentação e reconhecimento |
| NumPy | Manipulação de matrizes e cálculos com pixels |
| Matplotlib | Geração da comparação visual final |
| Unittest | Testes automatizados |

## Estrutura do projeto

```text
projeto/
|-- imagens/                  # Imagens utilizadas como entrada
|-- resultados/              # Etapas e resultados separados por imagem
|-- relatorio/               # Relatórios individuais e consolidado
|-- src/
|   |-- __init__.py
|   |-- correcoes.py         # Diagnóstico e correções automáticas
|   |-- processamento.py     # Técnicas de processamento digital
|   |-- reconhecimento.py    # Segmentação e classificação das formas
|   |-- utils.py             # Leitura, escrita e utilitários
|   |-- gerar_exemplos.py    # Gerador de imagens controladas
|   `-- main.py              # Interface de linha de comando e orquestração
|-- tests/
|   |-- __init__.py
|   `-- test_pipeline.py     # Testes automatizados
|-- requirements.txt         # Dependências do projeto
`-- README.md                # Documentação
```

### Responsabilidade dos módulos

#### `src/correcoes.py`

Calcula as métricas de brilho, contraste e ruído. Com base nos limiares configurados, pode corrigir imagens escuras, excesso de brilho, baixo contraste e ruído.

#### `src/processamento.py`

Executa todas as técnicas obrigatórias de processamento e organiza as imagens intermediárias que serão salvas em `resultados/`.

#### `src/reconhecimento.py`

Cria a máscara de segmentação, encontra os contornos, classifica as formas e produz a imagem final anotada.

#### `src/utils.py`

Centraliza as operações de leitura e gravação, suporta caminhos com caracteres especiais e valida os formatos de imagem aceitos.

#### `src/gerar_exemplos.py`

Gera cinco imagens sintéticas e reproduzíveis por meio do OpenCV: uma normal e outras com escuridão, brilho excessivo, baixo contraste e ruído.

#### `src/main.py`

Recebe os parâmetros da linha de comando, processa todas as imagens e gera os arquivos de saída e os relatórios.

## Requisitos

- Python 3.12 ou superior;
- `pip`;
- Windows, Linux ou macOS.

## Instalação

Clone o repositório e entre na pasta do projeto:

```bash
git clone URL_DO_REPOSITORIO
cd NOME_DO_REPOSITORIO
```

### Windows PowerShell

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Linux ou macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Preparação das imagens

Coloque as imagens que serão analisadas dentro da pasta `imagens/`.

Formatos aceitos:

```text
.png  .jpg  .jpeg  .bmp  .tif  .tiff  .webp
```

Para gerar os cinco exemplos controlados do projeto, execute:

```powershell
python -m src.gerar_exemplos
```

O comando cria:

```text
imagens/
|-- formas_multiplas.png
|-- formas_escuras.png
|-- formas_brilho_excessivo.png
|-- formas_baixo_contraste.png
`-- formas_com_ruido.png
```

Essas imagens são geradas programaticamente com OpenCV e servem para demonstração e testes. Caso a atividade acadêmica exija imagens produzidas por IA generativa, elas devem ser geradas separadamente, acompanhadas de seus prompts, e adicionadas à pasta `imagens/`.

## Execução

Com o ambiente virtual ativado, execute:

```powershell
python -m src.main
```

O programa processará todas as imagens encontradas em `imagens/`.

### Parâmetros opcionais

```powershell
python -m src.main --area-minima 300 --canny-baixo 40 --canny-alto 140 --verbose
```

| Parâmetro | Valor padrão | Descrição |
|---|---:|---|
| `--imagens` | `imagens/` | Pasta com as imagens de entrada |
| `--resultados` | `resultados/` | Pasta das imagens processadas |
| `--relatorio` | `relatorio/` | Pasta dos relatórios |
| `--area-minima` | `250` | Menor área aceita para um objeto |
| `--canny-baixo` | `50` | Limiar inferior do Canny |
| `--canny-alto` | `150` | Limiar superior do Canny |
| `--limiar-escura` | `80` | Média abaixo da qual a imagem é considerada escura |
| `--limiar-clara` | `190` | Média acima da qual a imagem é considerada clara |
| `--limiar-contraste` | `42` | Contraste abaixo do qual a imagem é corrigida |
| `--limiar-ruido` | `8` | Nível acima do qual o ruído é reduzido |
| `--verbose` | desativado | Exibe informações detalhadas no terminal |

Também é possível utilizar pastas externas:

```powershell
python -m src.main `
  --imagens C:\dados\entrada `
  --resultados C:\dados\saida `
  --relatorio C:\dados\relatorios
```

## Técnicas implementadas

### Diagnóstico visual

O sistema utiliza métricas numéricas simples para orientar as correções:

- **brilho:** média das intensidades dos pixels em tons de cinza;
- **contraste:** desvio-padrão das intensidades;
- **ruído:** desvio-padrão do resíduo entre a imagem e uma versão filtrada pela mediana.

Essas métricas ajudam a detectar problemas, mas não substituem completamente a avaliação visual humana.

### Correção de brilho com gamma

A transformação gamma modifica principalmente os tons médios. Ela é usada tanto para clarear imagens escuras quanto para reduzir o brilho de imagens muito claras.

### Correção de contraste com CLAHE

O CLAHE aumenta o contraste local em pequenas regiões da imagem e limita amplificações excessivas. Em imagens coloridas, a correção é aplicada somente ao canal de luminosidade do espaço de cores LAB.

### Conversão para tons de cinza

Remove as informações de cor e mantém a intensidade luminosa. Isso reduz a complexidade das etapas posteriores.

### Ajuste de brilho

Desloca os valores dos pixels para aproximar a média da imagem de um valor de referência.

### Ajuste de contraste

Amplia a diferença entre as regiões claras e escuras, utilizando a média e o desvio-padrão da imagem.

### Filtro Gaussiano

Suaviza pequenas variações e reduz detalhes finos antes das operações de segmentação e detecção de bordas.

### Equalização de histograma

Redistribui as intensidades disponíveis e pode destacar detalhes pouco visíveis em imagens com baixo contraste.

### Redução de ruído

Utiliza o algoritmo Non-local Means, que procura regiões semelhantes na imagem para reduzir variações indesejadas preservando parte das bordas.

### Detecção de bordas Canny

Identifica mudanças intensas de luminosidade e produz uma imagem binária com os limites mais relevantes dos objetos.

## Reconhecimento das formas

O reconhecimento ocorre em quatro etapas principais.

### 1. Segmentação

A imagem corrigida é suavizada e binarizada automaticamente pelo método de Otsu. O programa compara a máscara normal e a invertida para escolher a polaridade em que o fundo ocupa menos as bordas.

### 2. Operações morfológicas

São aplicadas abertura e fechamento para remover pequenos pontos, preencher falhas e melhorar a continuidade dos objetos.

### 3. Detecção de contornos

O OpenCV localiza os contornos externos. Contornos menores que `--area-minima` ou grandes demais em relação à imagem são descartados.

### 4. Classificação

Cada contorno é aproximado por um polígono:

| Condição | Classificação |
|---|---|
| 3 vértices | Triângulo |
| 4 vértices e proporção próxima de 1 | Quadrado |
| 4 vértices com outra proporção | Quadrilátero |
| 5 ou mais vértices e circularidade suficiente | Círculo |
| Demais casos | Forma não identificada |

A circularidade é calculada por:

```text
circularidade = 4 * pi * área / perímetro²
```

Valores próximos de `1` indicam formas mais circulares.

## Resultados gerados

Para cada imagem é criada uma pasta própria. Por exemplo, para `imagens/formas_multiplas.png`:

```text
resultados/formas_multiplas/
|-- 00_original.png
|-- 01_correcao_automatica.png
|-- 02_escala_cinza.png
|-- 03_ajuste_brilho.png
|-- 04_ajuste_contraste.png
|-- 05_filtro_gaussiano.png
|-- 06_equalizacao_histograma.png
|-- 07_reducao_ruido.png
|-- 08_bordas_canny.png
|-- 09_mascara_segmentacao.png
|-- 10_formas_reconhecidas.png
`-- 11_comparacao.png
```

Na imagem final, cada objeto recebe:

- contorno colorido;
- caixa delimitadora;
- número de identificação;
- nome da forma;
- área aproximada em pixels quadrados.

## Relatórios

Para cada imagem, o programa gera um arquivo TXT com:

- nome da imagem;
- quantidade de objetos;
- área total encontrada;
- tipos e quantidades de formas;
- métricas antes e depois das correções;
- área, perímetro, circularidade e caixa de cada objeto;
- lista de processamentos aplicados.

Exemplo simplificado:

```text
Nome da imagem: formas_multiplas.png
Quantidade de objetos: 5
Área total encontrada: 96328.00 px2
Tipos de formas encontradas: Círculo (2), Quadrado (2), Triângulo (1)

Métricas visuais:
  Antes: brilho=213.52; contraste=63.66; ruído=1.01
  Depois: brilho=184.29; contraste=78.69; ruído=1.24

Objetos encontrados:
  1. Triângulo: área=15296.00 px2; perímetro=588.56 px
  2. Quadrado: área=25598.00 px2; perímetro=637.66 px
```

O arquivo `relatorio/relatorio_consolidado.txt` reúne os resultados de todas as imagens processadas e informa quantos arquivos foram concluídos ou apresentaram falha.

## Testes

Execute a suíte de testes com:

```powershell
python -m unittest discover -v
```

Os testes verificam:

- reconhecimento de círculo, quadrado e triângulo;
- presença de todas as etapas obrigatórias;
- melhoria do brilho de uma imagem escura;
- execução completa com geração de imagens e relatório.

Resultado esperado:

```text
Ran 4 tests

OK
```

## Relação com o trabalho acadêmico

O projeto implementa as partes técnicas de processamento, correção e reconhecimento solicitadas pela atividade.

| Etapa da atividade | Situação no projeto |
|---|---|
| Criação de imagens | Existem cinco exemplos sintéticos gerados por OpenCV |
| Análise de brilho, contraste e ruído | Implementada automaticamente |
| Tons de cinza | Implementado |
| Ajuste de brilho | Implementado |
| Ajuste de contraste | Implementado |
| Filtro Gaussiano | Implementado |
| Equalização de histograma | Implementada |
| Detecção de bordas | Implementada com Canny |
| Redução de ruído | Implementada com Non-local Means |
| Correção de problemas | Implementada para quatro condições |
| Reconhecimento de padrões | Implementado para formas geométricas |
| Quantidade, área e formato | Incluídos nas imagens e relatórios |
| Imagem com objetos destacados | Gerada automaticamente |
| Testes automatizados | Implementados |

Para atender literalmente à etapa de IA generativa da atividade, ainda devem ser incluídos:

- pelo menos dez imagens realmente geradas por IA;
- prompts utilizados na geração;
- descrição e análise visual de cada imagem;
- reflexão individual final;
- relatório acadêmico exportado em PDF;
- capturas de tela selecionadas dos resultados.

## Limitações conhecidas

- formas sobrepostas podem ser interpretadas como um único contorno;
- perspectiva forte pode transformar quadrados em quadriláteros;
- sombras e fundos complexos podem prejudicar a segmentação;
- a classificação depende da qualidade do contorno encontrado;
- objetos muito pequenos podem ser descartados pela área mínima;
- imagens com resoluções muito diferentes podem exigir novos parâmetros;
- a média global de brilho pode classificar fundos muito claros como excesso de brilho;
- a redução de ruído nem sempre melhora todas as métricas numéricas;
- a análise de nitidez, naturalidade e erros visuais ainda depende de observação humana.

## Possíveis melhorias

- incluir detecção automática de desfoque;
- analisar canais de cor separadamente;
- utilizar segmentação por cor para fundos complexos;
- permitir configuração por arquivo YAML ou JSON;
- criar gráficos de histogramas antes e depois do processamento;
- gerar automaticamente um relatório em PDF;
- criar uma interface gráfica ou aplicação web;
- incluir novas classes de formas e objetos;
- adicionar imagens produzidas por IA generativa;
- empregar aprendizado de máquina em cenários mais complexos.

## Conclusão

O projeto demonstra como uma imagem pode ser transformada em informação por meio de técnicas clássicas de processamento digital e visão computacional. O sistema parte dos pixels originais, identifica problemas visuais, aplica correções, separa os objetos do fundo e extrai características como formato, área, perímetro e circularidade.

Nas imagens controladas, o pipeline reconhece corretamente círculos, quadrados e triângulos, gerando resultados visuais e relatórios que facilitam a análise de cada etapa. A solução também evidencia que a qualidade da imagem, o fundo, a iluminação e os parâmetros utilizados influenciam diretamente o desempenho do reconhecimento.

## Autor

Desenvolvido para a disciplina de Processamento Digital de Imagens.

