# Simulação de Atenuação de Múons Cósmicos (GEANT4 + CRY)

Simulação Monte Carlo, desenvolvida em GEANT4, da atenuação do fluxo de múons cósmicos ao atravessarem uma estrutura de concreto com múltiplas lajes — representando um bloco de salas de aula de quatro pavimentos do campus da Universidade Tecnológica Federal do Paraná (UTFPR), em Toledo.

Projeto de Iniciação Científica (bolsa Fundação Araucária), com resultados submetidos ao V SIMPOESTE / XII ENDICT e à XXXI SICITE (UTFPR, Cornélio Procópio).

## Visão geral

A simulação modela:
- Um volume-mundo de ar (120 × 120 × 600 m);
- Quatro lajes de concreto (`G4_CONCRETE`, NIST) de 15 cm de espessura cada, espaçadas em 4 m, representando as separações entre os quatro pavimentos da edificação;
- Uma fonte primária de raios cósmicos gerada pela biblioteca [CRY](https://nuclear.llnl.gov/simulation/) (*Cosmic-Ray Shower Library*), configurada para a latitude de Toledo, PR (−24,7°), ao nível do mar.

Para cada múon simulado, três categorias de evento são registradas: o momento ao cruzar um plano de referência logo acima da estrutura (entrada), a energia depositada a cada passo dentro do concreto, e o momento final no término da trajetória (morte). Esses três eventos são pareados individualmente por múon (via `EventID` + `TrackID`), permitindo medir diretamente a perda de momento de cada partícula, sem depender de comparação entre simulações independentes.

## Requisitos

- [GEANT4](https://geant4.web.cern.ch/) (testado com a série 11.x)
- [CRY](https://nuclear.llnl.gov/simulation/) — biblioteca geradora de chuveiros cósmicos
- CMake ≥ 3.16
- Compilador C++ compatível com C++17
- Python 3.9+ com `pandas`, `numpy` e `matplotlib` (para os scripts de análise)

## Estrutura do repositório

```
.
├── src/                       # Classes de usuário do GEANT4
│   ├── DetectorConstruction.cc   # Geometria: mundo, lajes de concreto
│   ├── PrimaryGeneratorAction.cc # Interface com o gerador CRY
│   ├── RunAction.cc               # Configuração do ntuple de saída
│   ├── EventAction.cc             # Rastreio do EventID por evento
│   ├── SteppingAction.cc          # Coleta de dados a cada passo
│   └── ActionInitialization.cc    # Registro das classes de ação
├── include/                   # Headers (.hh) correspondentes
├── main.cc                    # Ponto de entrada
├── CMakeLists.txt
├── macros/                    # Macros .mac (produção, visualização)
├── analysis/                  # Scripts Python de processamento e gráficos
│   ├── unificar_csv.py            # Unifica os CSVs gerados por thread
│   ├── analise_pareada_muons.py   # Pareamento por múon, métricas de atenuação
│   └── grafico_banner.py          # Geração das figuras finais
└── README.md
```

> **Nota:** ajuste os nomes de pasta acima para refletir a estrutura real do seu repositório, caso divirjam deste layout de referência.

## Compilação

```bash
git clone https://github.com/Djei365/muon-detection-simulation.git
cd muon-detection-simulation
mkdir build && cd build
cmake ..
make -j$(nproc)
```

Antes de compilar, ajuste o caminho local da instalação do CRY em `PrimaryGeneratorAction.cc` (variável `dataPath`), apontando para o diretório `data/` da sua instalação do CRY.

## Execução

```bash
# Modo interativo (visualização)
./muonSim

# Modo batch, a partir de uma macro de produção
./muonSim macros/producao.mac
```

A simulação exporta os dados em formato CSV (um arquivo por *thread*, no modo multithreaded), com as seguintes colunas:

| Coluna | Tipo | Descrição |
|---|---|---|
| `Altura_Z` | double | Posição vertical (m) do evento registrado |
| `Valor` | double | Grandeza física — momento (GeV) ou energia depositada (MeV), conforme `Tipo` |
| `Tipo` | double | `0` = morte da partícula; `1` = deposição de energia na laje; `2` = entrada na estrutura (referência) |
| `Angulo` | double | Ângulo polar da direção do momento (radianos, convenção nativa do GEANT4 — ver observação abaixo) |
| `EventID` | int | Identificador do evento GEANT4 |
| `TrackID` | int | Identificador da trilha dentro do evento |

**Observação sobre o ângulo:** o ângulo nativo do GEANT4 é medido a partir do eixo +z; como os múons se propagam predominantemente para baixo, o ângulo zenital físico (0° = vertical, 90° = horizontal) é obtido por `theta_zenital = 180 - theta_geant4`, conversão já aplicada nos scripts de análise.

## Análise de dados

```bash
cd analysis

# 1. Unifica os CSVs gerados pelas threads de execução
python3 unificar_csv.py

# 2. Executa o pareamento de trajetórias e gera as métricas de atenuação
python3 analise_pareada_muons.py --dados dados.csv --outdir figuras_pareado/

# 3. Gera as figuras finais (formatação para banner/artigo)
python3 grafico_banner.py --dados dados.csv --outdir figuras_banner/
```

## Status e próximos passos

Este repositório está em desenvolvimento ativo e será atualizado conforme os próximos aprimoramentos do projeto, incluindo:
- Refinamento geométrico da estrutura simulada a partir do projeto estrutural oficial da edificação, quando disponível;
- Ampliação do volume de eventos simulados, com foco em regiões de alta energia e ângulo zenital elevado;
- Validação experimental por comparação com medições de detectores de múons a serem instalados no campus.

## Citação

Se utilizar este código ou os resultados associados, por favor cite:

```
WALDOV, D. E.; LIMA, L. Simulações de Raios Cósmicos Utilizando GEANT4.
Universidade Tecnológica Federal do Paraná (UTFPR), campus Toledo, 2026.
```

## Agradecimentos

Desenvolvido com apoio da Fundação Araucária (bolsa de Iniciação Científica) e da Universidade Tecnológica Federal do Paraná (UTFPR).
