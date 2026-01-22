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

CONST_RANDOM = "🎲 ALEATÓRIO"

def setup_ui():
    st.set_page_config(page_title="Gerador de Pautas IA", page_icon="🤖", layout="wide")
    st.markdown(f"""
    <style>
        .stApp {{ background-color: #f8f9fa; }}
        section[data-testid="stSidebar"] {{ display: none; }}
        h1, h2, h3 {{ font-family: 'Segoe UI', sans-serif; color: {GenesisConfig.COLOR_PRIMARY}; }}
        div[data-testid="stButton"] button {{
            width: 100%; height: 50px; background-color: white !important;
            border: 1px solid #ddd !important; color: #444 !important;
            border-radius: 8px; font-size: 16px; font-weight: 500;
            justify-content: flex-start !important; padding-left: 15px !important;
            text-align: left !important; box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
        }}
        div[data-testid="column"] button[kind="primary"], 
        div[data-testid="column"] button[kind="secondary"] {{
            justify-content: center !important; text-align: center !important;
            padding-left: 0 !important; height: 60px !important;
        }}
        div[data-testid="stButton"] button:hover {{
            border-color: {GenesisConfig.COLOR_PRIMARY} !important;
            color: {GenesisConfig.COLOR_PRIMARY} !important;
            background-color: #fff !important;
        }}
        button[kind="secondary"] {{
            border: 2px solid {GenesisConfig.COLOR_PRIMARY} !important;
            color: {GenesisConfig.COLOR_PRIMARY} !important; font-weight: 700 !important;
        }}
        button[kind="secondary"]:hover {{
            background-color: {GenesisConfig.COLOR_PRIMARY} !important; color: white !important;
        }}
        button[kind="primary"] {{ border: 1px solid #ff4b4b !important; color: #ff4b4b !important; }}
        button[kind="primary"]:hover {{ background-color: #ff4b4b !important; color: white !important; }}
        .metric-card {{
            background: white; padding: 15px; border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05); border-left: 5px solid {GenesisConfig.COLOR_PRIMARY}; height: 100%;
        }}
        .metric-label {{ font-size: 11px; color: #888; text-transform: uppercase; margin-bottom: 5px; }}
        .metric-value {{ font-size: 16px; font-weight: 700; color: #333; }}
        .fake-label {{ font-size: 14px; margin-bottom: 7px; color: #31333F; font-family: "Source Sans Pro", sans-serif; visibility: visible; }}
    </style>
    """, unsafe_allow_html=True)

@st.dialog("Faça sua seleção")
def open_selection_dialog(label, options, key):
    st.write(f"Escolha uma opção para **{label}**:")
    current = st.session_state.get(key, options[0])
    try: idx = options.index(current)
    except: idx = 0
    container_kwargs = {"border": False}
    if len(options) > 10: container_kwargs["height"] = 300
    with st.container(**container_kwargs):
        new_val = st.radio(label, options, index=idx, key=f"radio_modal_{key}", label_visibility="collapsed")
    if new_val != current:
        st.session_state[key] = new_val
        st.rerun()

def smart_select(label, options, key, icon="", use_label=True):
    if key not in st.session_state: st.session_state[key] = options[0]
    current_val = str(st.session_state[key])
    display_text = (current_val[:28] + '..') if len(current_val) > 28 else current_val
    if use_label: st.markdown(f"<p class='fake-label'>{label}</p>", unsafe_allow_html=True)
    if st.button(f"{icon} {display_text}", key=f"btn_trig_{key}"): open_selection_dialog(label, options, key)
    return st.session_state[key]

def load_history():
    log_file = "historico_geracao.csv"
    if os.path.exists(log_file):
        try:
            df = pd.read_csv(log_file, sep=';', encoding='utf-8-sig')
            if 'DATA_PUB' in df.columns: df['DATA_PUB'] = pd.to_datetime(df['DATA_PUB'])
            if 'CRIADO_EM' in df.columns: df['CRIADO_EM'] = pd.to_datetime(df['CRIADO_EM'])
            df = df.sort_values(by='CRIADO_EM', ascending=False)
            return df
        except: return None
    return None

