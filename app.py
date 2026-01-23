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
    if key not in st.session_state or st.session_state[key] not in options:
        st.session_state[key] = options[0]
    current_val = str(st.session_state[key])
    display_text = (current_val[:28] + '..') if len(current_val) > 28 else current_val
    if use_label: st.markdown(f"<p class='fake-label'>{label}</p>", unsafe_allow_html=True)
    if st.button(f"{icon} {display_text}", key=f"btn_trig_{key}"): open_selection_dialog(label, options, key)
    return st.session_state[key]

# --- HISTÓRICO (AGORA COM FUSO DE BRASÍLIA) ---

def load_history():
    log_file = "historico_geracao.csv"
    if os.path.exists(log_file):
        try:
            # Mantém nomes de coluna em CAIXA ALTA E UNDERLINE para o código funcionar
            df = pd.read_csv(log_file, sep=';', encoding='utf-8-sig')
            if 'CRIADO_EM' in df.columns:
                df['CRIADO_EM'] = pd.to_datetime(df['CRIADO_EM'], errors='coerce')
                df = df.sort_values(by='CRIADO_EM', ascending=False)
            return df
        except: return None
    return None

def save_history_log(user_inputs, engine_result):
    try:
        log_file = "historico_geracao.csv"
        
        # Dados Seguros
        bairro_obj = engine_result.get('bairro')
        bairro_real = bairro_obj.get('nome', "Indaiatuba") if isinstance(bairro_obj, dict) else ("Indaiatuba" if "FORCE" in str(bairro_obj) else str(bairro_obj))
        
        persona_obj = engine_result.get('persona')
        persona_nome = persona_obj.get('nome', "Desconhecida") if isinstance(persona_obj, dict) else (str(persona_obj) if persona_obj else "Desconhecida")
        
        data_pub = user_inputs.get('data_pub_obj')
        data_pub_str = data_pub.strftime("%Y-%m-%d") if data_pub else datetime.date.today().strftime("%Y-%m-%d")

        # ⛔ APLICAÇÃO DO FUSO DE BRASÍLIA
        agora_br = datetime.datetime.now(GenesisConfig.TZ_BRASILIA).strftime("%Y-%m-%d %H:%M:%S")

        new_data = {
            "CRIADO_EM": agora_br,
            "DATA_PUB": data_pub_str,
            "TIPO_PAUTA": user_inputs.get('tipo_pauta', 'N/A'),
            "PERSONA": persona_nome,
            "BAIRRO": bairro_real,
            "ATIVO": str(engine_result.get('ativo_definido', '')),
            "TOPICO": str(engine_result.get('topico', '')),
            "FORMATO": str(engine_result.get('formato', ''))
        }
        
        df_new = pd.DataFrame([new_data])
        
        if not os.path.exists(log_file):
            df_new.to_csv(log_file, sep=';', index=False, encoding='utf-8-sig')
        else:
            df_new.to_csv(log_file, sep=';', index=False, header=False, mode='a', encoding='utf-8-sig')
            
    except Exception as e:
        st.warning(f"⚠️ Histórico não salvo: {e}")

# =========================================================
# APP PRINCIPAL
# =========================================================

