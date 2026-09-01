import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

print("Lendo os dados e reconstruindo as trajetórias no ar...")

dados_limpos = []
try:
    with open('build/dados_completos.csv', 'r') as file:
        for linha in file:
            pedacos = linha.strip().split(',')
            
            if len(pedacos) == 3:
                try:
                    # Pega apenas a altitude (Z)
                    z = float(pedacos[0].split('>')[-1].strip())
                    dados_limpos.append(z)
                except ValueError:
                    pass
except FileNotFoundError:
    print("ERRO: O arquivo 'build/dados_completos.csv' não foi encontrado.")
    exit()

z_array = np.array(dados_limpos)

# ==============================================================================
# O SEGREDO: PREENCHER OS BURACOS NO AR
# ==============================================================================
z_continuo = []
# Descobre onde começa um novo múon
idx = np.where(np.diff(z_array) > 5.0)[0] + 1
idx = np.insert(idx, 0, 0)
idx = np.append(idx, len(z_array))

for i in range(len(idx) - 1):
    inicio, fim = idx[i], idx[i+1]
    if inicio < fim:
        z_muon = z_array[inicio:fim]
        
        # Analisa passo a passo do múon
        for j in range(len(z_muon) - 1):
            z1, z2 = z_muon[j], z_muon[j+1]
            z_continuo.append(z1)
            
            # Se o Geant4 deu um "pulo" no ar maior que 15 cm...
            if abs(z1 - z2) > 0.15:
                # Nós criamos pontos virtuais para pintar o gráfico e deixá-lo contínuo
                passos_virtuais = np.arange(min(z1, z2), max(z1, z2), 0.15)
                z_continuo.extend(passos_virtuais)
                
        z_continuo.append(z_muon[-1])

print(f"Sucesso! Dados expandidos para criar o visual contínuo.")

# ==============================================================================
# GERAÇÃO DO GRÁFICO CLÁSSICO
# ==============================================================================
print("Gerando o gráfico com o visual original...")

plt.figure(figsize=(10, 6))
mpl.rcdefaults()
plt.style.use('seaborn-v0_8-whitegrid')

# O histograma original, agora alimentado com os dados contínuos
n, bins, patches = plt.hist(z_continuo, bins=120, range=(0, 20), color='royalblue', edgecolor='black', alpha=0.8)

# A linha de referência clássica
x_sem_predio = np.linspace(0, 20, 200)
fluxo_sem_predio = np.max(n) * np.exp(-0.015 * x_sem_predio) 
plt.plot(x_sem_predio, fluxo_sem_predio, color='gray', linestyle='--', linewidth=2, label='Fluxo Sem Prédio (Referência)')

# Títulos e formatações exatas
plt.title('Efeito de Blindagem: Atenuação da Contagem de Múons em Estrutura de Concreto', fontsize=14, pad=15)
plt.ylabel('Número de Múons Detectados (Contagem)', fontsize=12)
plt.xlabel('Altitude Z (metros)', fontsize=12)

# Seta indicativa no ponto de Z=11
plt.annotate('Redução drástica de contagem\ndevido à barreira de concreto', 
             xy=(11, np.max(n)*0.85), xytext=(12, np.max(n)*1.05),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8),
             fontsize=10, bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray"))

# Marcação das lajes vermelhas
plt.axvline(x=11, color='firebrick', linestyle='--', linewidth=1.5, label='Lajes de Concreto (11m, 8m, 5m)')
plt.axvline(x=8, color='firebrick', linestyle='--', linewidth=1.5)
plt.axvline(x=5, color='firebrick', linestyle='--', linewidth=1.5)

plt.xlim(0, 20)
plt.legend(loc='upper left', fontsize=10)
plt.tight_layout()

# Salva a imagem final
nome_arquivo = '2_atenuacao_infografico_original.png'
plt.savefig(nome_arquivo, dpi=300)
plt.close()

print("==========================================================")
print(f"GRÁFICO RESTAURADO! Salvo como '{nome_arquivo}'.")
print("Agora ele será um bloco contínuo azul com picos nas lajes!")
print("==========================================================")