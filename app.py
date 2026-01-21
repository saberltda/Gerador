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
# 🎨 DESIGN SYSTEM (CLEAN & COMPATIBLE)
# =========================================================
def setup_ui():
    st.set_page_config(page_title="Gerador de Pautas IA", page_icon="🤖", layout="wide")
    
    st.markdown(f"""
    <style>
        .stApp {{ background-color: #f8f9fa; }}
        section[data-testid="stSidebar"] {{ display: none; }}
        
        h1, h2, h3 {{ font-family: 'Segoe UI', sans-serif; color: {GenesisConfig.COLOR_PRIMARY}; }}

        /* Cards de Resultado */
        .metric-card {{
            background: white; padding: 15px; border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            border-left: 5px solid {GenesisConfig.COLOR_PRIMARY};
            height: 100%;
        }}
        .metric-label {{ font-size: 11px; color: #888; text-transform: uppercase; margin-bottom: 5px; }}
        .metric-value {{ font-size: 16px; font-weight: 700; color: #333; }}
        
        /* Ajuste para o Container de Rolagem */
        div[data-testid="stVerticalBlockBorderWrapper"] {{
            border-radius: 8px;
            border: 1px solid #eee;
        }}
    </style>
    """, unsafe_allow_html=True)

# =========================================================
# 🛠️ COMPONENTE MESTRE: SCROLL + AUTO-CLOSE (FIXED)
# =========================================================
def smart_select(label, options, key, icon=""):
    """
    Componente Dropdown Inteligente.
    Correção v5.1: Removido 'use_container_width' do popover para evitar TypeError
    em versões antigas do Streamlit.
    """
    
    # 1. Inicializa o valor selecionado
    if key not in st.session_state:
        st.session_state[key] = options[0]
        
    # 2. Inicializa o contador de rotação (O Segredo do Auto-Close)
    reset_key_name = f"reset_counter_{key}"
    if reset_key_name not in st.session_state:
        st.session_state[reset_key_name] = 0

    current_val = str(st.session_state[key])
    display_text = (current_val[:25] + '..') if len(current_val) > 25 else current_val
    
    # Define se precisa de scroll (listas grandes)
    scroll_height = 300 if len(options) > 8 else None

    # 3. Cria o Popover com ID Dinâmica
    popover_id = f"pop_{key}_{st.session_state[reset_key_name]}"
    
    # FIX: Removemos use_container_width=True para compatibilidade máxima
    with st.popover(f"{icon} {label}: {display_text}", key=popover_id):
        st.caption(f"Selecione **{label}**:")
        
        # Container com scroll (se necessário)
        with st.container(height=scroll_height, border=False):
            
            # Encontra o índice seguro
            try:
                idx = options.index(st.session_state[key])
            except:
                idx = 0
            
            # Radio Button (não abre teclado no celular)
            new_val = st.radio(
                label,
                options,
                index=idx,
                key=f"rad_{key}_{st.session_state[reset_key_name]}",
                label_visibility="collapsed"
            )
            
            # 4. Lógica de Fechamento
            if new_val != st.session_state[key]:
                st.session_state[key] = new_val
                # Incrementa o contador -> Muda a ID do Popover -> Força recriação (Fechado)
                st.session_state[reset_key_name] += 1
                st.rerun()

    return st.session_state[key]

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
        if f"reset_counter_{k}" in st.session_state:
            del st.session_state[f"reset_counter_{k}"]
    
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
            return None
    return None

