import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np
# Importação necessária para gráficos 3D
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import LinearLocator

# --- CONFIGURAÇÕES ---
CSV_FILE = "resultados.csv"
ANALYSIS_DIR = "analise_definitiva" # Novo diretório para a versão final

def create_dir_and_set_theme():
    """Cria o diretório de saída e define o tema visual dos gráficos."""
    os.makedirs(ANALYSIS_DIR, exist_ok=True)
    sns.set_theme(style="whitegrid", palette="deep", font_scale=1.1)
    print(f"Salvando todos os gráficos na pasta: '{ANALYSIS_DIR}'")

def save_plot(fig, filename, tight=True):
    """Função auxiliar para salvar e fechar figuras."""
    if tight:
        plt.tight_layout()
    path = os.path.join(ANALYSIS_DIR, filename)
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f" -> Gráfico salvo: {filename}")

# --- NOVOS GRÁFICOS 3D ---

def plot_3d_surface(df, value_col, agent_col, title, filename):
    """NOVO: Gera um gráfico de superfície 3D para Custo vs. Cidades e Agentes."""
    print(f"Gerando gráfico 3D: {title}...")
    try:
        # Cria a tabela pivot para obter a grade de dados
        pivot_table = df.pivot_table(values=value_col, index=agent_col, columns='NumCidades', aggfunc=np.mean)
        
        # Prepara os eixos X, Y, Z para o plot 3D
        X = pivot_table.columns.values
        Y = pivot_table.index.values
        X, Y = np.meshgrid(X, Y)
        Z = pivot_table.values

        # Cria a figura e o eixo 3D
        fig = plt.figure(figsize=(16, 12))
        ax = fig.add_subplot(111, projection='3d')

        # Plota a superfície
        surf = ax.plot_surface(X, Y, Z, cmap='viridis_r', edgecolor='none', antialiased=False)
        
        # Configurações do gráfico
        ax.set_title(title, fontsize=18, pad=20)
        ax.set_xlabel('Número de Cidades', fontsize=12, labelpad=10)
        ax.set_ylabel(f'Número de {agent_col.replace("Num", "")}', fontsize=12, labelpad=10)
        ax.set_zlabel('Custo Médio da Solução', fontsize=12, labelpad=10)
        
        # Adiciona uma barra de cores para mapear valores para cores
        fig.colorbar(surf, shrink=0.5, aspect=10, pad=0.1)
        
        # Melhora a visualização
        ax.view_init(elev=20, azim=-120) # Ajusta o ângulo da câmera
        ax.zaxis.set_major_locator(LinearLocator(10)) # Formata os ticks do eixo Z
        ax.zaxis.set_major_formatter('{x:.02f}')

        save_plot(fig, filename, tight=False) # tight_layout não funciona bem com 3D

    except Exception as e:
        print(f"  -> Não foi possível gerar o gráfico 3D: {e}")


# --- GRÁFICOS ANTERIORES (COM CORREÇÕES) ---

def plot_performance_difference(df):
    """Gráfico de barras da diferença de custo (com correção de warning)."""
    df['DiferencaCusto'] = df['CustoACO'] - df['CustoABC']
    avg_diff = df.groupby('NumCidades')['DiferencaCusto'].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(12, 7))
    # CORREÇÃO: Atribuir 'x' ao 'hue' para evitar o warning
    sns.barplot(data=avg_diff, x='NumCidades', y='DiferencaCusto', hue='NumCidades', palette=['red' if x < 0 else 'blue' for x in avg_diff['DiferencaCusto']], legend=False, ax=ax)
    
    ax.axhline(0, color='black', linewidth=0.8, linestyle='--')
    ax.set_title('Diferença de Desempenho (Custo Médio ACO - Custo Médio ABC)', fontsize=16)
    ax.set_xlabel('Número de Cidades', fontsize=12)
    ax.set_ylabel('Negativo = ACO Melhor | Positivo = ABC Melhor', fontsize=12)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
    save_plot(fig, "7_diferenca_desempenho.png")

# ... (O restante das funções de plotagem anteriores podem ser coladas aqui sem alterações) ...
# Para manter a resposta concisa, vou omitir as funções que não mudaram.
# Copie as funções plot_total_time_summary, plot_custo_vs_cidades, etc., do script anterior para cá.
def plot_total_time_summary(df):
    fig, ax = plt.subplots(figsize=(8, 6))
    total_time_abc = df['TempoABC'].sum()
    total_time_aco = df['TempoACO'].sum()
    times = {'ABC': total_time_abc / 3600, 'ACO': total_time_aco / 3600}
    sns.barplot(x=list(times.keys()), y=list(times.values()), ax=ax)
    ax.set_title('Esforço Computacional Total', fontsize=16)
    ax.set_ylabel('Tempo Total de Execução (horas)', fontsize=12)
    save_plot(fig, "0_tempo_total_geral.png")

def plot_custo_vs_cidades(df):
    fig, ax = plt.subplots(figsize=(12, 7))
    avg_by_city = df.groupby('NumCidades')[['CustoABC', 'CustoACO']].mean().reset_index()
    sns.lineplot(data=avg_by_city, x='NumCidades', y='CustoABC', marker='o', label='ABC (Custo Médio)', ax=ax)
    sns.lineplot(data=avg_by_city, x='NumCidades', y='CustoACO', marker='o', label='ACO (Custo Médio)', ax=ax)
    ax.set_title('Custo Médio da Solução vs. Número de Cidades', fontsize=16)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    save_plot(fig, "1_custo_medio_vs_cidades.png")

