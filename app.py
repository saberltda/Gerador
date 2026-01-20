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
# 🎨 DESIGN SYSTEM & CSS (Full Width Moderno)
# =========================================================
def setup_ui():
    st.set_page_config(page_title="Genesis Studio v59.1", page_icon="💎", layout="wide")
    
    st.markdown(f"""
    <style>
        .stApp {{ background-color: #f8f9fa; }}
        
        /* Esconde Sidebar padrão */
        section[data-testid="stSidebar"] {{ display: none; }}
        
        h1, h2, h3 {{ font-family: 'Segoe UI', sans-serif; color: {GenesisConfig.COLOR_PRIMARY}; }}
        
        /* Painel de Controle */
        .control-panel {{
            background-color: white; padding: 25px; border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            border-top: 5px solid {GenesisConfig.COLOR_PRIMARY}; margin-bottom: 25px;
        }}

        /* Cards de Resultado */
        .metric-card {{
            background: white; padding: 20px; border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            border-left: 5px solid {GenesisConfig.COLOR_PRIMARY};
            height: 100%; transition: transform 0.2s;
        }}
        .metric-card:hover {{ transform: translateY(-3px); box-shadow: 0 6px 12px rgba(0,0,0,0.15); }}
        .metric-label {{ font-size: 12px; color: #888; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }}
        .metric-value {{ font-size: 18px; font-weight: 700; color: #333; line-height: 1.3; }}
        .metric-sub {{ font-size: 13px; color: #666; margin-top: 5px; font-style: italic; }}
        
        /* Botões */
        div.stButton > button {{
            height: 60px; font-size: 18px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;
            border-radius: 10px; transition: all 0.3s ease;
        }}
        [data-testid="baseButton-secondary"] {{
            background: linear-gradient(135deg, {GenesisConfig.COLOR_PRIMARY}, #00509e);
            color: white; border: none;
        }}
        [data-testid="baseButton-secondary"]:hover {{ box-shadow: 0 5px 15px rgba(0,50,150,0.3); opacity: 0.95; }}
        
        [data-testid="baseButton-primary"] {{
            background-color: #f0f2f6; color: #555; border: 1px solid #ddd;
        }}
        [data-testid="baseButton-primary"]:hover {{ background-color: #e2e6ea; color: #333; border-color: #ccc; }}
    </style>
    """, unsafe_allow_html=True)

