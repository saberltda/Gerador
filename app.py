# app.py
import streamlit as st
import datetime
import os
from src.database import GenesisData, GenesisRules
from src.engine import GenesisEngine
from src.config import GenesisConfig
from src.builder import PromptBuilder
from src.utils import slugify

# =========================================================
# CONFIGURAÇÃO VISUAL (CSS)
# =========================================================
def setup_ui():
    st.set_page_config(page_title="Genesis Modular v53", page_icon="🏗️", layout="wide")
    
    # CSS para deixar bonito (Estilo "God Mode")
    st.markdown(f"""
    <style>
        .stApp {{ background-color: #f4f6f9; }}
        .big-card {{
            background: white; padding: 20px; border-radius: 10px;
            border-left: 6px solid {GenesisConfig.COLOR_PRIMARY};
            box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px;
        }}
        .stat-value {{ font-size: 24px; font-weight: bold; color: {GenesisConfig.COLOR_PRIMARY}; }}
        .stat-label {{ font-size: 14px; color: #666; text-transform: uppercase; letter-spacing: 1px; }}
        .highlight {{ color: #D4AF37; font-weight: bold; }}
        div.stButton > button {{
            background: linear-gradient(45deg, {GenesisConfig.COLOR_PRIMARY}, #004080);
            color: white; border: none; height: 60px; font-size: 18px; font-weight: bold;
            width: 100%; border-radius: 8px; text-transform: uppercase;
        }}
        div.stButton > button:hover {{ opacity: 0.9; }}
    </style>
    """, unsafe_allow_html=True)

