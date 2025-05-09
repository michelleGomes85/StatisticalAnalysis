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
    Classifica automaticamente o tipo da variável
    Retorna: 'Quantitativa contínua', 'Quantitativa discreta', 
             'Qualitativa nominal' ou 'Qualitativa ordinal'
    """

    is_numeric = pd.api.types.is_numeric_dtype(col_data)
    n_unique = col_data.nunique()
    
    if is_numeric:
        return "Quantitativa Contínua" if n_unique > 10 else "Quantitativa Discreta"
    
        # Lista de palavras-chave indicativas de ordem
    ordinal_keywords = ["nível", "grau", "satisfação", "avaliação", "classificação", "etapa"]

    # Conjunto de categorias com ordem conhecida (exemplo geral)
    known_ordinal_values = {
        "nível_de_satisfação": ["Insatisfeito", "Neutro", "Satisfeito"],
        "avaliação_final (0-10)": None  # se categorizada por faixas, poderia ser ordinal
    }

    # Verifica por nome da coluna
    if any(word in col_name.lower() for word in ordinal_keywords):
        return "Qualitativa Ordinal"
    
    # Verifica por valores típicos de ordem
    unique_vals = [str(val).lower() for val in col_data.unique()]
    if any(val in ["baixo", "médio", "alto", "insatisfeito", "neutro", "satisfeito"] for val in unique_vals):
        return "Qualitativa Ordinal"

    return "Qualitativa Nominal"

def calculate_frequencies(col_data, var_type):
    """
    Calcula tabela de frequências conforme o tipo de variável.

    Retorna: 
    - DataFrame com frequências absolutas, relativas e acumuladas
    - Categorias (intervalos) usadas (para variáveis quantitativas)
    - Rótulos formatados das categorias (presentes no índice da tabela)
    - Dados brutos ou categorizados (para plotagem)
    - Nome do eixo x (para plotagem)
    """
    categorias = None
    formatted_labels = None
    plot_data = None
    x_label = None
    
    if var_type.startswith("Quantitativa"):
        bins = calculate_optimal_bins(col_data)
        
        categorias = pd.cut(
            col_data,
            bins=bins,
            right=False,  # fechado à esquerda, aberto à direita
            include_lowest=True
        )
        
        freq = categorias.value_counts().sort_index()
        formatted_labels = [format_interval(interval) for interval in freq.index]
        freq.index = formatted_labels
        
        # Para plotagem
        plot_data = col_data  # Dados brutos para histograma
        x_label = "Valores"
    else:
        freq = col_data.value_counts().sort_index()
        formatted_labels = freq.index.astype(str).tolist()
        
        # Para plotagem
        plot_data = col_data.astype(str)  # Dados categóricos
        x_label = "Categorias"

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

    return {
        'freq_table': freq_table,
        'categories': categorias,
        'formatted_labels': formatted_labels,
        'plot_data': plot_data,
        'x_label': x_label,
        'var_type': var_type
    }

def calculate_optimal_bins(col_data):
    n = len(col_data)
    k = round(math.sqrt(n))

    min_val = float(col_data.min())
    max_val = float(col_data.max())

    amplitude_total = max_val - min_val
    intervalo = amplitude_total / k

    bins = [min_val + i * intervalo for i in range(k + 1)]
    bins[-1] = max_val + 1e-6  # garante inclusão do último valor

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