def show_manual():
    with st.expander("ℹ️ NOTAS RÁPIDAS"):
        c1, c2 = st.columns(2)
        with c1: st.caption("Use **Escassez** para vendas rápidas.")
        with c2: st.caption("Use **Autoridade** para branding.")

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
    st.title("Gerador de Pautas IA")
    st.caption(f"Versão 5.1 (Fixed Compatibility) | {GenesisConfig.VERSION}")
    
    tab_painel, tab_hist = st.tabs(["🎛️ CRIAÇÃO", "📂 HISTÓRICO"])

    with tab_painel:
        with st.container(border=True):
            
            # 1. CONTEXTO E PERSONA
            c1, c2 = st.columns([1, 2])
            with c1:
                data_pub = st.date_input("📅 Data", datetime.date.today(), key="k_data")
            with c2:
                sel_persona = smart_select("Persona", l_personas, "k_persona", "👤")

            st.markdown("---")

            # 2. GEOGRAFIA
            if "k_modo_geo" not in st.session_state: st.session_state["k_modo_geo"] = "🎲 Aleatório"
            
            try:
                modo_geo = st.pills("📍 Modo Geográfico", ["🎲 Aleatório", "🏙️ Foco Cidade", "📍 Bairro Específico"], default="🎲 Aleatório", key="k_modo_geo")
            except:
                modo_geo = st.radio("📍 Modo Geográfico", ["🎲 Aleatório", "🏙️ Foco Cidade", "📍 Bairro Específico"], horizontal=True, key="k_modo_geo")
            
            final_bairro_input = "ALEATÓRIO"
            
            if modo_geo == "📍 Bairro Específico":
                st.markdown("<br>", unsafe_allow_html=True)
                sel_bairro_manual = smart_select("Selecionar Bairro", l_bairros, "k_bairro", "🏘️")
                final_bairro_input = sel_bairro_manual
            elif modo_geo == "🏙️ Foco Cidade":
                final_bairro_input = "FORCE_CITY_MODE"
                st.caption("ℹ️ O texto falará sobre Indaiatuba como um todo.")

            st.markdown("---")

            # 3. ESTRATÉGIA
            c3, c4 = st.columns(2)
            with c3:
                sel_ativo = smart_select("Imóvel", l_ativos, "k_ativo", "🏠")
            with c4:
                sel_topico = smart_select("Tópico", l_topicos, "k_topico", "🚀")

            c5, c6 = st.columns(2)
            with c5:
                sel_formato = smart_select("Formato", l_formatos, "k_formato", "📝")
            with c6:
                sel_gatilho = smart_select("Gatilho", l_gatilhos, "k_gatilho", "🧠")

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
                status_text.text("🧠 Carregando contexto imobiliário...")
                progress_bar.progress(20)
                
                engine = GenesisEngine(dados_mestre)
                
                # Traduções de Chaves
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
                
                # Execução
                res = engine.run(user_sel)
                
                status_text.text("✍️ Redigindo com regras anti-anúncio...")
                progress_bar.progress(70)
                
                builder = PromptBuilder()
                
                # Datas
                fuso_br = datetime.timezone(datetime.timedelta(hours=-3))
                h_iso = datetime.datetime.now(fuso_br).strftime(f"%Y-%m-%dT%H:%M:%S{GenesisConfig.FUSO_PADRAO}")
                d_pub_iso = data_pub.strftime(f"%Y-%m-%dT00:00:00{GenesisConfig.FUSO_PADRAO}")
                
                local = res['bairro']['nome'] if res['bairro'] else "Indaiatuba"
                regras = regras_mestre.get_for_prompt(local)
                prompt = builder.build(res, d_pub_iso, h_iso, regras)
                
                nome_arq = f"{d_pub_iso.split('T')[0]}_SEO_{slugify(res['persona']['nome'])[:10]}.txt"
                
                progress_bar.progress(100)
                time.sleep(0.3)
                progress_bar.empty(); status_text.empty()

                st.success("✅ Pauta Gerada com Sucesso!")
                
                # Cards Visuais
                f_bonito = GenesisConfig.CONTENT_FORMATS_MAP.get(res['formato'], res['formato'])
                b_display = res['bairro']['nome'] if res['bairro'] else "Indaiatuba (Macro)"
                
                k1, k2, k3 = st.columns(3)
                with k1: st.markdown(f"""<div class="metric-card"><div class="metric-label">Persona Alvo</div><div class="metric-value">{res['persona']['nome'].split('(')[0]}</div></div>""", unsafe_allow_html=True)
                with k2: st.markdown(f"""<div class="metric-card"><div class="metric-label">Localização</div><div class="metric-value">{b_display}</div></div>""", unsafe_allow_html=True)
                with k3: st.markdown(f"""<div class="metric-card"><div class="metric-label">Estratégia</div><div class="metric-value">{f_bonito.split(' ')[0]} {f_bonito.split(' ')[1]}</div></div>""", unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("### 📋 Copie seu Prompt:")
                st.text_area("Prompt Final", value=prompt, height=400, label_visibility="collapsed")
                st.download_button("💾 Baixar Arquivo .txt", data=prompt, file_name=nome_arq, mime="text/plain", use_container_width=True)

            except Exception as e:
                status_text.empty(); progress_bar.empty()
                st.error(f"Erro na Geração: {e}")

    # --- ABA HISTÓRICO ---
    with tab_hist:
        df = load_history()
        if df is not None and not df.empty:
            st.dataframe(df, use_container_width=True, hide_index=True, column_config={"DATA": st.column_config.DatetimeColumn("Data", format="DD/MM HH:mm")})
            csv = df.to_csv(sep=';', index=False).encode('utf-8-sig')
            st.download_button("📥 Baixar Excel Completo", data=csv, file_name="historico_genesis.csv", mime="text/csv", use_container_width=True)
        else:
            st.info("Nenhuma pauta gerada recentemente.")

if __name__ == "__main__":
    main()
