import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Monitoramento de Dados", layout="wide")
st.title("📊 Monitoramento dos Dados")

uploaded_file = st.file_uploader("Selecione o arquivo Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df = df.reset_index(drop=True)
    total = len(df)

    st.markdown("### 📌 Indicadores com Gráficos")

    # 1. Links preenchidos
    link_cols = [col for col in df.columns if "Link" in col]
    link_counts = {col: df[col].notna().sum() for col in link_cols}

    values1 = list(link_counts.values())
    fig1, ax1 = plt.subplots(figsize=(6, 3))
    bars1 = ax1.bar(link_counts.keys(), values1)
    ax1.set_xticklabels(link_counts.keys(), rotation=45, ha='right')
    ax1.set_yticks([])
    ax1.bar_label(bars1, padding=3)
    ax1.set_ylim(0, max(values1) * 1.2)
    ax1.set_title("Links Preenchidos")


    # 2. Luminária e Lâmpada
    qtd_luminaria = df["Tipo de Luminária"].notna().sum() if "Tipo de Luminária" in df else 0
    qtd_lampada = df["Tipo de Lâmpada"].notna().sum() if "Tipo de Lâmpada" in df else 0

    values2 = [qtd_luminaria, qtd_lampada]
    fig2, ax2 = plt.subplots(figsize=(6, 3))
    bars2 = ax2.bar(["Luminária", "Lâmpada"], values2)
    ax2.set_yticks([])
    ax2.bar_label(bars2, padding=3)
    ax2.set_ylim(0, max(values2) * 1.2)
    ax2.set_title("Itens com Luminária e Lâmpada")


    # 3. Transformador, Potência, Estrutura
    col_trafos = df["Ponto tem trafo?"].astype(str).str.lower().str.strip()
    qtd_transformador = col_trafos.isin(["sim"]).sum()

    qtd_potencia = df["Potência (Trafo)"]
    qtd_potencia = pd.to_numeric(qtd_potencia, errors='coerce')  # converte texto p/ número
    qtd_potencia = qtd_potencia[qtd_potencia > 0].count()

    qtd_montagem = df["Montagem (Trafo)"].notna().sum() if "Montagem (Trafo)" in df else 0

    values3 = [qtd_transformador, qtd_potencia, qtd_montagem]
    fig3, ax3 = plt.subplots(figsize=(6, 3))
    bars3 = ax3.bar(["Ponto tem Trafo", "Potência", "Montagem"], values3)
    ax3.set_yticks([])
    ax3.bar_label(bars3, padding=3)
    ax3.set_ylim(0, max(values3) * 1.2)
    ax3.set_title("Transformadores e Detalhes")

 
    # 4. Card TELECOM
    col_telecom = df["Tem Telecom?"].astype(str).str.lower().str.strip()    
    qtd_telecom = col_trafos.isin(["sim"]).sum()     

    # 4. Tipo de Lâmpada
    fig4, ax4 = plt.subplots(figsize=(6, 3))
    if "Tipo de Lâmpada" in df:
        counts_lamp = df["Tipo de Lâmpada"].value_counts()
        values4 = counts_lamp.values
        bars4 = ax4.bar(counts_lamp.index.astype(str), values4)
        ax4.set_yticks([])
        ax4.bar_label(bars4, padding=3)
        ax4.set_ylim(0, max(values4) * 1.2)
        ax4.set_title("Distribuição por Tipo de Lâmpada")
        ax4.set_xticklabels(counts_lamp.index.astype(str), rotation=45, ha='right')
 
    # 5. Tipo do Braço
    fig5, ax5 = plt.subplots(figsize=(6, 3))
    if "Tipo do Braço" in df:
        counts_braco = df["Tipo do Braço"].value_counts()
        values5 = counts_braco.values
        bars5 = ax5.bar(counts_braco.index.astype(str), values5)
        ax5.set_yticks([])
        ax5.bar_label(bars5, padding=3)
        ax5.set_ylim(0, max(values5) * 1.2)
        ax5.set_title("Distribuição por Tipo do Braço")
        ax5.set_xticklabels(counts_braco.index.astype(str), rotation=45, ha='right')

    # 6. Mínimo e Máximo de Lâmpadas por Tipo do Braço
    fig6 = None

    if "Tipo do Braço" in df and "Quantidade de Lâmpadas" in df:
        df["Quantidade de Lâmpadas"] = pd.to_numeric(df["Quantidade de Lâmpadas"], errors='coerce')

        # Filtra dados válidos
        base = df.dropna(subset=["Tipo do Braço", "Quantidade de Lâmpadas"])[["Tipo do Braço", "Quantidade de Lâmpadas"]]

        # Remove duplicatas para cada combinação
        base = base.drop_duplicates()

        # Calcula extremos por grupo
        extremos = base.groupby("Tipo do Braço")["Quantidade de Lâmpadas"].agg(['min', 'max']).reset_index()

        #st.write("📊 Extremos calculados:", extremos)

        if not extremos.empty:
            fig6, ax6 = plt.subplots(figsize=(6, 3))
            width = 0.4
            x = range(len(extremos))

            ax6.bar([i - width/2 for i in x], extremos['min'], width=width, label='Mínimo')
            ax6.bar([i + width/2 for i in x], extremos['max'], width=width, label='Máximo')
            ax6.set_xticks(x)
            ax6.set_xticklabels(extremos["Tipo do Braço"], rotation=45, ha="right")
            ax6.set_yticks([])
            ax6.set_ylim(0, max(extremos['max']) * 1.2)
            ax6.set_title("Mínimo e Máximo de Lâmpadas por Tipo do Braço")
            ax6.legend()

            for i, val in enumerate(extremos['min']):
                ax6.text(i - width/2, val + 0.1, str(val), ha='center', va='bottom')
            for i, val in enumerate(extremos['max']):
                ax6.text(i + width/2, val + 0.1, str(val), ha='center', va='bottom')
        else:
            st.warning("❕ Nenhum dado suficiente para gerar o gráfico de mínimo e máximo.")
    else:
        st.warning("❕ Colunas 'Tipo do Braço' e/ou 'Quantidade de Lâmpadas' não estão presentes.")

    
    col1, col2, col3 = st.columns([1,1,2])
    
    with col1: st.metric(" Total de itens", len(df))

    with col2: st.metric("📡 Itens com TELECOM", qtd_telecom)

    # Exibir os gráficos em colunas 2x3
    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(fig1)
        st.pyplot(fig3)
        if fig5:
            st.pyplot(fig5)        
    with col2:
        st.pyplot(fig2)
        if fig4:
            st.pyplot(fig4)  
        if fig6:
            st.pyplot(fig6)                  