def main():
    setup_ui()
    try:
        dados_mestre = GenesisData()
        regras_mestre = GenesisRules()
    except RuntimeError as e:
        st.error(f"❌ Erro de Sistema: {e}"); st.stop()

    # --- DEFINIÇÃO DO MODO (DETERMINA AS LISTAS) ---
    if "k_tipo_pauta" not in st.session_state: st.session_state["k_tipo_pauta"] = "🏢 Imobiliária"

    # Listas estáticas
    persona_map = {v['nome']: k for k, v in GenesisConfig.PERSONAS.items()}
    l_personas = [CONST_RANDOM] + list(persona_map.keys())
    l_bairros = sorted([b['nome'] for b in dados_mestre.bairros])
    l_formatos = [CONST_RANDOM] + list(GenesisConfig.CONTENT_FORMATS_MAP.values())
    l_gatilhos = [CONST_RANDOM] + list(GenesisConfig.EMOTIONAL_TRIGGERS_MAP.values())

    st.title("Gerador de Pautas IA")
    st.caption(f"Versão 7.9 (Portal Sync) | {GenesisConfig.VERSION}")
    
    tab_painel, tab_hist = st.tabs(["🎛️ CRIAÇÃO", "📂 HISTÓRICO"])

    with tab_painel:
        with st.container(border=True):
            
            MAPA_MODOS = {"🏢 Imobiliária": "IMOBILIARIA", "📢 Portal da Cidade": "PORTAL"}
            opcoes_pauta = list(MAPA_MODOS.keys())
            
            try: tipo_pauta_ui = st.pills("Tipo de Pauta", opcoes_pauta, key="k_tipo_pauta")
            except: tipo_pauta_ui = st.radio("Tipo de Pauta", opcoes_pauta, horizontal=True, key="k_tipo_pauta")
            
            if not tipo_pauta_ui: tipo_pauta_ui = opcoes_pauta[0]
            tipo_pauta_code = MAPA_MODOS.get(tipo_pauta_ui, "IMOBILIARIA")
            eh_portal = (tipo_pauta_code == "PORTAL")

            # --- LÓGICA DINÂMICA DE LISTAS ---
            if not eh_portal:
                lista_ativos_display = [CONST_RANDOM] + dados_mestre.todos_ativos_imoveis
                # Usa tópicos imobiliários
                l_topicos = [CONST_RANDOM] + sorted(list(GenesisConfig.TOPICS_MAP.values()))
                label_ativo = "Imóvel"
                icon_ativo = "🏠"
            else:
                lista_ativos_display = [CONST_RANDOM] + dados_mestre.todos_ativos_portal
                # Usa tópicos de portal
                l_topicos = [CONST_RANDOM] + sorted(list(GenesisConfig.PORTAL_TOPICS_MAP.values()))
                label_ativo = "Categoria do Portal"
                icon_ativo = "📰"

            st.markdown("---")

            c1, c2 = st.columns([1, 2])
            with c1: data_pub = st.date_input("Data de Publicação", datetime.date.today(), key="k_data")
            with c2:
                if not eh_portal: sel_persona = smart_select("Persona Alvo", l_personas, "k_persona", "👤", use_label=True)
                else: st.info("ℹ️ Modo Portal: Público alvo definido como 'Cidadão'."); sel_persona = "CITIZEN_GENERAL"

            st.markdown("---")

            if "k_modo_geo" not in st.session_state: st.session_state["k_modo_geo"] = "🎲 Aleatório"
            try: modo_geo = st.pills("Modo Geográfico", ["🎲 Aleatório", "🏙️ Foco Cidade", "📍 Bairro Específico"], key="k_modo_geo")
            except: modo_geo = st.radio("Modo Geográfico", ["🎲 Aleatório", "🏙️ Foco Cidade", "📍 Bairro Específico"], horizontal=True, key="k_modo_geo")
            
            final_bairro_input = "ALEATÓRIO"
            if modo_geo == "📍 Bairro Específico":
                st.markdown("<br>", unsafe_allow_html=True)
                final_bairro_input = smart_select("Selecionar Bairro", l_bairros, "k_bairro", "🏘️", use_label=True)
            elif modo_geo == "🏙️ Foco Cidade":
                final_bairro_input = "FORCE_CITY_MODE"; st.caption("ℹ️ O texto falará sobre Indaiatuba como um todo.")

            st.markdown("---")

            c3, c4 = st.columns(2)
            with c3: sel_ativo = smart_select(label_ativo, lista_ativos_display, "k_ativo", icon_ativo, use_label=True)
            with c4: sel_topico = smart_select("Ângulo Editorial", l_topicos, "k_topico", "🚀", use_label=True)

            c5, c6 = st.columns(2)
            with c5: sel_formato = smart_select("Formato do Conteúdo", l_formatos, "k_formato", "📝", use_label=True)
            with c6: sel_gatilho = smart_select("Gatilho Mental", l_gatilhos, "k_gatilho", "🧠", use_label=True)

            st.markdown("<br>", unsafe_allow_html=True)

            c_reset, c_run = st.columns([1, 3])
            with c_reset:
                def reset_state_callback():
                    for k in ["k_persona", "k_bairro", "k_topico", "k_ativo", "k_formato", "k_gatilho", "k_modo_geo", "k_data", "k_tipo_pauta"]:
                        if k in st.session_state: del st.session_state[k]
                    st.session_state["k_modo_geo"] = "🎲 Aleatório"
                    st.session_state["k_tipo_pauta"] = "🏢 Imobiliária"
                    st.session_state["k_data"] = datetime.date.today()
                st.button("🧹 LIMPAR", on_click=reset_state_callback, type="primary", use_container_width=True)
            with c_run: run_btn = st.button("✨ GERAR ESTRATÉGIA", type="secondary", use_container_width=True)

        if run_btn:
            progress_bar = st.progress(0); status_text = st.empty()
            try:
                status_text.text("🧠 Carregando contexto...")
                progress_bar.progress(20)
                engine = GenesisEngine(dados_mestre)
                
                # --- TRADUÇÃO DAS SELEÇÕES ---
                p_key = "CITIZEN_GENERAL" if eh_portal else ("ALEATÓRIO" if sel_persona == CONST_RANDOM else persona_map[sel_persona])
                final_ativo_selecao = "ALEATÓRIO" if sel_ativo == CONST_RANDOM else sel_ativo
                
                # Tópico: Não precisa reversão pois usamos o display value
                final_topico = "ALEATÓRIO" if sel_topico == CONST_RANDOM else sel_topico
                
                f_key = "ALEATÓRIO"
                if sel_formato != CONST_RANDOM:
                    for k,v in GenesisConfig.CONTENT_FORMATS_MAP.items():
                        if v == sel_formato: f_key = k; break
                
                g_key = "ALEATÓRIO"
                if sel_gatilho != CONST_RANDOM:
                    for k,v in GenesisConfig.EMOTIONAL_TRIGGERS_MAP.items():
                        if v == sel_gatilho: g_key = k; break

                user_sel = {
                    "persona_key": p_key, "bairro_nome": final_bairro_input, "topico": final_topico,
                    "ativo": final_ativo_selecao, "formato": f_key, "gatilho": g_key,
                    "data_pub_obj": data_pub, "tipo_pauta": tipo_pauta_code
                }
                
                res = engine.run(user_sel)
                
                status_text.text("✍️ Redigindo com inteligência adaptativa...")
                progress_bar.progress(70)
                
                builder = PromptBuilder()
                fuso_br = datetime.timezone(datetime.timedelta(hours=-3))
                h_iso = datetime.datetime.now(fuso_br).strftime(f"%Y-%m-%dT%H:%M:%S{GenesisConfig.FUSO_PADRAO}")
                d_pub_iso = data_pub.strftime(f"%Y-%m-%dT00:00:00{GenesisConfig.FUSO_PADRAO}")
                local = res['bairro']['nome'] if res['bairro'] else "Indaiatuba"
                regras = regras_mestre.get_for_prompt(local)
                prompt = builder.build(res, d_pub_iso, h_iso, regras)
                
                data_prefix = d_pub_iso.split('T')[0]
                if eh_portal:
                    clean_ativo = slugify(res['ativo_definido'])[:20]
                    nome_arq = f"{data_prefix}_PORTAL_{clean_ativo}.txt"
                else:
                    clean_persona = slugify(res['persona']['nome'])[:10]
                    nome_arq = f"{data_prefix}_SEO_{clean_persona}.txt"
                
                progress_bar.progress(100); time.sleep(0.3); progress_bar.empty(); status_text.empty()
                st.success("✅ Pauta Gerada com Sucesso!")
                
                f_bonito = GenesisConfig.CONTENT_FORMATS_MAP.get(res['formato'], res['formato'])
                b_display = res['bairro']['nome'] if res['bairro'] else "Indaiatuba (Macro)"
                estrategia_display = f_bonito.split()[0] + " " + f_bonito.split()[1] if len(f_bonito.split()) >= 2 else f_bonito

                k1, k2, k3 = st.columns(3)
                with k1: 
                    nome_display = "Cidadão (Portal)" if eh_portal else res['persona']['nome'].split('(')[0]
                    st.markdown(f"""<div class="metric-card"><div class="metric-label">Público</div><div class="metric-value">{nome_display}</div></div>""", unsafe_allow_html=True)
                with k2: st.markdown(f"""<div class="metric-card"><div class="metric-label">Localização</div><div class="metric-value">{b_display}</div></div>""", unsafe_allow_html=True)
                with k3: st.markdown(f"""<div class="metric-card"><div class="metric-label">Estratégia</div><div class="metric-value">{estrategia_display}</div></div>""", unsafe_allow_html=True)

                st.markdown("<br>### 📋 Copie seu Prompt:", unsafe_allow_html=True)
                st.text_area("Prompt Final", value=prompt, height=400, label_visibility="collapsed")
                st.download_button("💾 Baixar Arquivo .txt", data=prompt, file_name=nome_arq, mime="text/plain", use_container_width=True)

            except Exception as e:
                status_text.empty(); progress_bar.empty(); st.error(f"Erro na Geração: {e}")

    with tab_hist:
        df = load_history()
        if df is not None and not df.empty:
            cols_cfg = {
                "DATA_PUB": st.column_config.DateColumn("Data Post", format="DD/MM/YYYY"),
                "CRIADO_EM": st.column_config.DatetimeColumn("Criado Em", format="DD/MM HH:mm"),
                "BAIRRO": "Local", "PERSONA": "Persona"
            }
            if "TIPO_PAUTA" in df.columns: cols_cfg["TIPO_PAUTA"] = "Tipo"
            st.dataframe(df, use_container_width=True, hide_index=True, column_config=cols_cfg)
            csv = df.to_csv(sep=';', index=False).encode('utf-8-sig')
            now_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
            st.download_button("📥 Baixar Excel Completo", data=csv, file_name=f"{now_str}_historico.csv", mime="text/csv", use_container_width=True)
        else: st.info("Nenhuma pauta gerada recentemente.")

if __name__ == "__main__":
    main()
