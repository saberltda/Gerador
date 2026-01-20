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
# 🎨 DESIGN SYSTEM & CSS (Mobile Friendly)
# =========================================================
def setup_ui():
    st.set_page_config(page_title="Genesis Studio v60", page_icon="💎", layout="wide")
    
    st.markdown(f"""
    <style>
        .stApp {{ background-color: #f8f9fa; }}
        section[data-testid="stSidebar"] {{ display: none; }}
        
        h1, h2, h3 {{ font-family: 'Segoe UI', sans-serif; color: {GenesisConfig.COLOR_PRIMARY}; }}
        
        /* Painel de Controle */
        .control-panel {{
            background-color: white; padding: 20px; border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            border-top: 5px solid {GenesisConfig.COLOR_PRIMARY}; margin-bottom: 25px;
        }}

        /* Cards de Resultado */
        .metric-card {{
            background: white; padding: 15px; border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            border-left: 5px solid {GenesisConfig.COLOR_PRIMARY};
            height: 100%;
        }}
        .metric-label {{ font-size: 11px; color: #888; text-transform: uppercase; margin-bottom: 5px; }}
        .metric-value {{ font-size: 16px; font-weight: 700; color: #333; }}
        .metric-sub {{ font-size: 12px; color: #666; font-style: italic; }}
        
        /* Ajuste dos Popovers (Botões de Seleção) */
        [data-testid="stPopover"] > div > button {{
            background-color: white;
            border: 1px solid #ddd;
            color: #444;
            width: 100%;
            text-align: left;
            justify-content: space-between;
            height: 50px;
        }}
        [data-testid="stPopover"] > div > button:hover {{
            border-color: {GenesisConfig.COLOR_PRIMARY};
            color: {GenesisConfig.COLOR_PRIMARY};
        }}

        /* Botão Principal */
        [data-testid="baseButton-secondary"] {{
            background: linear-gradient(135deg, {GenesisConfig.COLOR_PRIMARY}, #00509e);
            color: white; border: none; height: 55px; font-size: 16px; width: 100%;
        }}
    </style>
    """, unsafe_allow_html=True)

# =========================================================
# 🛠️ COMPONENTE MOBILE-FIRST (SEM TECLADO)
# =========================================================
def mobile_dropdown(label, options, key, icon=""):
    """
    Cria um botão que abre um menu de opções (Radio) em vez de Selectbox.
    Isso impede que o teclado do celular abra, pois não há campo de busca.
    """
    # Pega o valor atual ou o primeiro da lista
    current_val = st.session_state.get(key, options[0])
    
    # Encurta o texto se for muito longo para caber no botão do celular
    display_text = (current_val[:28] + '..') if len(current_val) > 28 else current_val
    
    # Cria o Popover (Botão que abre menu)
    with st.popover(f"{icon} {label}: {display_text}", use_container_width=True):
        st.caption(f"Selecione {label}:")
        # O Radio button é amigável para toque e não abre teclado
        selection = st.radio(label, options, key=key, label_visibility="collapsed")
        
    return selection

