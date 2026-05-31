cmake_minimum_required(VERSION 3.16)
project(MuonUTFPR)

# Localiza o Geant4
find_package(Geant4 REQUIRED ui_all vis_all)
include(${Geant4_USE_FILE})

# Caminho absoluto para a pasta que acabamos de baixar
set(CRY_DIR "/home/djei/cry_v1.7")

# Avisa o compilador onde ler os cabeçalhos (.h) do CRY
include_directories(${CRY_DIR}/src)

# Define os arquivos do seu projeto
set(SOURCES
    main.cpp
    DetectorConstruction.cpp
    PrimaryGeneratorAction.cpp
    ActionInitialization.cpp
    SteppingAction.cpp
    RunAction.cpp
    EventAction.cpp
)
# Cria o executável
add_executable(muonSim ${SOURCES})

# === ATENÇÃO: CONECTANDO AS DUAS BIBLIOTECAS ===
# Aqui nós juntamos o seu código (muonSim), o Geant4 e o arquivo compilado do CRY
target_link_libraries(muonSim ${Geant4_LIBRARIES} ${CRY_DIR}/lib/libCRY.a)


# ==========================================================
# COPIA OS ARQUIVOS .mac PARA A PASTA BUILD AUTOMATICAMENTE
# ==========================================================
file(GLOB MACRO_FILES "*.mac")
foreach(mac_file ${MACRO_FILES})
    file(COPY ${mac_file} DESTINATION ${PROJECT_BINARY_DIR})
endforeach()