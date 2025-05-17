import pandas as pd
import numpy as np
from scipy import stats
import math
import statistics

# ==============================================
# CLASSIFICAÇÃO E CATEGORIZAÇÃO
# ==============================================

def classify_variable(col_data):
    """
    Classifica automaticamente o tipo da variável:
    - Quantitativa Contínua
    - Quantitativa Discreta
    - Qualitativa Ordinal
    - Qualitativa Nominal
    """
    col_data = col_data.dropna()
    n_unique = col_data.nunique()
    
    # Verifica se é numérica
    is_numeric = pd.api.types.is_numeric_dtype(col_data)

    if is_numeric:
        # Converte para numpy array
        values = col_data.to_numpy()

        # Verifica se todos os valores são inteiros (mesmo que estejam como float)
        all_integers = np.all(np.equal(np.mod(values, 1), 0))

        if all_integers and n_unique < 30:
            return "Quantitativa Discreta"
        else:
            return "Quantitativa Contínua"

    # Valores ordinais conhecidos
    ordinal_values_set = {
        "Muito insatisfeito",
        "Insatisfeito",
        "Neutro",
        "Satisfeito",
        "Muito satisfeito"
    }

    # Verifica se contém valores ordinais
    if col_data.isin(ordinal_values_set).any():
        return "Qualitativa Ordinal"

    return "Qualitativa Nominal"

def calculate_frequencies(col_data, var_type):

    """
    Calcula tabela de frequências conforme o tipo de variável.

    Retorna:
    - freq_table: DataFrame com todas as frequências
    - categories: categorias (intervalos) usadas (para quantitativas)
    - formatted_bins: rótulos das categorias no formato "a | - b" (útil para exibição)
    - plot_data: dados brutos ou categóricos para uso na plotagem
    - x_label: nome do eixo x
    - bins: lista com os limites dos intervalos calculados (ex: [10, 15, 20])
    """

    # Inicializa variáveis gerais
    categories = None
    formatted_bins = [] 
    plot_data = None
    x_label = None
    bins = []           

    # -------------------------------
    # LÓGICA PARA VARIÁVEIS QUANTITATIVAS
    # -------------------------------
    if var_type.startswith("Quantitativa"):
        # Calcula os bins automaticamente
        bins = calculate_optimal_bins(col_data, var_type)

        # Cria categorias com pd.cut
        categories = pd.cut(
            col_data,
            bins=bins,
            right=False,  # fechado à esquerda, aberto à direita
            include_lowest=True
        )

        # Frequência por classe
        freq = categories.value_counts().sort_index()

        # Formata os intervalos como "a | - b"
        formatted_bins = [format_interval(interval) for interval in freq.index]

        # Aplica os rótulos formatados
        freq.index = formatted_bins  

        # Dados brutos para plotagem (histograma)
        plot_data = col_data
        x_label = "Valores"

    # -------------------------------
    # LÓGICA PARA VARIÁVEIS QUALITATIVAS
    # -------------------------------
    else:
        # Frequência simples das categorias
        freq = col_data.value_counts().sort_index()

        # Rótulos como strings (para exibição)
        formatted_bins = freq.index.astype(str).tolist()

        # Dados como string para consistência na plotagem
        plot_data = col_data.astype(str)
        x_label = "Categorias"

    # -------------------------------
    # CÁLCULOS DE FREQUÊNCIAS (valem para ambos os tipos)
    # -------------------------------
    total = freq.sum()
    rel_freq = (freq / total).round(4)
    rel_freq_perc = (rel_freq * 100).round(2)
    cum_freq = freq.cumsum()
    cum_rel_freq_perc = (cum_freq / total * 100).round(2)

    freq_table = pd.DataFrame({
        'Frequência Absoluta': freq,
        'Frequência Relativa': rel_freq,
        'Frequência Relativa [%]': rel_freq_perc,
        'Frequência Acumulativa': cum_freq,
        'Frequência Acumulativa [%]': cum_rel_freq_perc
    })

    total_row = pd.DataFrame({
        'Frequência Absoluta': [total],
        'Frequência Relativa': [rel_freq.sum()],
        'Frequência Relativa [%]': [rel_freq_perc.sum()],
        'Frequência Acumulativa': [np.nan],
        'Frequência Acumulativa [%]': [np.nan]
    }, index=['Total'])

    freq_table = pd.concat([freq_table, total_row])

    # -------------------------------
    # RETORNO DA FUNÇÃO
    # -------------------------------
    print(freq_table)
    return {
        'freq_table': freq_table,
        'categories': categories,
        'formatted_bins': formatted_bins,
        'plot_data': plot_data,
        'x_label': x_label,
        'var_type': var_type,
        'bins': bins  
    }

def calculate_optimal_bins(col_data, var_type):

    n = len(col_data)
    k = round(math.sqrt(n))
    
    min_val = float(col_data.min())
    max_val = float(col_data.max())
    
    amplitude_total = max_val - min_val
    
    # Se a variável for discreta, ajustamos os bins para inteiros
    if var_type == "Quantitativa Discreta":

        min_val = int(min_val)
        max_val = int(max_val)
        amplitude_total = max_val - min_val
        intervalo = amplitude_total / k
        
        # Garantir que os bins sejam inteiros e cubram todo o intervalo
        bins = [min_val + int(i * intervalo) for i in range(k + 1)]

         # Inclui o último valor
        bins[-1] = max_val + 1 
    else:
        # Variável contínua (pode ter valores float)
        intervalo = amplitude_total / k
        bins = [min_val + i * intervalo for i in range(k + 1)]

        # Garante inclusão do último valor
        bins[-1] = max_val + 1e-6  
    
    return bins

def format_interval(interval):

    """Formata intervalo no estilo 'a.b | - b.c' com 2 casas decimais"""

    left = f"{interval.left:.2f}"
    right = f"{interval.right:.2f}"
    return f"{left} | - {right}"

# ==============================================
# ESTATÍSTICAS DESCRITIVAS
# ==============================================

def calculate_statistics(col_data):

    """
    Calcula estatísticas descritivas para variáveis quantitativas
    Retorna: Dicionário organizado para criação de tabela
    """
    stats_dict = {
        'Medidas de Posição': {
            'Média': statistics.mean(col_data),
            'Mediana': statistics.median(col_data),
            'Moda': statistics.mode(col_data),
            'Primeiro Quartil [Q1]': np.percentile(col_data, 25),
            'Terceiro Quartil [Q3]': np.percentile(col_data, 75)
        },
        
        'Medidas de Dispersão': {
            'Amplitude': np.ptp(col_data),
            'Variância': np.var(col_data, ddof=1),
            'Desvio Padrão': np.std(col_data, ddof=1),
            'Coeficiente de Variação (CV)': (np.std(col_data, ddof=1) / statistics.mean(col_data)) 
                                       if statistics.mean(col_data) != 0 else np.nan
        }
    }
    
    return stats_dict