import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Comparativo de Arquivos", layout="wide")
st.title("🔍 Comparativo entre Arquivo Original e Final")

col1, col2 = st.columns(2)

with col1:
    original = st.file_uploader("Arquivo Original", type=["xlsx"], key="orig")

with col2:
    final = st.file_uploader("Arquivo Final", type=["xlsx"], key="final")

if original and final:
    df_orig = pd.read_excel(original)
    df_final = pd.read_excel(final)

    st.subheader("📈 Resumo de Alterações")

    # Garante alinhamento correto dos dados
    df_orig = df_orig.reset_index(drop=True)
    df_final = df_final.reset_index(drop=True)
    min_len = min(len(df_orig), len(df_final))
    df_orig = df_orig.loc[:min_len - 1]
    df_final = df_final.loc[:min_len - 1]

    # Detecta alterações por linha
    alteracoes_linha = (df_orig != df_final) & ~(df_orig.isna() & df_final.isna())
    linhas_alteradas = alteracoes_linha.any(axis=1).sum()

    # Mostra total de registros alterados com destaque
    st.markdown(f"### 🔄 Total de Registros Alterados: **{linhas_alteradas}**")


    common_cols = df_orig.columns.intersection(df_final.columns)
    diffs = {}

    for col in common_cols:
        if not df_orig[col].equals(df_final[col]):
            changes = (df_orig[col] != df_final[col]) & ~(df_orig[col].isna() & df_final[col].isna())
            changed_count = changes.sum()
            if changed_count > 0:
                diffs[col] = changed_count

    sorted_diffs = dict(sorted(diffs.items(), key=lambda item: item[1], reverse=True))

    # 🎯 Gráfico de alterações por coluna
    if sorted_diffs:
        st.subheader("📊 Gráfico de Alterações por Coluna")

        fig, ax = plt.subplots(figsize=(6, 2))  # altura ajustada
        ax.bar(sorted_diffs.keys(), sorted_diffs.values())
        ax.set_xlabel("Coluna")
        ax.set_ylabel("Qtd. de Alterações")
        ax.set_title("Alterações por Coluna")
        plt.xticks(rotation=90)
        st.pyplot(fig)

    # 🔍 Tabela interativa por coluna selecionada
    if sorted_diffs:
        st.subheader("🗂️ Detalhamento por Coluna")

        selected_col = st.selectbox("Selecione uma coluna para ver alterações detalhadas", list(sorted_diffs.keys()))
        if selected_col:
            # Garante que o índice seja o mesmo para alinhamento correto
            df_orig = df_orig.reset_index(drop=True)
            df_final = df_final.reset_index(drop=True)

            # Alinha até o menor número de linhas (caso tenham tamanhos diferentes)
            min_len = min(len(df_orig), len(df_final))
            detail_df = pd.DataFrame({
                "Original": df_orig.loc[:min_len - 1, selected_col],
                "Final": df_final.loc[:min_len - 1, selected_col]
            })

            # Aplica filtro real de diferença
            filtered = detail_df[
                (detail_df["Original"] != detail_df["Final"]) &
                ~(detail_df["Original"].isna() & detail_df["Final"].isna())
            ]

            st.write(f"Total de alterações: {len(filtered)}")
            st.dataframe(filtered.reset_index())
