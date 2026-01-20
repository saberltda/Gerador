# app.py
import streamlit as st
import datetime
import os
import time
import pandas as pd
from src.database import GenesisData, GenesisRules
from src.engine import GenesisEngine
from src.config import GenesisConfig
from src.builder import PromptBuilder
from src.utils import slugify

# =========================================================
# 🎨 DESIGN SYSTEM & CSS (Dashboard Style)
# =========================================================
def setup_ui():
    st.set_page_config(page_title="Genesis Studio v58", page_icon="💎", layout="wide")
    
    st.markdown(f"""
    <style>
        .stApp {{ background-color: #f0f2f6; }}
        section[data-testid="stSidebar"] {{ background-color: #ffffff; border-right: 1px solid #e0e0e0; }}
        
        h1, h2, h3 {{ font-family: 'Segoe UI', sans-serif; color: {GenesisConfig.COLOR_PRIMARY}; }}
        
        /* Cards de Resultado */
        .metric-card {{
            background: white; padding: 15px; border-radius: 12px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            border-left: 4px solid {GenesisConfig.COLOR_PRIMARY};
            height: 100%; transition: transform 0.2s;
        }}
        .metric-card:hover {{ transform: translateY(-2px); box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}
        .metric-label {{ font-size: 11px; color: #888; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px; }}
        .metric-value {{ font-size: 16px; font-weight: 700; color: #333; line-height: 1.3; }}
        .metric-sub {{ font-size: 12px; color: #666; margin-top: 4px; font-style: italic; }}
        
        /* Botão Principal */
        div.stButton > button {{
            background: linear-gradient(90deg, {GenesisConfig.COLOR_PRIMARY}, #00509e);
            color: white; border: none; height: 55px; font-size: 16px; font-weight: 600;
            width: 100%; border-radius: 8px; text-transform: uppercase; letter-spacing: 0.5px;
            box-shadow: 0 4px 6px rgba(0, 51, 102, 0.2);
        }}
        div.stButton > button:hover {{ opacity: 0.95; box-shadow: 0 6px 12px rgba(0, 51, 102, 0.3); }}
        
        /* Ajuste de Abas */
        .stTabs [data-baseweb="tab-list"] {{ gap: 8px; }}
        .stTabs [data-baseweb="tab"] {{
            height: 45px; background-color: #fff; border-radius: 6px; border: 1px solid #eee;
            color: #555; font-weight: 500;
        }}
        .stTabs [aria-selected="true"] {{
            background-color: {GenesisConfig.COLOR_PRIMARY}; color: white; border: none;
        }}
    </style>
    """, unsafe_allow_html=True)

# =========================================================
# LÓGICA DE CONTROLE
# =========================================================
def reset_state_callback():
    """Limpa estado e reseta filtros"""
    keys = ["k_persona", "k_bairro", "k_topico", "k_ativo", "k_formato", "k_gatilho", "k_modo_geo"]
    for k in keys: 
        if k in st.session_state:
            del st.session_state[k]

def load_history():
    log_file = "historico_geracao.csv"
    if os.path.exists(log_file):
        try:
            df = pd.read_csv(log_file, sep=';', encoding='utf-8-sig')
            if 'DATA' in df.columns:
                df['DATA'] = pd.to_datetime(df['DATA'])
                df = df.sort_values(by='DATA', ascending=False)
            return df
        except:
            try: return pd.read_csv(log_file, sep=';', encoding='utf-8')
            except: return None
    return None

def show_manual():
    with st.expander("📚 NOTAS TÉCNICAS (SEO & Gatilhos)"):
        st.info("💡 **Dica de Autonomia:** Use 'Aleatório' quando quiser que a IA descubra oportunidades inexploradas. Force escolhas manuais apenas quando tiver um imóvel específico para vender.")

