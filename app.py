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
    
    # CSS Ajustado
    st.markdown(f"""
    <style>
        .stApp {{ background-color: #f4f6f9; }}
        .big-card {{
            background: white; padding: 20px; border-radius: 10px;
            border-left: 6px solid {GenesisConfig.COLOR_PRIMARY};
            box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px;
        }}
        .stat-value {{ font-size: 22px; font-weight: bold; color: {GenesisConfig.COLOR_PRIMARY}; word-wrap: break-word; }}
        .stat-label {{ font-size: 13px; color: #666; text-transform: uppercase; letter-spacing: 1px; }}
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
# MANUAL DE SEO (TEXTO EDUCATIVO)
# =========================================================
def show_manual():
    with st.expander("📚 MANUAL DE OPERAÇÕES & ESTRATÉGIA SEO (Leia antes de usar)"):
        st.markdown("""
        ### 🚀 O Conceito "Genesis"
        Este não é um simples gerador de texto. É um **Diretor Criativo de IA** projetado especificamente para dominar o ranking "Imobiliária em Indaiatuba". Ele utiliza **Probabilidade Ponderada** para priorizar conteúdos que geram dinheiro, mas sem esquecer da autoridade de marca.

        ---

        ### 🎯 Aula Rápida de SEO: Onde está o Dinheiro?
        Ao escolher manualmente um **Tópico**, entenda o impacto no seu negócio:

        #### 💰 Money Keywords (Alta Prioridade - Fundo de Funil)
        *São tópicos onde o cliente já está com a carteira na mão. O programa prioriza estes temas em 80% das vezes no modo Aleatório.*
        * **Investimento / Valorização:** O cliente quer saber se vai perder dinheiro.
        * **Segurança:** Fator decisivo nº 1 para quem sai de SP.
        * **Custo de Vida:** Matemática pura para quem está fazendo as contas da mudança.
        * **Futuro / Plano Diretor:** Gatilho de ganância e visão de longo prazo.

        #### 🏗️ Authority Keywords (Média Prioridade - Meio de Funil)
        *Conteúdos que provam que você domina a cidade, não apenas os imóveis.*
        * **Educação / Escolas:** Fundamental para famílias.
        * **Logística / Viracopos:** Crucial para empresários e quem trabalha híbrido.
        * **Saúde / Hospitais:** Decisivo para público sênior e famílias com bebês.

        #### 🎨 Volume & Nicho (Baixa Prioridade - Topo de Funil)
        *Geram tráfego, mas pouco lead qualificado. Servem para "encher o blog" e criar semântica.*
        * **Clima, Arquitetura, Pets:** Assuntos leves. Use com moderação (ou deixe a IA sortear raramente).

        ---

        ### 🛠️ Como Configurar os Parâmetros
        1. **Persona:** Quem vai ler? (Ex: Não adianta falar de "Playground" para um "Investidor", fale de ROI).
        2. **Bairro:** Onde é o imóvel? (Se deixar Aleatório, a IA escolhe bairros compatíveis com a Persona).
        3. **Formato:** Como o texto será estruturado?
            * *Lista Polêmica:* Ótimo para viralizar.
            * *Guia Definitivo:* Ótimo para rankear no Google (SEO Técnico).
            * *Cenário Analítico:* Ótimo para convencer investidores racionais.
        4. **Gatilho:** Qual emoção queremos despertar? (Medo de perder a oportunidade? Orgulho de morar bem?).

        💡 **Dica de Ouro:** Na dúvida, deixe tudo em **ALEATÓRIO**. O robô foi treinado matematicamente para seguir a estratégia vencedora da Imobiliária Saber.
        """)

# =========================================================
# PROGRAMA PRINCIPAL
# =========================================================
def main():
    setup_ui()

    # 1. Carregamento de Dados
    try:
        dados_mestre = GenesisData()
        regras_mestre = GenesisRules()
    except RuntimeError as e:
        st.error(f"❌ Erro Crítico: {e}")
        st.stop()

    # Preparação das Listas
    persona_map = {v['nome']: k for k, v in GenesisConfig.PERSONAS.items()}
    lista_personas = ["ALEATÓRIO"] + list(persona_map.keys())
    lista_bairros = ["ALEATÓRIO"] + sorted([b['nome'] for b in dados_mestre.bairros])
    lista_topicos = ["ALEATÓRIO"] + sorted(list(GenesisConfig.TOPICS_MAP.values()))
    lista_ativos = ["ALEATÓRIO"] + dados_mestre.todos_ativos
    lista_formatos = ["ALEATÓRIO"] + list(GenesisConfig.CONTENT_FORMATS_MAP.values())
    lista_gatilhos = ["ALEATÓRIO"] + GenesisConfig.EMOTIONAL_TRIGGERS

    # 2. Sidebar (Configurações)
    with st.sidebar:
        st.header("⚡ GOD MODE CONFIG")
        st.caption(f"Engine: {GenesisConfig.VERSION}")
        
        data_escolhida = st.date_input("Data de Publicação", datetime.date.today())
        st.markdown("---")
        
        # Inputs do Usuário (Usando chaves únicas para o reset funcionar)
        sel_persona_nome = st.selectbox("1. Persona / Cliente", lista_personas, key="k_persona")
        sel_bairro = st.selectbox("2. Bairro ou Macro", lista_bairros, key="k_bairro")
        sel_topico = st.selectbox("3. Tópico (Peso SEO)", lista_topicos, key="k_topico")
        sel_ativo = st.selectbox("4. Tipo de Imóvel", lista_ativos, key="k_ativo")
        sel_formato = st.selectbox("5. Formato", lista_formatos, key="k_formato")
        sel_gatilho = st.selectbox("6. Gatilho", lista_gatilhos, key="k_gatilho")

        st.markdown("---")
        
        # LÓGICA DO BOTÃO RESET (LIMPA O ESTADO)
        if st.button("🔄 Resetar"):
            for key in st.session_state.keys():
                del st.session_state[key]
            st.rerun()

    # 3. Área Principal (Header)
    c1, c2 = st.columns([3, 1])
    with c1:
        st.title("⚡ GENESIS AGENCY MODULAR")
        st.markdown("**AI Content Director com Inteligência de SEO**")
    with c2:
        st.markdown("### 🤖 v53")
    
    # EXIBE O MANUAL AQUI
    show_manual()

    col_btn, _ = st.columns([1, 2])
    with col_btn:
        generate_btn = st.button("CRIAR PAUTA ESTRATÉGICA ✨")

    # 4. Lógica de Geração
    if generate_btn:
        try:
            with st.spinner("Processando estratégia de SEO..."):
                engine = GenesisEngine(dados_mestre)
                
                # Traduções
                persona_key_sel = "ALEATÓRIO"
                if sel_persona_nome != "ALEATÓRIO":
                    persona_key_sel = persona_map[sel_persona_nome]

                formato_key_sel = "ALEATÓRIO"
                if sel_formato != "ALEATÓRIO":
                    for k, v in GenesisConfig.CONTENT_FORMATS_MAP.items():
                        if v == sel_formato:
                            formato_key_sel = k
                            break

                user_selection = {
                    "persona_key": persona_key_sel,
                    "bairro_nome": sel_bairro,
                    "topico": sel_topico,
                    "ativo": sel_ativo,
                    "formato": formato_key_sel,
                    "gatilho": sel_gatilho
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
            st.error(f"Erro na execução: {e}")
            import traceback
            st.code(traceback.format_exc())
            st.stop()

        # 5. Exibição dos Resultados (COLUNAS AJUSTADAS [1, 1])
        col_main, col_view = st.columns([1, 1]) # <--- AJUSTE AQUI
        
        with col_main:
            bairro_display = resultado['bairro']['nome'] if resultado['bairro'] else "Indaiatuba (Geral)"
            zona_display = resultado['bairro']['zona'] if resultado['bairro'] else "Macro-zona"
            formato_tecnico = resultado['formato']
            formato_bonito = GenesisConfig.CONTENT_FORMATS_MAP.get(formato_tecnico, formato_tecnico)

            st.success("Estratégia Gerada com Sucesso!")
            
            st.markdown(f"""
            <div class="big-card">
                <div style="display:grid; grid-template-columns: 1fr; gap: 15px;">
                    <div>
                        <div class="stat-label">Persona Alvo</div>
                        <div class="stat-value">{resultado['persona']['nome']}</div>
                        <small><i>{resultado['persona']['dor']}</i></small>
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
                    <div>
                        <div class="stat-label">Tópico Principal</div>
                        <div class="stat-value">{resultado['topico']}</div>
                    </div>
                    <br>
                    <div class="stat-label">Nota Técnica</div>
                    <small>{resultado['obs_tecnica']}</small>
                </div>
            </div>
            """, unsafe_allow_html=True)

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
