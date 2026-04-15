import streamlit as st
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import players
import pandas as pd

st.set_page_config(page_title="NBA Stats Analyzer", page_icon="🏀")
st.title("🏀 NBA Stats Analyzer")
st.markdown("Probabilidades baseadas em dados reais da temporada")

# Input do usuário
nome = st.text_input("Nome do jogador:", placeholder="Ex: Stephen Curry")
season = st.selectbox("Temporada:", ["2024-25", "2023-24", "2022-23"])

if st.button("Analisar") and nome:
    with st.spinner("Buscando dados reais da NBA..."):
        resultado = players.find_players_by_full_name(nome)

        if not resultado:
            st.error(f"Jogador '{nome}' não encontrado.")
        else:
            jogador = resultado[0]
            gamelog = playergamelog.PlayerGameLog(
                player_id=jogador["id"], season=season
            )
            df = gamelog.get_data_frames()[0]

            if df.empty:
                st.warning("Sem dados para essa temporada.")
            else:
                total = len(df)
                media_pts = df["PTS"].mean()
                media_ast = df["AST"].mean()
                media_reb = df["REB"].mean()

                st.subheader(f"{jogador['full_name']} — {season}")

                # Médias
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Jogos", total)
                col2.metric("Média PTS", f"{media_pts:.1f}")
                col3.metric("Média AST", f"{media_ast:.1f}")
                col4.metric("Média REB", f"{media_reb:.1f}")

                st.markdown("---")
                st.subheader("📊 Probabilidades")

                # Pontos
                st.markdown("**Pontos**")
                for pts in [10, 15, 20, 25, 30, 35]:
                    pct = round(len(df[df["PTS"] >= pts]) / total * 100, 1)
                    st.progress(int(pct), text=f"≥ {pts} pts → {pct}%")

                st.markdown("**Assistências**")
                for ast in [5, 8, 10, 12]:
                    pct = round(len(df[df["AST"] >= ast]) / total * 100, 1)
                    st.progress(int(pct), text=f"≥ {ast} ast → {pct}%")

                st.markdown("**Rebotes**")
                for reb in [5, 8, 10, 12]:
                    pct = round(len(df[df["REB"] >= reb]) / total * 100, 1)
                    st.progress(int(pct), text=f"≥ {reb} reb → {pct}%")

                # Tabela de jogos
                st.markdown("---")
                st.subheader("📅 Últimos 10 jogos")
                st.dataframe(
                    df[["GAME_DATE", "MATCHUP", "PTS", "AST", "REB"]].head(10),
                    use_container_width=True
                )