# =========================================================
# APP PRINCIPAL
# =========================================================
def main():
    setup_ui()
    
    try:
        dados_mestre = GenesisData()
        regras_mestre = GenesisRules()
    except RuntimeError as e:
        st.error(f"❌ Erro de Sistema: {e}")
        st.stop()

    # Listas
    persona_map = {v['nome']: k for k, v in GenesisConfig.PERSONAS.items()}
    l_personas = ["ALEATÓRIO"] + list(persona_map.keys())
    l_bairros = sorted([b['nome'] for b in dados_mestre.bairros]) # Sem "Aleatório" aqui, pois a lógica mudou
    l_topicos = ["ALEATÓRIO"] + sorted(list(GenesisConfig.TOPICS_MAP.values()))
    l_ativos = ["ALEATÓRIO"] + dados_mestre.todos_ativos
    l_formatos = ["ALEATÓRIO"] + list(GenesisConfig.CONTENT_FORMATS_MAP.values())
    l_gatilhos = ["ALEATÓRIO"] + list(GenesisConfig.EMOTIONAL_TRIGGERS_MAP.values())

    # ---------------------------------------------------------
    # BARRA LATERAL (PODER TOTAL AO USUÁRIO)
    # ---------------------------------------------------------
    with st.sidebar:
        st.title("🎛️ CONTROLE")
        st.caption(f"Versão: {GenesisConfig.VERSION}")
        data_pub = st.date_input("📅 Data da Publicação", datetime.date.today())
        st.divider()

        # 1. CLIENTE (PERSONA)
        st.markdown("#### 👤 1. Quem é o Cliente?")
        sel_persona = st.selectbox("Selecione a Persona", l_personas, key="k_persona")
        
        st.markdown("---")

        # 2. LOCALIZAÇÃO (LÓGICA CONDICIONAL AQUI)
        st.markdown("#### 📍 2. Onde é o Imóvel?")
        
        # O Pulo do Gato: Radio Button define se mostra ou não a lista de bairros
        modo_geo = st.radio(
            "Definição Geográfica:",
            ["🎲 Aleatório (IA Decide)", "🏙️ Foco Cidade (Sem Bairro)", "📍 Bairro Específico"],
            key="k_modo_geo",
            horizontal=True
        )

        final_bairro_input = "ALEATÓRIO" # Padrão
        
        if modo_geo == "📍 Bairro Específico":
            # Só mostra a lista se o usuário pediu especificidade
            sel_bairro_manual = st.selectbox("Escolha o Bairro:", l_bairros, key="k_bairro")
            final_bairro_input = sel_bairro_manual
        elif modo_geo == "🏙️ Foco Cidade (Sem Bairro)":
            # Envia um código que o motor sabe que força modo cidade
            final_bairro_input = "FORCE_CITY_MODE"
            st.caption("ℹ️ O texto falará de Indaiatuba no geral, sem citar bairros.")
        else:
            # Aleatório
            st.caption("ℹ️ A IA vai analisar a Persona e escolher o melhor bairro (ou focar na cidade).")

        st.markdown("---")

        # 3. IMÓVEL E ESTRATÉGIA
        st.markdown("#### 🏠 3. Detalhes da Pauta")
        sel_ativo = st.selectbox("Tipo de Imóvel", l_ativos, key="k_ativo")
        sel_topico = st.selectbox("Tópico (SEO)", l_topicos, key="k_topico")
        
        c_lat1, c_lat2 = st.columns(2)
        with c_lat1:
            sel_formato = st.selectbox("Formato", l_formatos, key="k_formato")
        with c_lat2:
            sel_gatilho = st.selectbox("Gatilho", l_gatilhos, key="k_gatilho")

        st.divider()
        if st.button("🔄 LIMPAR FILTROS", on_click=reset_state_callback):
            pass

    # ---------------------------------------------------------
    # ÁREA PRINCIPAL
    # ---------------------------------------------------------
    c_title, c_ver = st.columns([5, 1])
    with c_title:
        st.title("Genesis Content Studio")
    with c_ver:
        st.markdown("### v58")

    # ABAS
    tab_gen, tab_hist = st.tabs(["✨ GERADOR", "📂 HISTÓRICO"])

    # --- ABA GERADOR ---
    with tab_gen:
        show_manual()
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_space, col_action, col_space2 = st.columns([1, 2, 1])
        with col_action:
            run_btn = st.button("🚀 GERAR ESTRATÉGIA AGORA")

        if run_btn:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                status_text.text("🧠 Carregando inteligência de mercado...")
                progress_bar.progress(20)
                time.sleep(0.2)
                
                engine = GenesisEngine(dados_mestre)
                
                # Traduções
                p_key = "ALEATÓRIO"
                if sel_persona != "ALEATÓRIO": p_key = persona_map[sel_persona]
                
                f_key = "ALEATÓRIO"
                if sel_formato != "ALEATÓRIO":
                    for k,v in GenesisConfig.CONTENT_FORMATS_MAP.items():
                        if v == sel_formato: f_key = k; break
                
                g_key = "ALEATÓRIO"
                if sel_gatilho != "ALEATÓRIO":
                    for k,v in GenesisConfig.EMOTIONAL_TRIGGERS_MAP.items():
                        if v == sel_gatilho: g_key = k; break

                # Aqui usamos a variável 'final_bairro_input' definida pela lógica condicional
                user_sel = {
                    "persona_key": p_key,
                    "bairro_nome": final_bairro_input, 
                    "topico": sel_topico, "ativo": sel_ativo,
                    "formato": f_key, "gatilho": g_key
                }
                
                progress_bar.progress(50)
                res = engine.run(user_sel)
                
                status_text.text("✍️ Escrevendo prompt otimizado...")
                progress_bar.progress(80)
                
                builder = PromptBuilder()
                h_iso = datetime.datetime.now().strftime(f"%Y-%m-%dT%H:%M:%S{GenesisConfig.FUSO_PADRAO}")
                d_pub_iso = data_pub.strftime(f"%Y-%m-%dT00:00:00{GenesisConfig.FUSO_PADRAO}")
                local = res['bairro']['nome'] if res['bairro'] else "Indaiatuba"
                regras = regras_mestre.get_for_prompt(local)
                prompt = builder.build(res, d_pub_iso, h_iso, regras)
                
                nome_arq = f"{d_pub_iso.split('T')[0]}_SEO_{slugify(res['persona']['nome'])[:10]}.txt"
                
                progress_bar.progress(100)
                time.sleep(0.2)
                progress_bar.empty(); status_text.empty()

                # --- DASHBOARD ---
                st.success("✅ Estratégia Definida com Sucesso!")
                
                f_bonito = GenesisConfig.CONTENT_FORMATS_MAP.get(res['formato'], res['formato'])
                g_bonito = GenesisConfig.EMOTIONAL_TRIGGERS_MAP.get(res['gatilho'], res['gatilho'])
                b_display = res['bairro']['nome'] if res['bairro'] else "Indaiatuba (Macro)"
                
                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    st.markdown(f"""<div class="metric-card"><div class="metric-label">Persona</div><div class="metric-value">{res['persona']['nome']}</div><div class="metric-sub">{res['persona']['dor'][:50]}...</div></div>""", unsafe_allow_html=True)
                with c2:
                    st.markdown(f"""<div class="metric-card"><div class="metric-label">Local & Ativo</div><div class="metric-value">{b_display}</div><div class="metric-sub">{res['ativo_definido']}</div></div>""", unsafe_allow_html=True)
                with c3:
                    st.markdown(f"""<div class="metric-card"><div class="metric-label">Tática</div><div class="metric-value">{f_bonito}</div><div class="metric-sub">{g_bonito}</div></div>""", unsafe_allow_html=True)
                with c4:
                    st.markdown(f"""<div class="metric-card"><div class="metric-label">SEO</div><div class="metric-value">{res['topico']}</div><div class="metric-sub">Foco de Ranking</div></div>""", unsafe_allow_html=True)

                st.markdown("---")
                st.subheader("📋 Prompt Gerado")
                st.text_area("Copie e cole na IA:", value=prompt, height=500)
                st.download_button("💾 Baixar Pauta (.txt)", data=prompt, file_name=nome_arq, mime="text/plain")

            except Exception as e:
                status_text.empty(); progress_bar.empty()
                st.error(f"Erro na execução: {e}")

    # --- ABA HISTÓRICO ---
    with tab_hist:
        st.header("📂 Arquivo de Pautas")
        df = load_history()
        if df is not None and not df.empty:
            f_col1, f_col2 = st.columns(2)
            with f_col1:
                filtro_persona = st.selectbox("Filtrar por Persona:", ["TODAS"] + list(df['PERSONA'].unique()))
            
            df_show = df.copy()
            if filtro_persona != "TODAS":
                df_show = df_show[df_show['PERSONA'] == filtro_persona]

            st.dataframe(df_show, use_container_width=True, hide_index=True, column_config={"DATA": st.column_config.DatetimeColumn("Data", format="DD/MM/YY HH:mm")})
            csv = df_show.to_csv(sep=';', index=False).encode('utf-8-sig')
            st.download_button("📥 Baixar Planilha Excel", data=csv, file_name="historico_genesis.csv", mime="text/csv")
        else:
            st.info("Histórico vazio.")

if __name__ == "__main__":
    main()
