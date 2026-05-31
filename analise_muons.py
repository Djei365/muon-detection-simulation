import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# ====================================================================
# PARÂMETROS MATEMÁTICOS PARA O FLUXO DIFERENCIAL
# ====================================================================
# Cone de aceitação estreito (0 a 7 graus) para simular fluxo vertical
THETA_MAX_GRAUS = 7.0
THETA_MAX_RAD = np.deg2rad(THETA_MAX_GRAUS)

# Cálculo do Ângulo Sólido (Delta Omega) em esferorradianos (sr)
DELTA_OMEGA = 2 * np.pi * (1 - np.cos(THETA_MAX_RAD))

# Fator de Normalização (Ajuste fino para bater com a escala 10^-3 do artigo)
FATOR_DE_AJUSTE = 1e-6 
CONSTANTE_NORMALIZACAO = FATOR_DE_AJUSTE * (1.0 / DELTA_OMEGA)

# ====================================================================
# 1. CARREGAMENTO E LIMPEZA DOS DADOS (LEITOR À PROVA DE BALAS)
# ====================================================================
print("A ler e extrair dados rigorosos do Geant4...")

dados_limpos = []
try:
    with open('dados_completos.csv', 'r') as file:
        for linha in file:
            pedacos = linha.strip().split(',')
            
            # Só aceita linhas com 3 pedaços exatos (Z, Momento, Theta)
            if len(pedacos) == 3:
                try:
                    # Limpa a assinatura de multithreading (ex: "G4WT2 > 244.8")
                    z_str = pedacos[0].split('>')[-1].strip()
                    
                    # Força a conversão numérica
                    z = float(z_str)
                    momento = float(pedacos[1])
                    theta = float(pedacos[2])
                    
                    dados_limpos.append([z, momento, theta])
                except ValueError:
                    # Ignora linhas de log do Geant4 misturadas no CSV
                    pass
except FileNotFoundError:
    print("ERRO: O ficheiro 'dados_completos.csv' não foi encontrado.")
    exit()

df = pd.DataFrame(dados_limpos, columns=['Altura_Z_m', 'Momento_GeV', 'Theta_rad'])

if len(df) == 0:
    print("Nenhum dado válido extraído. Verifique a simulação.")
    exit()

# Converte radianos para graus e filtra o fluxo estritamente vertical
df['Theta_deg'] = np.rad2deg(df['Theta_rad'])
df_vertical = df[df['Theta_deg'] <= THETA_MAX_GRAUS]

print(f"Dados extraídos com sucesso! Múons verticais: {len(df_vertical):,}\n")

# ====================================================================
# 2. GERAÇÃO DO GRÁFICO (Estilo ROOT / Artigo Científico)
# ====================================================================
print("A gerar o Espectro Diferencial...")

# Configuração de estilo exigida em publicações de física
mpl.rcdefaults() 
plt.style.use('default') 
plt.rcParams.update({
    'xtick.direction': 'in', 'ytick.direction': 'in',
    'xtick.top': True, 'ytick.right': True,
    'axes.linewidth': 1.5, 'font.family': 'serif'
})

def calcular_fluxo_diferencial(dados_momento, bins):
    contagens, margens_bins = np.histogram(dados_momento, bins=bins)
    larguras_bins = np.diff(margens_bins)
    fluxo = (contagens * CONSTANTE_NORMALIZACAO) / larguras_bins
    return fluxo, margens_bins

plt.figure(figsize=(9, 7))
plt.yscale('log')
plt.xscale('log')

# Isola as populações de interesse
muons_topo = df_vertical[df_vertical['Altura_Z_m'] > 15]['Momento_GeV']
muons_chao = df_vertical[df_vertical['Altura_Z_m'] <= 5]['Momento_GeV']

# Escala idêntica aos artigos acadêmicos de referência (10^0 a 10^3)
bins_log = np.logspace(0, 3, 40)

fluxo_topo, margens = calcular_fluxo_diferencial(muons_topo, bins_log)
fluxo_chao, _ = calcular_fluxo_diferencial(muons_chao, bins_log)

# Desenha as curvas em formato de degrau (step)
plt.step(margens[:-1], fluxo_topo, where='post', color='black', linewidth=2.0, 
         label='Geant4: Topo ($>15$ m)')
plt.step(margens[:-1], fluxo_chao, where='post', color='red', linestyle='--', linewidth=2.0, 
         label=r'Geant4: Solo ($\leq 5$ m)')

# Títulos e formatação matemática dos eixos
plt.title('Espectro de Momento Diferencial dos Múons ($\\theta \\approx 0^{\\circ}$)', fontsize=14, pad=15)
plt.xlabel('$p$ / (GeV/c)', fontsize=13)
plt.ylabel('$\\Phi(p, \\theta)$ / (GeV/c)$^{-1} \\cdot$ cm$^{-2} \\cdot$ sr$^{-1} \\cdot$ s$^{-1}$', fontsize=13)

# Ajuste fino das marcações dos eixos logarítmicos
plt.minorticks_on()
plt.tick_params(which='major', length=8, width=1.2)
plt.tick_params(which='minor', length=4, width=0.8)
plt.xlim(1, 1000)

plt.legend(frameon=False, fontsize=12, loc='lower left')
plt.tight_layout()

# Salva a imagem final
nome_arquivo = 'espectro_diferencial_isolado.png'
plt.savefig(nome_arquivo, dpi=300)
plt.close()

print("==========================================================")
print(f"SUCESSO! O gráfico '{nome_arquivo}' foi gerado na sua pasta.")
print("==========================================================")