# =========================================================
# PROGRAMA PRINCIPAL
# =========================================================
def main():
    setup_ui()

    # 1. Carregamento de Dados (Como abrir um Table no Delphi)
    try:
        dados_mestre = GenesisData() # Carrega assets/bairros.json
        regras_mestre = GenesisRules() # Carrega assets/REGRAS.txt
    except RuntimeError as e:
        st.error(f"❌ Erro Crítico: {e}")
        st.stop()

    # =========================================================
    # PREPARAÇÃO DAS LISTAS (COM NOMES AMIGÁVEIS)
    # =========================================================
    
    # Personas: Mapa Reverso (Nome -> Chave)
    persona_map = {v['nome']: k for k, v in GenesisConfig.PERSONAS.items()}
    lista_personas = ["ALEATÓRIO"] + list(persona_map.keys())
    
    lista_bairros = ["ALEATÓRIO"] + sorted([b['nome'] for b in dados_mestre.bairros])
    
    # Tópicos: Pega apenas os valores (Nomes Bonitos)
    lista_topicos = ["ALEATÓRIO"] + sorted(list(GenesisConfig.TOPICS_MAP.values()))
    
    lista_ativos = ["ALEATÓRIO"] + dados_mestre.todos_ativos
    
    # Formatos: AGORA PEGA OS NOMES BONITOS DO MAPA (Ajuste Novo)
    lista_formatos = ["ALEATÓRIO"] + list(GenesisConfig.CONTENT_FORMATS_MAP.values())
    
    lista_gatilhos = ["ALEATÓRIO"] + GenesisConfig.EMOTIONAL_TRIGGERS

    # 2. Sidebar (Configurações)
    with st.sidebar:
        st.header("⚡ GOD MODE CONFIG")
        st.caption(f"Engine: {GenesisConfig.VERSION}")
        
        data_escolhida = st.date_input("Data de Publicação", datetime.date.today())
        st.markdown("---")
        
        # Inputs do Usuário
        sel_persona_nome = st.selectbox("1. Persona / Cliente", lista_personas)
        sel_bairro = st.selectbox("2. Bairro ou Macro", lista_bairros)
        sel_topico = st.selectbox("3. Tópico (Peso SEO)", lista_topicos)
        sel_ativo = st.selectbox("4. Tipo de Imóvel", lista_ativos)
        sel_formato = st.selectbox("5. Formato", lista_formatos) # Mostra "🔥 Lista Polêmica"
        sel_gatilho = st.selectbox("6. Gatilho", lista_gatilhos)

        st.markdown("---")
        if st.button("🔄 Resetar"):
            st.rerun()

    # 3. Área Principal (Header)
    c1, c2 = st.columns([3, 1])
    with c1:
        st.title("⚡ GENESIS AGENCY MODULAR")
        st.markdown("**AI Content Director com Inteligência de SEO**")
    with c2:
        # Logo placeholder
        st.markdown("### 🤖 v53")

    col_btn, _ = st.columns([1, 2])
    with col_btn:
        generate_btn = st.button("CRIAR PAUTA ESTRATÉGICA ✨")

    # 4. Lógica do Botão (O "OnClick" do Delphi)
    if generate_btn:
        try:
            with st.spinner("Processando estratégia de SEO..."):
                # A. Instancia o Motor
                engine = GenesisEngine(dados_mestre)
                
                # B. Prepara os inputs (TRADUÇÃO UI -> ENGINE)
                
                # Tradução Persona (Nome -> Chave)
                persona_key_sel = "ALEATÓRIO"
                if sel_persona_nome != "ALEATÓRIO":
                    persona_key_sel = persona_map[sel_persona_nome]

                # Tradução Formato (Nome Bonito -> Chave Técnica) - NOVO!
                formato_key_sel = "ALEATÓRIO"
                if sel_formato != "ALEATÓRIO":
                    # Procura qual chave tem esse valor bonito
                    for k, v in GenesisConfig.CONTENT_FORMATS_MAP.items():
                        if v == sel_formato:
                            formato_key_sel = k
                            break

                user_selection = {
                    "persona_key": persona_key_sel,
                    "bairro_nome": sel_bairro,
                    "topico": sel_topico, # Engine trata o Aleatório/Peso
                    "ativo": sel_ativo,
                    "formato": formato_key_sel, # Envia "LISTA_POLEMICA" e não "🔥 Lista..."
                    "gatilho": sel_gatilho
                }

                # C. Roda a Engine (Processamento Pesado)
                resultado = engine.run(user_selection)

                # D. Prepara o Texto Final (Builder)
                builder = PromptBuilder()
                
                # Datas para o JSON-LD
                hoje_iso = datetime.datetime.now().strftime(f"%Y-%m-%dT%H:%M:%S{GenesisConfig.FUSO_PADRAO}")
                d_pub = data_escolhida.strftime(f"%Y-%m-%dT00:00:00{GenesisConfig.FUSO_PADRAO}")
                
                # Prepara regras locais
                nome_bairro_ctx = resultado['bairro']['nome'] if resultado['bairro'] else "Indaiatuba"
                regras_injetadas = regras_mestre.get_for_prompt(nome_bairro_ctx)

                # Gera o Prompt
                prompt_final = builder.build(resultado, d_pub, hoje_iso, regras_injetadas)

                # Nome do arquivo para download
                p_name = slugify(resultado['persona']['nome'])[:10]
                ativo_name = slugify(resultado['ativo_definido'])[:10]
                nome_arquivo = f"{d_pub.split('T')[0]}_SEO_{p_name}_{ativo_name}.txt"

        except Exception as e:
            st.error(f"Erro na execução: {e}")
            import traceback
            st.code(traceback.format_exc())
            st.stop()

        # 5. Exibição dos Resultados (View)
        col_main, col_view = st.columns([1, 2])
        
        # Coluna da Esquerda (Resumo Visual)
        with col_main:
            bairro_display = resultado['bairro']['nome'] if resultado['bairro'] else "Indaiatuba (Geral)"
            zona_display = resultado['bairro']['zona'] if resultado['bairro'] else "Macro-zona"
            
            # Recupera o nome bonito do formato sorteado para exibir na tela
            formato_tecnico = resultado['formato']
            formato_bonito = GenesisConfig.CONTENT_FORMATS_MAP.get(formato_tecnico, formato_tecnico)

            st.success("Estratégia Gerada com Sucesso!")
            
            st.markdown(f"""
            <div class="big-card">
                <div style="display:grid; grid-template-columns: 1fr; gap: 10px;">
                    <div>
                        <div class="stat-label">Persona Alvo</div>
                        <div class="stat-value">{resultado['persona']['nome']}</div>
                        <small>{resultado['persona']['dor']}</small>
                    </div>
                    <hr>
                    <div>
                        <div class="stat-label">Localização Foco</div>
                        <div class="stat-value">{bairro_display}</div>
                        <small>{zona_display}</small>
                    </div>
                    <hr>
                    <div>
                        <div class="stat-label">Formato & Gatilho</div>
                        <div class="stat-value highlight">{formato_bonito}</div>
                        <small>{resultado['gatilho']}</small>
                    </div>
                    <hr>
                    <div class="stat-label">Tópico Principal</div>
                    <div class="stat-value">{resultado['topico']}</div>
                    <br>
                    <div class="stat-label">Nota Técnica</div>
                    <small>{resultado['obs_tecnica']}</small>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Coluna da Direita (Prompt e Download)
        with col_view:
            st.subheader("📋 Prompt Final (Copiar para IA)")
            st.text_area("Conteúdo", value=prompt_final, height=600)
            
            st.download_button(
                label="💾 BAIXAR ARQUIVO DE PAUTA (.txt)",
                data=prompt_final,
                file_name=nome_arquivo,
                mime="text/plain"
            )

if __name__ == "__main__":
    main()
