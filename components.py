
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ==============================================
# CSS GLOBAL
# ==============================================

def inject_global_css():

    """Injeta CSS global na aplicação"""
    st.markdown("""
                
    <style>
                
    /* Estilos gerais */
                
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        line-height: 1.6;
        color: #c7ebff;
    }
                
    .st-emotion-cache-1yiq2ps {
        justify-content: center;
    }
                
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* Espaçamento entre componentes */
    .stMarkdown, .stDataFrame, .stPlotlyChart {
        margin-bottom: 1.5rem;
    }
    
    .st-emotion-cache-hkl0h9 {
        color: #c7ebff;
        background-color: #172d43;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
                
    .st-emotion-cache-83erdr {
        background-color: transparent;
        align-self: center;
    }
    
    .st-at {
        background-color: #262730;
    }
                
    div {
        border: none !important;
    }

    </style>
    """, unsafe_allow_html=True)

# ==============================================
# HEADER
# ==============================================
def styled_header():

    """Cabeçalho estilizado da aplicação"""

    st.markdown("""
                
    <style>
                
    .main-header {
        background-color: #262730;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
                
    .main-header h1 {
        color: rgb(199, 235, 255);
        text-align: center;
        margin: 0;
        font-size: 2rem;
    }
    </style>
                
    <div class="main-header">
        <h1>Painel Interativo de Análise Estatística</h1>
    </div>
    """, unsafe_allow_html=True)

# ==============================================
# ESCOLHER ARQUIVO
# ==============================================

def styled_file_uploader():

    """Uploader de arquivos estilizado"""

    st.markdown("""
    <style>
                
    .stFileUploader > div {
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        margin-top: 30px;
    }
                
    </style>
                
    """, unsafe_allow_html=True)

    return st.sidebar.file_uploader("Faça upload de um arquivo CSV", type="csv")

# ==============================================
# SELECT ESCOLHER O TIPO DE VARIAVEL
# ==============================================