def main():
    setup_ui()
    try:
        dados_mestre = GenesisData()
        regras_mestre = GenesisRules()
        portal_sync = PortalSynchronizer()
        imob_sync = RealEstateSynchronizer()
    except Exception as e:
        st.error(f"❌ Erro Crítico: {e}"); st.stop()

    if "k_tipo_pauta" not in st.session_state: st.session_state["k_tipo_pauta"] = "🏢 Imobiliária"
    
    l_bairros = sorted([b['nome'] for b in dados_mestre.bairros])
    l_gatilhos = [CONST_RANDOM] + list(GenesisConfig.EMOTIONAL_TRIGGERS_MAP.values())

    st.title("Gerador de Pautas IA")
    st.caption(f"Versão 8.6 (UTC-3 Enforced) | {GenesisConfig.VERSION}")
    
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

            # --- SETUP DE LISTAS ---
            if eh_portal:
                label_parent = "1. Editoria (Seção)"
                icon_parent = "📰"
                raw_parent = portal_sync.get_editorias_display()
                map_parent_inv = {label: key for key, label in raw_parent}
                lista_parent_ui = [CONST_RANDOM] + list(map_parent_inv.keys())

                current_parent_label = st.session_state.get("k_ativo", CONST_RANDOM)
                current_parent_key = map_parent_inv.get(current_parent_label, None)

                if current_parent_key:
                    raw_topics = portal_sync.get_valid_topics(current_parent_key)
                    map_topico_inv = {label: key for key, label in raw_topics}
                    l_topicos = [CONST_RANDOM] + list(map_topico_inv.keys())
                    
                    raw_formats = portal_sync.get_valid_formats(current_parent_key)
                    map_formato_inv = {label: key for key, label in raw_formats}
                    l_formatos = [CONST_RANDOM] + list(map_formato_inv.keys())
                else:
                    l_topicos = [CONST_RANDOM]; l_formatos = [CONST_RANDOM]; map_topico_inv = {}; map_formato_inv = {}

            else:
                label_parent = "1. Categoria (Perfil)"
                icon_parent = "🏠"
                raw_parent = imob_sync.get_clusters_display()
                map_parent_inv = {label: key for key, label in raw_parent}
                lista_parent_ui = [CONST_RANDOM] + list(map_parent_inv.keys())

                current_parent_label = st.session_state.get("k_ativo", CONST_RANDOM)
                current_parent_key = map_parent_inv.get(current_parent_label, None)

                if current_parent_key:
                    ativos_db = imob_sync.get_valid_assets(current_parent_key)
                    lista_ativos_especificos = [CONST_RANDOM] + ativos_db
                    
                    raw_topics = imob_sync.get_valid_topics(current_parent_key)
                    map_topico_inv = {label: key for key, label in raw_topics}
                    l_topicos = [CONST_RANDOM] + list(map_topico_inv.keys())

                    raw_formats = imob_sync.get_valid_formats(current_parent_key)
                    map_formato_inv = {label: key for key, label in raw_formats}
                    l_formatos = [CONST_RANDOM] + list(map_formato_inv.keys())
                else:
                    lista_ativos_especificos = [CONST_RANDOM]; l_topicos = [CONST_RANDOM]; l_formatos = [CONST_RANDOM]
                    map_topico_inv = {}; map_formato_inv = {}

            st.markdown("---")

            c1, c2 = st.columns([1, 2])
            with c1: data_pub = st.date_input("Data de Publicação", datetime.date.today(), key="k_data")
            with c2:
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

            c3, c4 = st.columns(2)
            with c3: 
                sel_parent_ui = smart_select(label_parent, lista_parent_ui, "k_ativo", icon_parent, use_label=True)
                sel_parent_key = map_parent_inv.get(sel_parent_ui, "ALEATÓRIO")
            
            with c4:
                if not eh_portal:
                    sel_sub_ativo = smart_select("2. Imóvel Específico", lista_ativos_especificos, "k_sub_ativo", "🔑", use_label=True)
                else:
                    sel_topico_ui = smart_select("2. Tema Específico", l_topicos, "k_topico", "🔥", use_label=True)
                    sel_topico_key = map_topico_inv.get(sel_topico_ui, "ALEATÓRIO")

            c5, c6 = st.columns(2)
            with c5:
                if not eh_portal:
                    sel_topico_ui = smart_select("3. Tópico / Ângulo", l_topicos, "k_topico", "💡", use_label=True)
                    sel_topico_key = map_topico_inv.get(sel_topico_ui, "ALEATÓRIO")
                else:
                    sel_formato_ui = smart_select("3. Formato Jornalístico", l_formatos, "k_formato", "📝", use_label=True)
                    sel_formato_key = map_formato_inv.get(sel_formato_ui, "ALEATÓRIO")
            
            with c6:
                if not eh_portal:
                    sel_formato_ui = smart_select("4. Formato do Texto", l_formatos, "k_formato", "📝", use_label=True)
                    sel_formato_key = map_formato_inv.get(sel_formato_ui, "ALEATÓRIO")
                else:
                    st.empty()

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
                    for k in ["k_persona", "k_bairro", "k_topico", "k_ativo", "k_sub_ativo", "k_formato", "k_gatilho", "k_modo_geo", "k_data", "k_tipo_pauta"]:
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
                
                sub_ativo_val = st.session_state.get("k_sub_ativo", "ALEATÓRIO") if not eh_portal else "N/A"
                if sub_ativo_val == CONST_RANDOM: sub_ativo_val = "ALEATÓRIO"
                final_topico = sel_topico_key if 'sel_topico_key' in locals() and sel_topico_key else "ALEATÓRIO"
                final_formato = sel_formato_key if 'sel_formato_key' in locals() and sel_formato_key else "ALEATÓRIO"

                user_sel = {
                    "persona_key": "ALEATÓRIO", "bairro_nome": final_bairro_input,
                    "topico": final_topico, "ativo": sel_parent_key,
                    "sub_ativo": sub_ativo_val, "formato": final_formato,
                    "gatilho": gatilho_key, "data_pub_obj": data_pub,
                    "tipo_pauta": tipo_pauta_code
                }
                
                res = engine.run(user_sel)
                
                status_text.text("✍️ Escrevendo Texto Otimizado...")
                progress_bar.progress(70)
                
                builder = PromptBuilder()
                
                # ⛔ GERAÇÃO DO HORÁRIO NO FUSO CORRETO
                h_iso = datetime.datetime.now(GenesisConfig.TZ_BRASILIA).strftime(f"%Y-%m-%dT%H:%M:%S{GenesisConfig.FUSO_PADRAO}")
                d_pub_iso = data_pub.strftime(f"%Y-%m-%dT00:00:00{GenesisConfig.FUSO_PADRAO}")
                
                local = res['bairro']['nome'] if (res.get('bairro') and isinstance(res['bairro'], dict)) else "Indaiatuba"
                regras = regras_mestre.get_for_prompt(local)
                prompt = builder.build(res, d_pub_iso, h_iso, regras)
                
                data_prefix = d_pub_iso.split('T')[0]
                clean_name = slugify(str(res['ativo_definido']))[:20]
                nome_arq = f"{data_prefix}_{'PORTAL' if eh_portal else 'IMOB'}_{clean_name}.txt"
                
                save_history_log(user_sel, res)

                progress_bar.progress(100); time.sleep(0.3); progress_bar.empty(); status_text.empty()
                st.success("✅ Pauta Gerada com Sucesso!")
                
                # Cards de exibição
                b_display = res['bairro']['nome'] if (res.get('bairro') and isinstance(res['bairro'], dict)) else "Indaiatuba"
                parent_display = res.get('ativo_definido', 'N/A') if eh_portal else res.get('cluster_tecnico', 'N/A')
                k1, k2, k3 = st.columns(3)
                with k1: st.markdown(f"""<div class="metric-card"><div class="metric-label">Estratégia</div><div class="metric-value">{parent_display}</div></div>""", unsafe_allow_html=True)
                with k2: st.markdown(f"""<div class="metric-card"><div class="metric-label">Localização</div><div class="metric-value">{b_display}</div></div>""", unsafe_allow_html=True)
                with k3: st.markdown(f"""<div class="metric-card"><div class="metric-label">Formato</div><div class="metric-value">{res.get('formato', 'N/A')}</div></div>""", unsafe_allow_html=True)

                st.markdown("<br>### 📋 Copie seu Prompt:", unsafe_allow_html=True)
                st.text_area("Prompt Final", value=prompt, height=400, label_visibility="collapsed")
                st.download_button("💾 Baixar Arquivo .txt", data=prompt, file_name=nome_arq, mime="text/plain", use_container_width=True)

            except Exception as e:
                status_text.empty(); progress_bar.empty(); st.error(f"Erro na Geração: {e}")

    with tab_hist:
        df = load_history()
        if df is not None and not df.empty:
            # ⛔ MÁGICA DA UX: Renomeia as colunas APENAS para exibição na tela
            df_display = df.rename(columns={
                "CRIADO_EM": "Criado Em",
                "DATA_PUB": "Data Publicação",
                "TIPO_PAUTA": "Tipo Pauta",
                "PERSONA": "Público Alvo",
                "BAIRRO": "Local",
                "ATIVO": "Tema/Ativo",
                "TOPICO": "Ângulo",
                "FORMATO": "Formato"
            })
            
            st.dataframe(df_display, use_container_width=True, hide_index=True)
            
            # ⛔ MÁGICA DO EXCEL: Renomeia as colunas também no arquivo baixado
            # Assim o usuário final vê "Criado Em" e não "CRIADO_EM"
            csv = df_display.to_csv(sep=';', index=False).encode('utf-8-sig')
            
            now_str = datetime.datetime.now(GenesisConfig.TZ_BRASILIA).strftime("%Y-%m-%d_%H-%M")
            st.download_button("📥 Baixar Planilha (.csv)", data=csv, file_name=f"{now_str}_historico.csv", mime="text/csv", use_container_width=True)
        else:
            st.info("Nenhuma pauta gerada recentemente.")

if __name__ == "__main__":
    main()