# =========================================================
# LÓGICA DE CONTROLE (CORRIGIDA)
# =========================================================
def reset_state_callback():
    """
    Força manualmente todos os widgets para o valor padrão.
    Isso é mais seguro do que usar 'del' no session_state.
    """
    # 1. Reseta Selectboxes para o índice 0 ("ALEATÓRIO")
    st.session_state["k_persona"] = "ALEATÓRIO"
    st.session_state["k_topico"] = "ALEATÓRIO"
    st.session_state["k_ativo"] = "ALEATÓRIO"
    st.session_state["k_formato"] = "ALEATÓRIO"
    st.session_state["k_gatilho"] = "ALEATÓRIO"
    
    # 2. Reseta o Radio Button para a primeira opção
    st.session_state["k_modo_geo"] = "🎲 Aleatório"
    
    # 3. Reseta a Data para Hoje
    st.session_state["k_data"] = datetime.date.today()
    
    # 4. Remove a chave do Bairro (pois ela é condicional e pode não existir)
    if "k_bairro" in st.session_state:
        del st.session_state["k_bairro"]

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
    with st.expander("ℹ️ NOTAS RÁPIDAS (SEO & GATILHOS)"):
        c1, c2, c3 = st.columns(3)
        with c1: st.info("**Money Keywords:** Investimento, Segurança (Venda).")
        with c2: st.info("**Joias da Coroa:** Escassez e Urgência (Decisão).")
        with c3: st.info("**Dica:** Use 'Aleatório' para descobrir nichos.")

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
    l_bairros = sorted([b['nome'] for b in dados_mestre.bairros])
    l_topicos = ["ALEATÓRIO"] + sorted(list(GenesisConfig.TOPICS_MAP.values()))
    l_ativos = ["ALEATÓRIO"] + dados_mestre.todos_ativos
    l_formatos = ["ALEATÓRIO"] + list(GenesisConfig.CONTENT_FORMATS_MAP.values())
    l_gatilhos = ["ALEATÓRIO"] + list(GenesisConfig.EMOTIONAL_TRIGGERS_MAP.values())

    # ---------------------------------------------------------
    # CABEÇALHO
    # ---------------------------------------------------------
    st.title("💎 Genesis Content Studio v59.1")
    st.markdown(f"**Diretor Criativo de IA** | Blog: {GenesisConfig.BLOG_URL}")

    # ABAS PRINCIPAIS
    tab_painel, tab_hist = st.tabs(["🎛️ PAINEL DE CRIAÇÃO", "📂 HISTÓRICO"])

    with tab_painel:
        # =====================================================
        # ÁREA DE CONTROLE
        # =====================================================
        with st.container(border=True):
            st.markdown("### 🛠️ Configuração da Pauta")
            
            # LINHA 1: CONTEXTO GERAL
            c1, c2 = st.columns([1, 2])
            with c1:
                data_pub = st.date_input("📅 Data Publicação", datetime.date.today(), key="k_data")
            with c2:
                sel_persona = st.selectbox("👤 Persona (Público Alvo)", l_personas, key="k_persona")

            st.markdown("---")

            # LINHA 2: GEOGRAFIA
            c_geo_mode, c_geo_select = st.columns([1, 2])
            
            with c_geo_mode:
                # Se a chave não existir (primeira execução), define padrão
                if "k_modo_geo" not in st.session_state:
                    st.session_state["k_modo_geo"] = "🎲 Aleatório"
                    
                modo_geo = st.radio(
                    "📍 Definição Geográfica",
                    ["🎲 Aleatório", "🏙️ Foco Cidade", "📍 Bairro Específico"],
                    key="k_modo_geo"
                )
            
            final_bairro_input = "ALEATÓRIO"
            with c_geo_select:
                if modo_geo == "📍 Bairro Específico":
                    sel_bairro_manual = st.selectbox("Escolha o Bairro:", l_bairros, key="k_bairro")
                    final_bairro_input = sel_bairro_manual
                elif modo_geo == "🏙️ Foco Cidade":
                    st.info("ℹ️ O texto será focado na cidade de Indaiatuba (Macro).")
                    final_bairro_input = "FORCE_CITY_MODE"
                else:
                    st.info("ℹ️ A IA escolherá o local ideal para a Persona.")

            st.markdown("---")

            # LINHA 3: ESTRATÉGIA
            c3, c4 = st.columns(2)
            with c3:
                sel_ativo = st.selectbox("🏠 Tipo de Imóvel", l_ativos, key="k_ativo")
            with c4:
                sel_topico = st.selectbox("🚀 Tópico (Foco SEO)", l_topicos, key="k_topico")

            # LINHA 4: REFINAMENTO
            c5, c6 = st.columns(2)
            with c5:
                sel_formato = st.selectbox("📝 Formato do Texto", l_formatos, key="k_formato")
            with c6:
                sel_gatilho = st.selectbox("🧠 Gatilho Mental", l_gatilhos, key="k_gatilho")

            st.markdown("<br>", unsafe_allow_html=True)

            # LINHA 5: AÇÕES
            c_reset, c_run = st.columns([1, 3])
            with c_reset:
                st.button("🧹 LIMPAR TUDO", on_click=reset_state_callback, type="primary", use_container_width=True)
            with c_run:
                run_btn = st.button("✨ GERAR ESTRATÉGIA", type="secondary", use_container_width=True)

        # =====================================================
        # ÁREA DE RESULTADOS
        # =====================================================
        if run_btn:
            show_manual()
            
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

                user_sel = {
                    "persona_key": p_key, "bairro_nome": final_bairro_input, 
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

                # DASHBOARD
                st.success("✅ Estratégia Definida com Sucesso!")
                
                f_bonito = GenesisConfig.CONTENT_FORMATS_MAP.get(res['formato'], res['formato'])
                g_bonito = GenesisConfig.EMOTIONAL_TRIGGERS_MAP.get(res['gatilho'], res['gatilho'])
                b_display = res['bairro']['nome'] if res['bairro'] else "Indaiatuba (Macro)"
                
                k1, k2, k3, k4 = st.columns(4)
                with k1:
                    st.markdown(f"""<div class="metric-card"><div class="metric-label">Persona</div><div class="metric-value">{res['persona']['nome']}</div><div class="metric-sub">{res['persona']['dor'][:45]}...</div></div>""", unsafe_allow_html=True)
                with k2:
                    st.markdown(f"""<div class="metric-card"><div class="metric-label">Local & Ativo</div><div class="metric-value">{b_display}</div><div class="metric-sub">{res['ativo_definido']}</div></div>""", unsafe_allow_html=True)
                with k3:
                    st.markdown(f"""<div class="metric-card"><div class="metric-label">Tática</div><div class="metric-value">{f_bonito}</div><div class="metric-sub">{g_bonito}</div></div>""", unsafe_allow_html=True)
                with k4:
                    st.markdown(f"""<div class="metric-card"><div class="metric-label">SEO</div><div class="metric-value">{res['topico']}</div><div class="metric-sub">Foco de Ranking</div></div>""", unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)
                
                # Prompt e Download
                st.subheader("📋 Prompt Gerado")
                st.text_area("Copie e cole na IA:", value=prompt, height=600)
                
                c_down, _ = st.columns([1, 3])
                with c_down:
                    st.download_button("💾 Baixar Pauta (.txt)", data=prompt, file_name=nome_arq, mime="text/plain", use_container_width=True)

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
