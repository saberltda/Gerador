# app.py
import streamlit as st
import datetime
import os
import pandas as pd
from src.database import GenesisData, GenesisRules
from src.engine import GenesisEngine
from src.config import GenesisConfig
from src.builder import PromptBuilder
from src.utils import slugify

# =========================================================
# CONFIGURAÇÃO VISUAL
# =========================================================
def setup_ui():
    st.set_page_config(page_title="Genesis Modular v55.2", page_icon="🏗️", layout="wide")
    
    st.markdown(f"""
    <style>
        .stApp {{ background-color: #f4f6f9; }}
        .big-card {{
            background: white; padding: 20px; border-radius: 10px;
            border-left: 6px solid {GenesisConfig.COLOR_PRIMARY};
            box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px;
        }}
        .stat-value {{ 
            font-size: 20px; font-weight: bold; color: {GenesisConfig.COLOR_PRIMARY}; 
            word-wrap: break-word; white-space: normal; line-height: 1.4;
        }}
        .stat-label {{ font-size: 12px; color: #666; text-transform: uppercase; letter-spacing: 1px; }}
        .highlight {{ color: #D4AF37; font-weight: bold; }}
        
        div.stButton > button {{
            background: linear-gradient(45deg, {GenesisConfig.COLOR_PRIMARY}, #004080);
            color: white; border: none; height: 60px; font-size: 18px; font-weight: bold;
            width: 100%; border-radius: 8px; text-transform: uppercase;
        }}
        div.stButton > button:hover {{ opacity: 0.9; }}
        
        /* Ajuste para as abas */
        .stTabs [data-baseweb="tab-list"] {{ gap: 10px; }}
        .stTabs [data-baseweb="tab"] {{
            height: 50px; white-space: pre-wrap; background-color: white; border-radius: 5px;
            color: {GenesisConfig.COLOR_PRIMARY};
        }}
        .stTabs [aria-selected="true"] {{
            background-color: {GenesisConfig.COLOR_PRIMARY}; color: white;
        }}
    </style>
    """, unsafe_allow_html=True)

# =========================================================
# CALLBACKS E UTILITÁRIOS
# =========================================================
def reset_state_callback():
    keys_to_reset = ["k_persona", "k_bairro", "k_topico", "k_ativo", "k_formato", "k_gatilho"]
    for key in keys_to_reset:
        st.session_state[key] = "ALEATÓRIO"

def load_history():
    """Carrega o CSV de histórico e retorna um DataFrame Pandas"""
    log_file = "historico_geracao.csv"
    if os.path.exists(log_file):
        try:
            # Tenta ler com utf-8-sig (o novo padrão) ou utf-8
            df = pd.read_csv(log_file, sep=';', encoding='utf-8-sig')
            df['DATA'] = pd.to_datetime(df['DATA'])
            df = df.sort_values(by='DATA', ascending=False)
            return df
        except Exception:
            # Fallback se o arquivo for antigo
            try:
                df = pd.read_csv(log_file, sep=';', encoding='utf-8')
                return df
            except Exception as e:
                st.error(f"Erro ao ler histórico: {e}")
                return None
    return None

def show_manual():
    with st.expander("📚 MANUAL DE OPERAÇÕES & GATILHOS MENTAIS"):
        st.markdown("""
        ### 🧠 Estratégia de Gatilhos (Gustavo Ferreira)
        * **JOIAS DA COROA (Venda):** Escassez, Urgência, Autoridade, Prova Social.
        * **CONEXÃO (Branding):** Inimigo Comum, Novidade, Porquê, História.
        """)