# =========================================================
# LÓGICA DE CONTROLE
# =========================================================
def reset_state_callback():
    keys_to_reset = [
        "k_persona", "k_bairro", "k_topico", 
        "k_ativo", "k_formato", "k_gatilho", 
        "k_modo_geo", "k_data"
    ]
    for k in keys_to_reset:
        if k in st.session_state:
            del st.session_state[k]
    
    # Reseta valores padrão
    st.session_state["k_modo_geo"] = "🎲 Aleatório"
    st.session_state["k_data"] = datetime.date.today()

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
    with st.expander("ℹ️ NOTAS RÁPIDAS"):
        c1, c2 = st.columns(2)
        with c1: st.info("**Venda:** Use Gatilhos de Escassez/Urgência.")
        with c2: st.info("**Branding:** Use Tópicos de Autoridade (Saúde/Educação).")

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

    # --- CABEÇALHO ---
    st.title("💎 Genesis v60 (Mobile)")
    
    tab_painel, tab_hist = st.tabs(["🎛️ CRIAÇÃO", "📂 HISTÓRICO"])

    with tab_painel:
        # =====================================================
        # ÁREA DE CONTROLE (BOTÕES TIPO POPUP)
        # =====================================================
        with st.container(border=True):
            st.markdown("### 🛠️ Configuração da Pauta")
            
            # 1. CONTEXTO
            c1, c2 = st.columns([1, 2])
            with c1:
                data_pub = st.date_input("📅 Data", datetime.date.today(), key="k_data")
            with c2:
                # Substituindo Selectbox por Mobile Dropdown
                sel_persona = mobile_dropdown("Persona", l_personas, "k_persona", "👤")

            st.markdown("---")

            # 2. GEOGRAFIA
            c_geo_mode, c_geo_select = st.columns([1, 2])
            with c_geo_mode:
                if "k_modo_geo" not in st.session_state: st.session_state["k_modo_geo"] = "🎲 Aleatório"
                # Radio button já é mobile friendly
                modo_geo = st.radio("📍 Geografia", ["🎲 Aleatório", "🏙️ Foco Cidade", "📍 Bairro Específico"], key="k_modo_geo")
            
            final_bairro_input = "ALEATÓRIO"
            with c_geo_select:
                if modo_geo == "📍 Bairro Específico":
                    # Dropdown Mobile para Bairros
                    sel_bairro_manual = mobile_dropdown("Bairro", l_bairros, "k_bairro", "🏘️")
                    final_bairro_input = sel_bairro_manual
                elif modo_geo == "🏙️ Foco Cidade":
                    st.success("Texto focado na Cidade (Macro)")
                    final_bairro_input = "FORCE_CITY_MODE"
                else:
                    st.info("A IA escolherá o melhor local.")

            st.markdown("---")

            # 3. ESTRATÉGIA (Mobile Dropdowns)
            c3, c4 = st.columns(2)
            with c3:
                sel_ativo = mobile_dropdown("Imóvel", l_ativos, "k_ativo", "🏠")
            with c4:
                sel_topico = mobile_dropdown("Tópico", l_topicos, "k_topico", "🚀")

            c5, c6 = st.columns(2)
            with c5:
                sel_formato = mobile_dropdown("Formato", l_formatos, "k_formato", "📝")
            with c6:
                sel_gatilho = mobile_dropdown("Gatilho", l_gatilhos, "k_gatilho", "🧠")

            st.markdown("<br>", unsafe_allow_html=True)

            # 4. AÇÕES
            c_reset, c_run = st.columns([1, 3])
            with c_reset:
                st.button("🧹 LIMPAR", on_click=reset_state_callback, type="primary", use_container_width=True)
            with c_run:
                run_btn = st.button("✨ GERAR ESTRATÉGIA", type="secondary", use_container_width=True)

        # =====================================================
        # RESULTADOS
        # =====================================================
        if run_btn:
            show_manual()
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                status_text.text("🧠 Pensando...")
                progress_bar.progress(30)
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
                
                res = engine.run(user_sel)
                
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

                st.success("✅ Sucesso!")
                
                f_bonito = GenesisConfig.CONTENT_FORMATS_MAP.get(res['formato'], res['formato'])
                g_bonito = GenesisConfig.EMOTIONAL_TRIGGERS_MAP.get(res['gatilho'], res['gatilho'])
                b_display = res['bairro']['nome'] if res['bairro'] else "Indaiatuba"
                
                # Cards Mobile Friendly (2 por linha)
                k1, k2 = st.columns(2)
                with k1:
                    st.markdown(f"""<div class="metric-card"><div class="metric-label">Persona</div><div class="metric-value">{res['persona']['nome'].split('(')[0]}</div></div>""", unsafe_allow_html=True)
                with k2:
                    st.markdown(f"""<div class="metric-card"><div class="metric-label">Local</div><div class="metric-value">{b_display}</div></div>""", unsafe_allow_html=True)
                
                k3, k4 = st.columns(2)
                with k3:
                    st.markdown(f"""<div class="metric-card"><div class="metric-label">Estratégia</div><div class="metric-value">{f_bonito.split(' ')[0]} {f_bonito.split(' ')[1]}</div></div>""", unsafe_allow_html=True)
                with k4:
                    st.markdown(f"""<div class="metric-card"><div class="metric-label">SEO</div><div class="metric-value">{res['topico'].split(' ')[1]}</div></div>""", unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)
                st.text_area("Copiar Prompt:", value=prompt, height=400)
                st.download_button("💾 Baixar .txt", data=prompt, file_name=nome_arq, mime="text/plain", use_container_width=True)

            except Exception as e:
                status_text.empty(); progress_bar.empty()
                st.error(f"Erro: {e}")

    # --- ABA HISTÓRICO ---
    with tab_hist:
        df = load_history()
        if df is not None and not df.empty:
            st.dataframe(df, use_container_width=True, hide_index=True, column_config={"DATA": st.column_config.DatetimeColumn("Data", format="DD/MM HH:mm")})
            csv = df.to_csv(sep=';', index=False).encode('utf-8-sig')
            st.download_button("📥 Baixar Excel", data=csv, file_name="historico_genesis.csv", mime="text/csv", use_container_width=True)
        else:
            st.info("Sem histórico.")

if __name__ == "__main__":
    main()
