import streamlit as st
import datetime
import os
import time
import pandas as pd
from src.database import GenesisData, GenesisRules
from src.engine import GenesisEngine
from src.config import GenesisConfig
from src.builder import PromptBuilder
from src.logic import PortalSynchronizer, RealEstateSynchronizer
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
        .fake-label {{ font-size: 14px; margin-bottom: 7px; color: #31333F; font-family: "Source Sans Pro", sans-serif; visibility: visible; }}
        .metric-card {{
            background: white; padding: 15px; border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05); border-left: 5px solid {GenesisConfig.COLOR_PRIMARY}; height: 100%;
        }}
        .metric-label {{ font-size: 11px; color: #888; text-transform: uppercase; margin-bottom: 5px; }}
        .metric-value {{ font-size: 16px; font-weight: 700; color: #333; }}
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
    if key not in st.session_state or st.session_state[key] not in options:
        st.session_state[key] = options[0]
        
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
            df = df.sort_values(by='CRIADO_EM', ascending=False)
            return df
        except: return None
    return None

def main():
    setup_ui()
    try:
        dados_mestre = GenesisData()
        regras_mestre = GenesisRules()
        portal_sync = PortalSynchronizer()
        imob_sync = RealEstateSynchronizer()
    except RuntimeError as e:
        st.error(f"❌ Erro de Sistema: {e}"); st.stop()

    if "k_tipo_pauta" not in st.session_state: st.session_state["k_tipo_pauta"] = "🏢 Imobiliária"

    l_bairros = sorted([b['nome'] for b in dados_mestre.bairros])
    l_gatilhos = [CONST_RANDOM] + list(GenesisConfig.EMOTIONAL_TRIGGERS_MAP.values())

    st.title("Gerador de Pautas IA")
    st.caption(f"Versão 8.3 (Fully Synced) | {GenesisConfig.VERSION}")
    
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

            # =========================================================
            # LÓGICA DE UI SINCRONIZADA (PARA AMBOS OS MODOS)
            # =========================================================
            
            # Variáveis de Controle
            map_parent_inv = {} # Pai (Editoria ou Cluster)
            map_topico_inv = {} # Filho 1
            map_formato_inv = {} # Filho 2
            lista_ativos_especificos = [] # Filho 3 (Apenas Imob)

            # --- SETUP DE LISTAS ---
            if eh_portal:
                label_parent = "1. Editoria (Seção)"
                icon_parent = "📰"
                
                # Pai: Editoria
                raw_parent = portal_sync.get_editorias_display()
                map_parent_inv = {label: key for key, label in raw_parent}
                lista_parent_ui = [CONST_RANDOM] + list(map_parent_inv.keys())

                # Recupera Seleção Atual
                current_parent_label = st.session_state.get("k_ativo", CONST_RANDOM)
                current_parent_key = map_parent_inv.get(current_parent_label, None)

                # Filhos (Portal não tem "Ativo Específico", só Tópico e Formato)
                if current_parent_key:
                    # Tópicos
                    raw_topics = portal_sync.get_valid_topics(current_parent_key)
                    map_topico_inv = {label: key for key, label in raw_topics}
                    l_topicos = [CONST_RANDOM] + list(map_topico_inv.keys())
                    
                    # Formatos
                    raw_formats = portal_sync.get_valid_formats(current_parent_key)
                    map_formato_inv = {label: key for key, label in raw_formats}
                    l_formatos = [CONST_RANDOM] + list(map_formato_inv.keys())
                else:
                    l_topicos = [CONST_RANDOM]; l_formatos = [CONST_RANDOM]

            else:
                # MODO IMOBILIÁRIA (Agora Sincronizado!)
                label_parent = "1. Categoria (Perfil)"
                icon_parent = "🏠"

                # Pai: Cluster/Categoria
                raw_parent = imob_sync.get_clusters_display()
                map_parent_inv = {label: key for key, label in raw_parent}
                lista_parent_ui = [CONST_RANDOM] + list(map_parent_inv.keys())

                # Recupera Seleção Atual
                current_parent_label = st.session_state.get("k_ativo", CONST_RANDOM)
                current_parent_key = map_parent_inv.get(current_parent_label, None)

                # Filhos
                if current_parent_key:
                    # Ativos Específicos (Sub-ativo)
                    lista_ativos_especificos = [CONST_RANDOM] + imob_sync.get_valid_assets(current_parent_key)
                    
                    # Tópicos
                    raw_topics = imob_sync.get_valid_topics(current_parent_key)
                    map_topico_inv = {label: key for key, label in raw_topics}
                    l_topicos = [CONST_RANDOM] + list(map_topico_inv.keys())

                    # Formatos
                    raw_formats = imob_sync.get_valid_formats(current_parent_key)
                    map_formato_inv = {label: key for key, label in raw_formats}
                    l_formatos = [CONST_RANDOM] + list(map_formato_inv.keys())
                else:
                    lista_ativos_especificos = [CONST_RANDOM]; l_topicos = [CONST_RANDOM]; l_formatos = [CONST_RANDOM]

            st.markdown("---")

            # --- LINHA 1: DATA E LOCAL ---
            c1, c2 = st.columns([1, 2])
            with c1: data_pub = st.date_input("Data de Publicação", datetime.date.today(), key="k_data")
            with c2:
                # Controle Geográfico (Mantido)
                if not eh_portal:
                    if "k_modo_geo" not in st.session_state: st.session_state["k_modo_geo"] = "🎲 Aleatório"
                    try: modo_geo = st.pills("Modo Geográfico", ["🎲 Aleatório", "🏙️ Foco Cidade", "📍 Bairro Específico"], key="k_modo_geo")
                    except: modo_geo = st.radio("Modo Geográfico", ["🎲 Aleatório", "🏙️ Foco Cidade", "📍 Bairro Específico"], horizontal=True, key="k_modo_geo")
                    
                    if modo_geo == "📍 Bairro Específico":
                        final_bairro_input = smart_select("Selecionar Bairro", l_bairros, "k_bairro", "🏘️", use_label=True)
                    elif modo_geo == "🏙️ Foco Cidade":
                        final_bairro_input = "FORCE_CITY_MODE"
                    else: final_bairro_input = "ALEATÓRIO"
                else:
                    st.caption("📍 Abrangência: **Cidade Inteira (Indaiatuba)**")
                    final_bairro_input = "FORCE_CITY_MODE"

            st.markdown("---")

            # --- LINHA 2: CASCATA PAI E FILHO 1 ---
            c3, c4 = st.columns(2)
            
            with c3: 
                # SELETOR PAI (Editoria ou Cluster)
                sel_parent_ui = smart_select(label_parent, lista_parent_ui, "k_ativo", icon_parent, use_label=True)
                sel_parent_key = map_parent_inv.get(sel_parent_ui, "ALEATÓRIO")
            
            with c4:
                # SELETOR FILHO 1 (Ativo Específico OU Tópico)
                if not eh_portal:
                    # Imobiliária: Mostra Ativo Específico aqui
                    sel_sub_ativo = smart_select("2. Imóvel Específico", lista_ativos_especificos, "k_sub_ativo", "🔑", use_label=True)
                else:
                    # Portal: Mostra Tópico aqui
                    sel_topico_ui = smart_select("2. Tema Específico", l_topicos, "k_topico", "🔥", use_label=True)
                    sel_topico_key = map_topico_inv.get(sel_topico_ui, "ALEATÓRIO")

            # --- LINHA 3: CASCATA FILHO 2 e 3 ---
            c5, c6 = st.columns(2)
            
            with c5:
                if not eh_portal:
                    # Imobiliária: Mostra Tópico aqui
                    sel_topico_ui = smart_select("3. Tópico / Ângulo", l_topicos, "k_topico", "💡", use_label=True)
                    sel_topico_key = map_topico_inv.get(sel_topico_ui, "ALEATÓRIO")
                else:
                    # Portal: Mostra Formato aqui
                    sel_formato_ui = smart_select("3. Formato Jornalístico", l_formatos, "k_formato", "📝", use_label=True)
                    sel_formato_key = map_formato_inv.get(sel_formato_ui, "ALEATÓRIO")
            
            with c6:
                if not eh_portal:
                    # Imobiliária: Mostra Formato aqui
                    sel_formato_ui = smart_select("4. Formato do Texto", l_formatos, "k_formato", "📝", use_label=True)
                    sel_formato_key = map_formato_inv.get(sel_formato_ui, "ALEATÓRIO")
                else:
                    st.empty() # Portal só tem 3 níveis

            # --- GATILHO (Opcional) ---
            if not eh_portal:
                st.markdown("<br>", unsafe_allow_html=True)
                st.caption("Configuração Extra:")
                sel_gatilho = smart_select("Gatilho Mental (Opcional)", l_gatilhos, "k_gatilho", "🧠", use_label=True)
                gatilho_key = "ALEATÓRIO"
                if sel_gatilho != CONST_RANDOM:
                    for k,v in GenesisConfig.EMOTIONAL_TRIGGERS_MAP.items():
                        if v == sel_gatilho: gatilho_key = k; break
            else:
                gatilho_key = "NEUTRAL_JOURNALISM"

            st.markdown("<br>", unsafe_allow_html=True)

            c_reset, c_run = st.columns([1, 3])
            with c_reset:
                def reset_state_callback():
                    keys_to_reset = ["k_persona", "k_bairro", "k_topico", "k_ativo", "k_sub_ativo", "k_formato", "k_gatilho", "k_modo_geo", "k_data", "k_tipo_pauta"]
                    for k in keys_to_reset:
                        if k in st.session_state: del st.session_state[k]
                    st.session_state["k_modo_geo"] = "🎲 Aleatório"
                    st.session_state["k_tipo_pauta"] = "🏢 Imobiliária"
                st.button("🧹 LIMPAR", on_click=reset_state_callback, type="primary", use_container_width=True)
            with c_run: run_btn = st.button("✨ GERAR TEXTO", type="secondary", use_container_width=True)

        if run_btn:
            progress_bar = st.progress(0); status_text = st.empty()
            try:
                status_text.text("🧠 Sincronizando Estratégia...")
                progress_bar.progress(20)
                engine = GenesisEngine(dados_mestre)
                
                # Montagem do User Selection (Padronizado)
                # 'ativo' = PAI (Editoria ou Cluster)
                # 'sub_ativo' = FILHO (Apenas Imob)
                # 'topico' = Key traduzida
                # 'formato' = Key traduzida
                
                # Tratamento do sub_ativo para Imob
                sub_ativo_val = st.session_state.get("k_sub_ativo", "ALEATÓRIO") if not eh_portal else "N/A"
                if sub_ativo_val == CONST_RANDOM: sub_ativo_val = "ALEATÓRIO"

                user_sel = {
                    "persona_key": "ALEATÓRIO", # Agora definido pelo Cluster
                    "bairro_nome": final_bairro_input,
                    "topico": sel_topico_key if sel_topico_key else "ALEATÓRIO",
                    "ativo": sel_parent_key, # Chave do Pai
                    "sub_ativo": sub_ativo_val, # Chave do Filho 1 (Imob)
                    "formato": sel_formato_key if sel_formato_key else "ALEATÓRIO",
                    "gatilho": gatilho_key,
                    "data_pub_obj": data_pub,
                    "tipo_pauta": tipo_pauta_code
                }
                
                res = engine.run(user_sel)
                
                status_text.text("✍️ Escrevendo Texto Otimizado...")
                progress_bar.progress(70)
                
                builder = PromptBuilder()
                fuso_br = datetime.timezone(datetime.timedelta(hours=-3))
                h_iso = datetime.datetime.now(fuso_br).strftime(f"%Y-%m-%dT%H:%M:%S{GenesisConfig.FUSO_PADRAO}")
                d_pub_iso = data_pub.strftime(f"%Y-%m-%dT00:00:00{GenesisConfig.FUSO_PADRAO}")
                local = res['bairro']['nome'] if res['bairro'] else "Indaiatuba"
                regras = regras_mestre.get_for_prompt(local)
                prompt = builder.build(res, d_pub_iso, h_iso, regras)
                
                data_prefix = d_pub_iso.split('T')[0]
                clean_name = slugify(res['ativo_definido'])[:20]
                nome_arq = f"{data_prefix}_{'PORTAL' if eh_portal else 'IMOB'}_{clean_name}.txt"
                
                progress_bar.progress(100); time.sleep(0.3); progress_bar.empty(); status_text.empty()
                st.success("✅ Pauta Sincronizada com Sucesso!")
                
                # Exibição
                b_display = res['bairro']['nome'] if res['bairro'] else "Indaiatuba"
                parent_display = res['ativo_definido'] if eh_portal else res['cluster_tecnico']
                
                k1, k2, k3 = st.columns(3)
                with k1: st.markdown(f"""<div class="metric-card"><div class="metric-label">Estratégia</div><div class="metric-value">{parent_display}</div></div>""", unsafe_allow_html=True)
                with k2: st.markdown(f"""<div class="metric-card"><div class="metric-label">Localização</div><div class="metric-value">{b_display}</div></div>""", unsafe_allow_html=True)
                with k3: st.markdown(f"""<div class="metric-card"><div class="metric-label">Formato</div><div class="metric-value">{res['formato']}</div></div>""", unsafe_allow_html=True)

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
                "BAIRRO": "Local"
            }
            st.dataframe(df, use_container_width=True, hide_index=True, column_config=cols_cfg)
        else: st.info("Nenhuma pauta gerada recentemente.")

if __name__ == "__main__":
    main()