def plot_tempo_vs_cidades(df):
    fig, ax = plt.subplots(figsize=(12, 7))
    avg_by_city = df.groupby('NumCidades')[['TempoABC', 'TempoACO']].mean().reset_index()
    sns.lineplot(data=avg_by_city, x='NumCidades', y='TempoABC', marker='o', label='ABC (Tempo Médio)', ax=ax)
    sns.lineplot(data=avg_by_city, x='NumCidades', y='TempoACO', marker='o', label='ACO (Tempo Médio)', ax=ax)
    ax.set_title('Tempo de Execução Médio vs. Número de Cidades', fontsize=16)
    ax.set_yscale('log')
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    save_plot(fig, "2_tempo_medio_vs_cidades.png")

def plot_heatmap(df, value_col, agent_col, title, filename):
    try:
        fig, ax = plt.subplots(figsize=(14, 8))
        pivot_table = df.pivot_table(values=value_col, index=agent_col, columns='NumCidades', aggfunc=np.mean)
        sns.heatmap(pivot_table, annot=True, fmt=".2f", cmap="viridis_r", linewidths=.5, ax=ax)
        ax.set_title(title, fontsize=16)
        save_plot(fig, filename)
    except Exception as e:
        print(f"  -> Não foi possível gerar o heatmap: {e}")

def plot_cost_vs_time_scatter(df):
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.scatterplot(data=df, x='TempoABC', y='CustoABC', alpha=0.6, label='ABC', ax=ax)
    sns.scatterplot(data=df, x='TempoACO', y='CustoACO', alpha=0.6, label='ACO', ax=ax)
    ax.set_title('Custo da Solução vs. Tempo de Execução', fontsize=16)
    ax.set_xlabel('Tempo de Execução (s)', fontsize=12)
    ax.set_ylabel('Custo da Solução Encontrada', fontsize=12)
    ax.set_xscale('log')
    ax.legend()
    save_plot(fig, "6_scatter_custo_vs_tempo.png")

def plot_efficiency(df):
    fig, ax = plt.subplots(figsize=(12, 7))
    df['EficienciaABC'] = df['CustoABC'] / (df['TempoABC'] + 1e-6)
    df['EficienciaACO'] = df['CustoACO'] / (df['TempoACO'] + 1e-6)
    avg_efficiency = df.groupby('NumCidades')[['EficienciaABC', 'EficienciaACO']].mean().reset_index()
    sns.lineplot(data=avg_efficiency, x='NumCidades', y='EficienciaABC', marker='o', label='ABC (Eficiência Média)', ax=ax)
    sns.lineplot(data=avg_efficiency, x='NumCidades', y='EficienciaACO', marker='o', label='ACO (Eficiência Média)', ax=ax)
    ax.set_title('Eficiência do Algoritmo (Custo / Segundo)', fontsize=16)
    ax.set_xlabel('Número de Cidades', fontsize=12)
    ax.set_ylabel('Custo por Segundo (Menor é Melhor)', fontsize=12)
    ax.legend()
    save_plot(fig, "8_eficiencia_custo_por_segundo.png")

def plot_cost_distribution_violin(df):
    fig, ax = plt.subplots(figsize=(16, 9))
    df_abc = df[['NumCidades', 'CustoABC']].copy(); df_abc.rename(columns={'CustoABC': 'Custo'}, inplace=True); df_abc['Algoritmo'] = 'ABC'
    df_aco = df[['NumCidades', 'CustoACO']].copy(); df_aco.rename(columns={'CustoACO': 'Custo'}, inplace=True); df_aco['Algoritmo'] = 'ACO'
    df_long = pd.concat([df_abc, df_aco])
    sns.violinplot(data=df_long, x='NumCidades', y='Custo', hue='Algoritmo', split=True, inner='quart', palette={'ABC': 'blue', 'ACO': 'red'}, ax=ax)
    ax.set_title('Distribuição dos Custos Encontrados por Tamanho do Problema', fontsize=16)
    ax.set_xlabel('Número de Cidades', fontsize=12)
    ax.set_ylabel('Custo da Solução', fontsize=12)
    ax.legend(title='Algoritmo')
    save_plot(fig, "9_distribuicao_custos_violino.png")


def main():
    """Função principal que orquestra a geração de todos os gráficos."""
    if not os.path.exists(CSV_FILE):
        print(f"ERRO: Arquivo '{CSV_FILE}' não encontrado. Execute o script de testes primeiro.")
        return

    create_dir_and_set_theme()
    df = pd.read_csv(CSV_FILE)

    # --- Geração dos Gráficos ---
    plot_total_time_summary(df)
    plot_custo_vs_cidades(df)
    plot_tempo_vs_cidades(df)
    plot_heatmap(df, 'CustoABC', 'NumAbelhas', 'ABC: Custo vs. Cidades e Abelhas', '3_heatmap_custo_abc.png')
    plot_heatmap(df, 'CustoACO', 'NumFormigas', 'ACO: Custo vs. Cidades e Formigas', '4_heatmap_custo_aco.png')
    plot_cost_vs_time_scatter(df)
    plot_performance_difference(df)
    plot_efficiency(df)
    plot_cost_distribution_violin(df)
    
    # --- Chamada para os novos gráficos 3D ---
    plot_3d_surface(df, 'CustoABC', 'NumAbelhas', 'ABC: Superfície de Custo (Cidades vs. Abelhas)', '10_superficie_3d_abc.png')
    plot_3d_surface(df, 'CustoACO', 'NumFormigas', 'ACO: Superfície de Custo (Cidades vs. Formigas)', '11_superficie_3d_aco.png')
    
    print("\nAnálise definitiva concluída com sucesso!")

if __name__ == "__main__":
    main()