def styled_variable_type_selector(default_value="Quantitativa Contínua", key=None):
    
    st.markdown("""
    <style>
    .stSelectbox {
        width: 30%;           
    }
    .stSelectbox label {
        font-weight: bold;
        color: #FFF;
        margin-bottom: 10px;
    }
    
    .stSelectbox p {
        font-size: 1.1rem !important;
        margin-bottom: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

    options = [
        "Qualitativa Nominal",
        "Qualitativa Ordinal",
        "Quantitativa Discreta",
        "Quantitativa Contínua"
    ]

    st.markdown('<div class="var-type-box-desc">Selecione abaixo o tipo da variável que deseja analisar. Essa escolha é importante para aplicar os gráficos e medidas estatísticas adequados.</div>', unsafe_allow_html=True)
    with st.container():
        var_type = st.selectbox(
            "Escolha o tipo da variável que será analisada",
            options=options,
            index=options.index(default_value),
            key=key
        )
    
    return var_type

# ==============================================
# COMPONENTES DE VISUALIZAÇÃO DE DADOS
# ==============================================

def data_preview(df):

    """Visualização dos dados com opção de ocultar"""

    st.markdown("""
                
    <style>
                
    /* Estilo para o DataFrame */
                
    .dataframe-container {
        border-radius: 8px;
        overflow: hidden;
    }

    </style>
                
    """, unsafe_allow_html=True)

    show_table = st.sidebar.checkbox("Mostrar tabela de dados", value=True, key='show_table')
    st.subheader("Tabela de Dados Importados")

    if show_table:
        with st.container():
            st.dataframe(df, height=300)
    else:
        st.info("Tabela ocultada. Marque a opção 'Mostrar tabela de dados' no sidebar para visualizar.")

# ==============================================
# COMPONENTES ABAS
# ==============================================

def create_analysis_tabs():

    """Cria abas para análise com estilo personalizado"""

    st.markdown("""
    <style>
                
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
                
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0 25px;
        background-color: #262730;
        border-radius: 8px 8px 0 0;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stTabs [aria-selected="true"] {
        background-color: #172d43;
        color: white;
    }
    </style>
                
    """, unsafe_allow_html=True)
    
    return st.tabs(["📋 Tabela de Frequência", "📈 Visualização", "📊 Análise Estatística"])


# ==============================================
# COMPONENTES GRÁFICOS
# ==============================================

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_distribution(plot_info, col_name):
    """
    Gera um gráfico de distribuição interativo com tema escuro.
    Para variáveis quantitativas, usa histograma com classes calculadas.
    
    Args:
        plot_info (dict): Dicionário contendo:
            - 'var_type': Tipo da variável (ex: "Qualitativa Nominal", "Quantitativa Contínua")
            - 'plot_data': Dados para plotagem (pd.Series)
            - 'freq_table': Tabela de frequências (para quantitativas)
            - 'bins': Intervalos dos bins (para quantitativas)
        col_name (str): Nome da coluna/variável
    """
    
    # =============================================
    # Configurações de estilo
    # =============================================
    container_style = """
    <style>
    .plot-container {
        border-radius: 8px;
        padding: 15px;
        background-color: #111111;
        box-shadow: 0 2px 4px rgba(255,255,255,0.1);
        color: white;
    }
    </style>
    """
    st.markdown(container_style, unsafe_allow_html=True)
    
    # =============================================
    # Variáveis Qualitativas
    # =============================================
    if plot_info['var_type'].startswith("Qualitativa"):
        df_counts = plot_info['plot_data'].value_counts().reset_index()
        df_counts.columns = [col_name, "Frequência"]
        
        fig = px.bar(
            df_counts,
            x=col_name,
            y="Frequência",
            title=f"Distribuição de {col_name}",
            color=col_name,
            color_discrete_sequence=px.colors.qualitative.Dark24,
            template='plotly_dark'
        )
        
        fig.update_layout(
            xaxis_title=col_name,
            yaxis_title="Contagem",
            showlegend=False
        )
        
    # =============================================
    # Variáveis Quantitativas
    # =============================================
    else:
        
        # Preparar dados
        frequencias = plot_info['freq_table']['Frequência Absoluta'].iloc[:-1].values
        bins = plot_info['bins']
        data = plot_info['plot_data']
        
        # Criar figura com subplots se for contínua
        if plot_info['var_type'].endswith("Contínua"):

            fig = make_subplots(
                rows=2, cols=1,
                shared_xaxes=True,
                vertical_spacing=0.05,
                row_heights=[0.7, 0.3]
            )
            
            # Adicionar histograma
            fig.add_trace(
                go.Bar(
                    x=[(bins[i] + bins[i+1])/2 for i in range(len(bins)-1)],
                    y=frequencias,
                    width=[bins[i+1] - bins[i] for i in range(len(bins)-1)],
                    marker_color='#636EFA',
                    marker_line_color='black',
                    marker_line_width=1,
                    opacity=0.8,
                    name='Frequência'
                ),
                row=1, col=1
            )
            
            # Adicionar boxplot
            fig.add_trace(
                go.Box(
                    x=data,
                    name='Distribuição',
                    marker_color='#00CC96',
                    boxpoints=False
                ),
                row=2, col=1
            )
            
            fig.update_layout(
                title=f"Distribuição de {col_name}",
                height=600
            )
            
        else:  # Discreta
            fig = go.Figure()
            fig.add_trace(
                go.Bar(
                    x=[(bins[i] + bins[i+1])/2 for i in range(len(bins)-1)],
                    y=frequencias,
                    width=[bins[i+1] - bins[i] for i in range(len(bins)-1)],
                    marker_color='#636EFA',
                    marker_line_color='black',
                    marker_line_width=1,
                    opacity=0.8,
                    name='Frequência'
                )
            )
            
            fig.update_layout(
                title=f"Distribuição de {col_name}",
                xaxis_title=col_name,
                yaxis_title="Frequência"
            )
    
    # =============================================
    # Configurações comuns e exibição
    # =============================================
    fig.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    with st.container():
        st.plotly_chart(fig, use_container_width=True)

def plot_statistical_details(col_data, col_name):

    """Boxplot para análise estatística"""

    fig = px.box(col_data, points="all", title=f"Detalhes Estatísticos - {col_name}")
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)