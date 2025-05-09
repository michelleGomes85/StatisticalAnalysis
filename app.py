import streamlit as st
import pandas as pd
from components import (
    inject_global_css,
    styled_header,
    styled_file_uploader,
    data_preview,
    create_analysis_tabs,
    plot_distribution,
    plot_statistical_details,
    styled_variable_type_selector
)

from utils import (
    classify_variable,
    calculate_frequencies,
    calculate_statistics
)

# ==============================================
# CONFIGURAÇÃO INICIAL
# ==============================================

def initialize_app():
    """Configurações iniciais da aplicação"""
    st.set_page_config(
        page_title="Análise Estatística",
        layout="wide",
        page_icon="📊",
        initial_sidebar_state="expanded"
    )
    
    # Aplica CSS global
    inject_global_css()
    
    # Exibe cabeçalho
    styled_header()

# ==============================================
# FLUXO PRINCIPAL
# ==============================================

def main():
    
    initialize_app()
    
    # Upload de dados
    uploaded_file = styled_file_uploader()
    
    if not uploaded_file:
        df = pd.read_csv("datas.csv", decimal=",")
    else:
        # Carrega e exibe dados
        df = pd.read_csv(uploaded_file, decimal=",")
        
    data_preview(df)
    
    # Seleção de variáveis
    st.sidebar.markdown("### Selecione as variáveis para análise:")
    selected_columns = [
        col for col in df.columns 
        if st.sidebar.checkbox(col, key=f"checkbox_{col}")
    ]
    
    # Análise para cada variável selecionada
    for col in selected_columns:

        st.markdown(f"---\n## Variável: `{col}`")
        col_data = df[col].dropna()
        
        # Classificação da variável
        var_type = styled_variable_type_selector(classify_variable(col_data), key=f"selectbox_{col}")
        
        # Abas de análise
        tab_freq, tab_viz, tab_stats = create_analysis_tabs()
        
        # Tab 1: Tabela de Frequência
        with tab_freq:
            freq_info = calculate_frequencies(col_data, var_type)
            st.write(freq_info['freq_table'])
        
        # Tab 2: Visualização Gráfica
        with tab_viz:
            plot_distribution(freq_info, col)
            if var_type.startswith("Quantitativa"):
                plot_statistical_details(col_data, col)
        
        # Tab 3: Análise Estatística
        with tab_stats:
            if var_type.startswith("Quantitativa"):
                show_statistical_analysis(col_data)
            else:
                st.warning("Análise estatística disponível apenas pra variáveis quantitativas")

# ==============================================
# FUNÇÕES AUXILIARES
# ==============================================

def show_statistical_analysis(col_data):
    """
    Exibe as estatísticas em tabelas simples no Streamlit com dados centralizados e cabeçalho colorido
    """
    stats = calculate_statistics(col_data)
    
    # Tabela de Medidas de Posição
    df_posicao = pd.DataFrame.from_dict(
        stats['Medidas de Posição'], 
        orient='index', 
        columns=['Valor']
    )
    df_posicao.index.name = 'Medidas de Posição'
    
    # Estilizando a tabela de Medidas de Posição
    df_posicao_styled = df_posicao.style.set_properties(**{'text-align': 'center'})
    st.dataframe(df_posicao_styled)
    
    # Tabela de Medidas de Dispersão
    df_dispersao = pd.DataFrame.from_dict(
        stats['Medidas de Dispersão'], 
        orient='index', 
        columns=['Valor']
    )
    df_dispersao.index.name = 'Medidas de Dispersão'
    
    # Estilizando a tabela de Medidas de Dispersão
    df_dispersao_styled = df_dispersao.style.set_properties(**{'text-align': 'center'})
    st.dataframe(df_dispersao_styled)

# ==============================================
# EXECUÇÃO
# ==============================================

if __name__ == "__main__":
    main()