# =========================================================
# PROGRAMA PRINCIPAL
# =========================================================
def main():
    setup_ui()

    try:
        dados_mestre = GenesisData()
        regras_mestre = GenesisRules()
    except RuntimeError as e:
        st.error(f"❌ Erro Crítico: {e}")
        st.stop()

    # Prepara Listas
    persona_map = {v['nome']: k for k, v in GenesisConfig.PERSONAS.items()}
    lista_personas = ["ALEATÓRIO"] + list(persona_map.keys())
    lista_bairros = ["ALEATÓRIO"] + sorted([b['nome'] for b in dados_mestre.bairros])
    lista_topicos = ["ALEATÓRIO"] + sorted(list(GenesisConfig.TOPICS_MAP.values()))
    lista_ativos = ["ALEATÓRIO"] + dados_mestre.todos_ativos
    lista_formatos = ["ALEATÓRIO"] + list(GenesisConfig.CONTENT_FORMATS_MAP.values())
    lista_gatilhos = ["ALEATÓRIO"] + list(GenesisConfig.EMOTIONAL_TRIGGERS_MAP.values())

    # --- SIDEBAR FIXA ---
    with st.sidebar:
        st.header("⚡ CONFIGURAÇÃO")
        data_escolhida = st.date_input("Data de Publicação", datetime.date.today())
        st.markdown("---")
        
        sel_persona_nome = st.selectbox("1. Persona", lista_personas, key="k_persona")
        sel_bairro = st.selectbox("2. Bairro", lista_bairros, key="k_bairro")
        sel_topico = st.selectbox("3. Tópico", lista_topicos, key="k_topico")
        sel_ativo = st.selectbox("4. Ativo", lista_ativos, key="k_ativo")
        sel_formato = st.selectbox("5. Formato", lista_formatos, key="k_formato")
        sel_gatilho = st.selectbox("6. Gatilho", lista_gatilhos, key="k_gatilho")

        st.markdown("---")
        st.button("🔄 Resetar Filtros", on_click=reset_state_callback)

    # --- CABEÇALHO ---
    c1, c2 = st.columns([3, 1])
    with c1:
        st.title("⚡ GENESIS AGENCY MODULAR")
    with c2:
        st.markdown("### 🤖 v55.2")

    # --- SISTEMA DE ABAS (TABS) ---
    tab_gerador, tab_historico = st.tabs(["⚡ GERADOR DE PAUTAS", "📜 HISTÓRICO DE GERAÇÕES"])

    # =========================================================
    # ABA 1: GERADOR (A tela original)
    # =========================================================
    with tab_gerador:
        show_manual()
        
        col_btn, _ = st.columns([1, 2])
        with col_btn:
            generate_btn = st.button("CRIAR PAUTA ESTRATÉGICA ✨")

        if generate_btn:
            try:
                with st.spinner("Processando IA & Salvando Log..."):
                    engine = GenesisEngine(dados_mestre)
                    
                    # Traduções
                    persona_key_sel = "ALEATÓRIO"
                    if sel_persona_nome != "ALEATÓRIO": persona_key_sel = persona_map[sel_persona_nome]

                    formato_key_sel = "ALEATÓRIO"
                    if sel_formato != "ALEATÓRIO":
                        for k, v in GenesisConfig.CONTENT_FORMATS_MAP.items():
                            if v == sel_formato: formato_key_sel = k; break
                    
                    gatilho_key_sel = "ALEATÓRIO"
                    if sel_gatilho != "ALEATÓRIO":
                        for k, v in GenesisConfig.EMOTIONAL_TRIGGERS_MAP.items():
                            if v == sel_gatilho: gatilho_key_sel = k; break

                    user_selection = {
                        "persona_key": persona_key_sel,
                        "bairro_nome": sel_bairro,
                        "topico": sel_topico,
                        "ativo": sel_ativo,
                        "formato": formato_key_sel,
                        "gatilho": gatilho_key_sel
                    }

                    resultado = engine.run(user_selection)
                    builder = PromptBuilder()
                    
                    hoje_iso = datetime.datetime.now().strftime(f"%Y-%m-%dT%H:%M:%S{GenesisConfig.FUSO_PADRAO}")
                    d_pub = data_escolhida.strftime(f"%Y-%m-%dT00:00:00{GenesisConfig.FUSO_PADRAO}")
                    
                    nome_bairro_ctx = resultado['bairro']['nome'] if resultado['bairro'] else "Indaiatuba"
                    regras_injetadas = regras_mestre.get_for_prompt(nome_bairro_ctx)
                    prompt_final = builder.build(resultado, d_pub, hoje_iso, regras_injetadas)

                    p_name = slugify(resultado['persona']['nome'])[:10]
                    ativo_name = slugify(resultado['ativo_definido'])[:10]
                    nome_arquivo = f"{d_pub.split('T')[0]}_SEO_{p_name}_{ativo_name}.txt"

            except Exception as e:
                st.error(f"Erro: {e}")
                st.stop()

            # EXIBIÇÃO RESULTADO
            col_main, col_view = st.columns([1, 1])
            with col_main:
                bairro_display = resultado['bairro']['nome'] if resultado['bairro'] else "Indaiatuba (Geral)"
                zona_display = resultado['bairro']['zona'] if resultado['bairro'] else "Macro-zona"
                
                formato_tecnico = resultado['formato']
                formato_bonito = GenesisConfig.CONTENT_FORMATS_MAP.get(formato_tecnico, formato_tecnico)
                
                gatilho_tecnico = resultado['gatilho']
                gatilho_bonito = GenesisConfig.EMOTIONAL_TRIGGERS_MAP.get(gatilho_tecnico, gatilho_tecnico)

                st.success("✅ Pauta Gerada e Registrada no Histórico!")
                
                st.markdown(f"""
                <div class="big-card">
                    <div style="display:grid; grid-template-columns: 1fr; gap: 15px;">
                        <div><div class="stat-label">Persona</div><div class="stat-value">{resultado['persona']['nome']}</div></div>
                        <hr>
                        <div><div class="stat-label">Local</div><div class="stat-value">{bairro_display}</div><small>{zona_display}</small></div>
                        <hr>
                        <div><div class="stat-label">Estratégia</div><div class="stat-value highlight">{formato_bonito}</div><div class="stat-value highlight" style="font-size:16px;">{gatilho_bonito}</div></div>
                        <hr>
                        <div><div class="stat-label">Tópico</div><div class="stat-value">{resultado['topico']}</div></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col_view:
                st.subheader("📋 Prompt Final")
                st.text_area("Copiar:", value=prompt_final, height=600)
                st.download_button("💾 Baixar .txt", data=prompt_final, file_name=nome_arquivo)

    # =========================================================
    # ABA 2: HISTÓRICO (O Visualizador de Dados)
    # =========================================================
    with tab_historico:
        st.header("📜 Histórico de Gerações")
        st.markdown("Aqui fica o registro de todas as pautas criadas por este robô.")
        
        df_history = load_history()
        
        if df_history is not None and not df_history.empty:
            # Métricas Rápidas
            totais = len(df_history)
            try:
                personas_top = df_history['PERSONA'].value_counts().idxmax()
                bairro_top = df_history['BAIRRO'].value_counts().idxmax()
            except:
                personas_top = "-"
                bairro_top = "-"
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Total de Pautas", totais)
            m2.metric("Persona + Usada", personas_top)
            m3.metric("Bairro + Citado", bairro_top)
            
            st.divider()
            
            # Tabela Interativa
            st.dataframe(
                df_history, 
                use_container_width=True,
                hide_index=True,
                column_config={
                    "DATA": st.column_config.DatetimeColumn("Data", format="DD/MM/YYYY HH:mm"),
                    "PERSONA": "Persona Alvo",
                    "BAIRRO": "Localização",
                    "TOPICO": "Tema SEO",
                    "ATIVO": "Imóvel",
                    "FORMATO": "Formato",
                    "GATILHO": "Gatilho"
                }
            )
            
            # Botão para baixar o Excel/CSV completo
            # MUDANÇA AQUI: encoding='utf-8-sig' para download também
            csv_data = df_history.to_csv(sep=';', index=False).encode('utf-8-sig')
            st.download_button(
                label="📥 Baixar Histórico Completo (CSV/Excel)",
                data=csv_data,
                file_name="historico_completo_genesis.csv",
                mime="text/csv"
            )
        else:
            st.info("📭 Nenhum histórico encontrado ainda. Gere a primeira pauta para iniciar o registro!")

if __name__ == "__main__":
    main()
