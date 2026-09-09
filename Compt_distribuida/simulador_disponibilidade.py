import math
import random
import pandas as pd
import matplotlib.pyplot as plt

def calculo_analitico(n, k, p):
    """
    Calcula a disponibilidade analítica usando a distribuição binomial.
    Fórmula: Somatório de i=k até n de (n escolhe i) * p^i * (1-p)^(n-i)
    """
    disponibilidade = 0.0
    for i in range(k, n + 1):
        combinacoes = math.comb(n, i)
        probabilidade = combinacoes * (p ** i) * ((1 - p) ** (n - i))
        disponibilidade += probabilidade
    return disponibilidade

def simulador_estocastico(n, k, p, num_rodadas=10000):
    """
    Simula a disponibilidade usando uma abordagem estocástica (Monte Carlo).
    """
    rodadas_sucesso = 0
    for _ in range(num_rodadas):
        servidores_disponiveis = 0
        for _ in range(n):
            if random.random() <= p:
                servidores_disponiveis += 1
        
        if servidores_disponiveis >= k:
            rodadas_sucesso += 1
            
    return rodadas_sucesso / num_rodadas

def executar_experimentos():
    resultados = []
    
    # Parâmetros para testar
    n_valores = [4, 10]
    p_valores = [0.1, 0.3, 0.5, 0.7, 0.9, 0.95, 0.99]
    num_rodadas = 10000
    
    for n in n_valores:
        # Casos específicos para k: 1, n/2, n
        # Usando math.ceil para n/2 caso n seja ímpar, mas usarei 4 e 10 que são pares
        k_valores = [1, n // 2, n]
        
        for k in k_valores:
            for p in p_valores:
                disp_analitica = calculo_analitico(n, k, p)
                disp_simulada = simulador_estocastico(n, k, p, num_rodadas)
                
                resultados.append({
                    'N (Servidores)': n,
                    'K (Mínimo Necessário)': k,
                    'P (Prob. Disponibilidade)': p,
                    'Disponibilidade Analítica': disp_analitica,
                    'Disponibilidade Simulada': disp_simulada,
                    'Diferença Absoluta': abs(disp_analitica - disp_simulada)
                })
                
    df = pd.DataFrame(resultados)
    return df

def gerar_graficos(df):
    n_valores = df['N (Servidores)'].unique()
    
    for n in n_valores:
        df_n = df[df['N (Servidores)'] == n]
        
        plt.figure(figsize=(10, 6))
        
        k_valores = df_n['K (Mínimo Necessário)'].unique()
        marcadores = ['o', 's', '^']
        cores = ['blue', 'green', 'red']
        
        for i, k in enumerate(k_valores):
            df_k = df_n[df_n['K (Mínimo Necessário)'] == k]
            
            # Plotar valor Analítico (linha)
            plt.plot(df_k['P (Prob. Disponibilidade)'], df_k['Disponibilidade Analítica'], 
                     label=f'Analítica (k={k})', color=cores[i], linestyle='-')
            
            # Plotar valor Simulado (pontos dispersos)
            plt.scatter(df_k['P (Prob. Disponibilidade)'], df_k['Disponibilidade Simulada'], 
                        label=f'Simulada (k={k})', color=cores[i], marker=marcadores[i], s=50, alpha=0.7)
            
        plt.title(f'Disponibilidade do Serviço vs Probabilidade do Servidor (N={n})')
        plt.xlabel('Probabilidade de cada servidor estar disponível (p)')
        plt.ylabel('Disponibilidade do Serviço (A)')
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.7)
        
        caminho_grafico = f'c:/Users/Marina/Desktop/Compt_distribuida/grafico_disponibilidade_n{n}.png'
        plt.savefig(caminho_grafico)
        plt.close()

if __name__ == "__main__":
    print("Iniciando a execução dos cálculos e simulações...")
    df_resultados = executar_experimentos()
    
    # Salvar resultados em CSV
    caminho_csv = 'c:/Users/Marina/Desktop/Compt_distribuida/resultados_disponibilidade.csv'
    df_resultados.to_csv(caminho_csv, index=False)
    print(f"Tabela de resultados salva em: {caminho_csv}")
    
    # Gerar gráficos
    print("Gerando gráficos 2D...")
    gerar_graficos(df_resultados)
    print("Gráficos gerados e salvos com sucesso no diretório.")
    
    # Mostrar um resumo no console
    print("\nResumo dos resultados (Primeiras e últimas linhas):")
    print(df_resultados.head(10))
    print("...")
    print(df_resultados.tail(10))
