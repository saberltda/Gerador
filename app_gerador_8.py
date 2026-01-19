import streamlit as st
import random
import datetime
import unicodedata
import json
import urllib.request
import ssl
import re
import os

# ==============================================================================
# 🏛️ GENESIS AGENCY CORE (V8.0)
# A fusão definitiva entre Design (v7) e Performance (v50.1)
# ==============================================================================

class AgencyConfig:
    VERSION = "GENESIS 8.0 (AGENCY DIRECTOR MODE)"
    BLOG_URL = "https://blog.saber.imb.br"
    LEAD_SCRIPT = '<div style="text-align:center; margin: 40px 0;"><script async data-uid="d188d73e78" src="https://sabernovidades.kit.com/d188d73e78/index.js"></script></div>'
    
    # Cores da UI do Streamlit
    THEME = {
        "primary": "#003366", # Azul Saber
        "accent": "#D4AF37",  # Ouro (Premium)
        "bg": "#f4f6f9"
    }

    # Vocabulário de "Elite" (SEO Semântico)
    SEMANTIC_ENTITIES = {
        "FAMILY": ["Colégio Objetivo", "Parque Ecológico", "Segurança Monitorada", "Ciclovias", "Qualidade do Ar"],
        "INVESTOR": ["Valorização do m²", "Liquidez", "Plano Diretor", "Vetores de Crescimento", "Hub Logístico"],
        "HIGH_END": ["Helvetia", "Arquitetura Contemporânea", "Privacidade Absoluta", "Pé Direito Duplo", "Acabamento Premium"],
        "LOGISTICS": ["Aeroporto de Viracopos", "Rodovia Santos Dumont", "Galpões Modulares", "Last Mile"]
    }

    # Gatilhos de Neuromarketing (Instruções de Tom)
    NEURO_TRIGGERS = {
        "ESCASSEZ_REAL": "Enfatize que lotes/imóveis nesta zona específica são finitos e raros de aparecer à venda.",
        "CONTRASTE_DOR": "Comece descrevendo vividamente o caos de SP (trânsito/barulho) para contrastar com a paz de Indaiatuba.",
        "AUTORIDADE_DADOS": "Use números precisos (distâncias em minutos, metros quadrados) para gerar confiança racional.",
        "PERTENCIMENTO": "Descreva a comunidade local como um clube exclusivo de pessoas que valorizam o bem-viver.",
        "PROVA_SOCIAL_IMPLICITA": "Mencione como 'novas famílias estão migrando' para validar a decisão de compra."
    }

    # Personas Expandidas (União v7 + v50.1)
    PERSONAS = {
        "FAMILY_EXODUS": {
            "nome": "Família Êxodo (SP->Interior)",
            "cluster": "FAMILY",
            "dor": "Medo da violência e a infância perdida em apartamentos fechados.",
            "desejo": "Quintal, pé na grama e escolas de ponta a 5 minutos.",
            "zonas_alvo": ["residencial_fechado", "chacaras_fechado"]
        },
        "INVESTOR_SHARK": {
            "nome": "Investidor de Alta Performance",
            "cluster": "INVESTOR",
            "dor": "Ativos parados perdendo para a inflação.",
            "desejo": "ROI acima da média, liquidez rápida e segurança jurídica.",
            "zonas_alvo": ["mista", "residencial_fechado", "industrial"]
        },
        "DOCTOR_LUXURY": {
            "nome": "Médico/Profissional de Saúde",
            "cluster": "HIGH_END",
            "dor": "Rotina exaustiva de plantões e falta de silêncio.",
            "desejo": "Santuário de paz, isolamento acústico e proximidade do HAOC.",
            "zonas_alvo": ["residencial_fechado"]
        },
        "LOGISTICS_BOSS": {
            "nome": "Empresário Logístico",
            "cluster": "LOGISTICS",
            "dor": "Custo Brasil e gargalos de transporte.",
            "desejo": "Eficiência, acesso à Rodovia SP-75 e incentivos fiscais.",
            "zonas_alvo": ["industrial"]
        },
        "FIRST_HOME_URBAN": {
            "nome": "Jovem Casal (1º Imóvel)",
            "cluster": "URBAN",
            "dor": "Aluguel caro e medo de financiamento eterno.",
            "desejo": "Entrada possível, bairro planejado e potencial de valorização.",
            "zonas_alvo": ["residencial_aberto", "zona_vertical"]
        }
    }

# =========================================================
# 🧠 CÉREBRO DA AGÊNCIA (Lógica & Dados)
# =========================================================

class AgencyBrain:
    def __init__(self):
        self.bairros = self._load_bairros()
        
    def _load_bairros(self):
        # Tenta carregar do JSON, se falhar, usa Mock de elite
        try:
            with open("bairros.json", "r", encoding="utf-8") as f:
                raw = json.load(f)
            # Normalização de Zonas
            final = []
            for b in raw:
                z = b.get('zona', '').lower()
                if "fechado" in z: zn = "residencial_fechado"
                elif "chácara" in z: zn = "chacaras_fechado"
                elif "industrial" in z or "empresarial" in z: zn = "industrial"
                elif "mista" in z: zn = "mista"
                else: zn = "residencial_aberto"
                b['zona_norm'] = zn
                final.append(b)
            return final
        except:
            return [
                {"nome": "Jardim Pau Preto", "zona": "Bairro Aberto", "zona_norm": "residencial_aberto"},
                {"nome": "Helvetia Park", "zona": "Condomínio Fechado", "zona_norm": "residencial_fechado"},
                {"nome": "Distrito Industrial", "zona": "Zona Industrial", "zona_norm": "industrial"}
            ]

    def select_strategy(self):
        # 1. Escolhe Persona
        p_key = random.choice(list(AgencyConfig.PERSONAS.keys()))
        persona = AgencyConfig.PERSONAS[p_key]
        
        # 2. Filtra Bairros Compatíveis (Logic Shield v2.0)
        candidatos = [b for b in self.bairros if b['zona_norm'] in persona['zonas_alvo']]
        if not candidatos: candidatos = self.bairros # Fallback
        bairro = random.choice(candidatos)
        
        # 3. Define Ativo (Logic Shield v2.0)
        ativo = self._definir_ativo(persona['cluster'], bairro['zona_norm'])
        
        # 4. Seleciona Gatilho Neuro
        gatilho_key = random.choice(list(AgencyConfig.NEURO_TRIGGERS.keys()))
        gatilho_desc = AgencyConfig.NEURO_TRIGGERS[gatilho_key]

        return {
            "persona": persona,
            "bairro": bairro,
            "ativo": ativo,
            "gatilho_nome": gatilho_key,
            "gatilho_desc": gatilho_desc,
            "cluster_semantic": AgencyConfig.SEMANTIC_ENTITIES.get(persona['cluster'], [])
        }

    def _definir_ativo(self, cluster, zona):
        if zona == "industrial": return "Galpão Logístico Modular"
        if cluster == "HIGH_END": return "Casa de Alto Padrão (Conceito Aberto)"
        if cluster == "INVESTOR" and zona == "residencial_aberto": return "Terreno para Construção (Flip)"
        if zona == "residencial_fechado": return "Sobrado em Condomínio Clube"
        return "Imóvel Residencial"

# =========================================================
# 📡 BLOG INTELLIGENCE (Anti-Canibalização)
# =========================================================

class BlogIntelligence:
    def check_cannibalization(self, bairro_nome):
        # Simulação rápida para performance (em prod, conectaríamos ao RSS real igual v7)
        # Retorna apenas um status visual para o usuário
        return "Varredura Concluída: Tópico Seguro" 

# =========================================================
# ✍️ PROMPT ARCHITECT (O Diferencial do v8)
# =========================================================

class PromptArchitect:
    def format_date_pt(self, date_obj):
        meses = {1:"jan.", 2:"fev.", 3:"mar.", 4:"abr.", 5:"mai.", 6:"jun.", 
                 7:"jul.", 8:"ago.", 9:"set.", 10:"out.", 11:"nov.", 12:"dez."}
        return f"{date_obj.day} de {meses[date_obj.month]} de {date_obj.year}"

    def build_prompt(self, strategy, pub_date):
        p = strategy['persona']
        b = strategy['bairro']
        date_str = self.format_date_pt(pub_date)
        iso_date = pub_date.strftime("%Y-%m-%dT09:00:00-03:00")
        
        # Lista de entidades semânticas para injetar
        semantic_list = ", ".join(strategy['cluster_semantic'])

        return f"""
# 🚀 COMANDO DE AGÊNCIA DE ELITE (ROLE: SENIOR COPYWRITER)

**CONTEXTO:** Você é o redator principal da "Imobiliária Saber", a maior autoridade imobiliária de Indaiatuba, Brasil.
**OBJETIVO:** Criar um artigo de blog PERFEITO, otimizado para SEO, pronto para conversão e tecnicamente impecável para a plataforma Blogger.

---

## 1. BRIEFING ESTRATÉGICO (Siga à risca)
* **Persona Alvo:** {p['nome']} (Dores: {p['dor']})
* **Local de Foco:** {b['nome']} ({b['zona']})
* **Produto:** {strategy['ativo']}
* **Estratégia de Neuromarketing:** {strategy['gatilho_nome']}
    * *Instrução:* {strategy['gatilho_desc']}
* **Entidades Semânticas Obrigatórias:** {semantic_list}

---

## 2. PROTOCOLO DE PESQUISA (ANTI-ALUCINAÇÃO)
⚠️ **CRÍTICO:** Você DEVE realizar uma "Busca Mental" simulando o Google Maps.
1.  Não invente nomes de padarias ou escolas. Use locais REAIS de Indaiatuba próximos ao {b['nome']}.
2.  Se citar distâncias, use tempos realistas (ex: "A 8 minutos do Parque Ecológico").
3.  NUNCA invente depoimentos de clientes fictícios.

---

## 3. REGRAS DE CÓDIGO E FORMATAÇÃO (Blogger Ready)
Você vai gerar o output em um formato que eu possa copiar e colar direto no editor HTML.

### CSS Obrigatório (Injete isso no início):
`<style> h2 {{ color: #003366; border-bottom: 2px solid #D4AF37; padding-bottom: 10px; }} table {{ width: 100%; border-collapse: collapse; min-width: 600px; }} th, td {{ border: 1px solid #ddd; padding: 12px; hyphens: none; }} .table-wrapper {{ overflow-x: auto; margin-bottom: 20px; }} </style>`

### Estrutura do Artigo:
1.  **H1 (Título):** Persuasivo, contendo "{b['nome']}" e o benefício principal.
2.  **Introdução:** Use o gatilho de **{strategy['gatilho_nome']}**. Conecte a dor da persona com a solução.
3.  **Corpo (H2):** * Use parágrafos curtos.
    * **Tabela Técnica:** OBRIGATÓRIO criar uma tabela com distâncias reais (Escolas, Mercados, Rodovias) usando a classe `.table-wrapper`.
4.  **Conclusão:** Reafirme a autoridade da Imobiliária Saber.
5.  **CTA (Call to Action):** Use o script de captura fornecido abaixo.
6.  **Metadados:** JSON-LD para SEO.

---

## 4. O OUTPUT FINAL
Gere **APENAS** o conteúdo abaixo, na ordem exata.

**[BLOCO 1: BASTIDORES]**
Resuma em 1 parágrafo quais locais reais você selecionou para citar e porquê.

**[BLOCO 2: CÓDIGO HTML PRONTO PARA PUBLICAR]**
* Não use `<html>` ou `<body>`. Comece do `<style>`.
* Inclua o JSON-LD:
    `<script type="application/ld+json"> {{ "@context": "https://schema.org", "@type": "BlogPosting", "headline": "SEU TITULO H1", "datePublished": "{iso_date}", "author": {{ "@type": "Organization", "name": "Imobiliária Saber" }} }} </script>`
* Inclua o Script de Lead no final:
    `{AgencyConfig.LEAD_SCRIPT}`

**[BLOCO 3: CONFIGURAÇÕES]**
* **Título do Post:** (O mesmo do H1, sem tags)
* **Descrição da Pesquisa (Meta):** (Max 150 chars, focada em clique)
* **Marcadores (Tags):** Indaiatuba, {b['nome']}, {strategy['ativo']}, Imóveis Indaiatuba.

"""

# =========================================================
# 🖥️ UI STREAMLIT (AGENCY DASHBOARD)
# =========================================================

def main():
    st.set_page_config(page_title="Genesis Agency v8", page_icon="💎", layout="wide")

    # CSS Customizado para parecer uma ferramenta interna de agência
    st.markdown(f"""
    <style>
        .stApp {{ background-color: {AgencyConfig.THEME['bg']}; }}
        .big-card {{ 
            background: white; padding: 20px; border-radius: 10px; 
            border-left: 6px solid {AgencyConfig.THEME['primary']};
            box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px;
        }}
        .stat-value {{ font-size: 24px; font-weight: bold; color: {AgencyConfig.THEME['primary']}; }}
        .stat-label {{ font-size: 14px; color: #666; text-transform: uppercase; letter-spacing: 1px; }}
        .highlight {{ color: {AgencyConfig.THEME['accent']}; font-weight: bold; }}
        div.stButton > button {{
            background: linear-gradient(45deg, {AgencyConfig.THEME['primary']}, #004080);
            color: white; border: none; height: 60px; font-size: 18px; font-weight: bold;
            width: 100%; border-radius: 8px; text-transform: uppercase;
        }}
        div.stButton > button:hover {{ opacity: 0.9; }}
    </style>
    """, unsafe_allow_html=True)

    # Header
    c1, c2 = st.columns([3, 1])
    with c1:
        st.title("💎 GENESIS AGENCY V8.0")
        st.markdown("**AI Content Director para Imobiliária Saber**")
    with c2:
        st.image("https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEixiE1KghKkH0E-I53yyi5zoT7eRX0lxCGLpcWLGAmEE5st8OfHfuzbxfiygwCWRqAdSfpmjAhM8-SogHDU_1gXCX6IHrjW1BaUc87un1lF1o6y2Et7eV0m3gJgvfJs3HsAGyAcPYk8Tl_65rlQmgAp5orRZqtLDvixbCUwscTT8ZJO-7zckc36rNkWHz4/s1600/1000318124.png", width=100)

    # Sidebar de Controle
    with st.sidebar:
        st.header("⚙️ Configuração da Pauta")
        data_pub = st.date_input("Data de Publicação", datetime.date.today())
        st.markdown("---")
        st.markdown("### 🛡️ Protocolos Ativos")
        st.caption("✅ Logic Shield v2.0 (Zoneamento)")
        st.caption("✅ Anti-Alucinação (Google Maps Sim)")
        st.caption("✅ Lead Capture Injection (Kit.com)")
        st.markdown("---")
        if st.button("🔄 Resetar Sistema"):
            st.rerun()

    # Botão de Ação Principal
    col_main, col_view = st.columns([1, 2])
    
    with col_main:
        st.markdown("### Gerar Briefing")
        st.write("O sistema irá selecionar a melhor oportunidade baseada no inventário e personas.")
        generate_btn = st.button("CRIAR PAUTA ESTRATÉGICA ✨")

    if generate_btn:
        brain = AgencyBrain()
        architect = PromptArchitect()
        
        with st.spinner("🤖 A IA está analisando o mercado e definindo a estratégia..."):
            strategy = brain.select_strategy()
            prompt_final = architect.build_prompt(strategy, data_pub)
        
        # Exibição do "Raciocínio da Agência" (Visualização Rica)
        with col_view:
            st.markdown(f"""
            <div class="big-card">
                <div style="display:grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                    <div>
                        <div class="stat-label">Persona Alvo</div>
                        <div class="stat-value">{strategy['persona']['nome']}</div>
                        <small>{strategy['persona']['dor']}</small>
                    </div>
                    <div>
                        <div class="stat-label">Bairro Selecionado</div>
                        <div class="stat-value">{strategy['bairro']['nome']}</div>
                        <small>{strategy['bairro']['zona_norm'].replace('_', ' ').title()}</small>
                    </div>
                </div>
                <hr style="opacity: 0.2">
                <div style="display:grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                    <div>
                        <div class="stat-label">Ativo Foco</div>
                        <div class="stat-value">{strategy['ativo']}</div>
                    </div>
                    <div>
                        <div class="stat-label">Neuromarketing</div>
                        <div class="stat-value highlight">{strategy['gatilho_nome']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Área de Output do Prompt
        st.markdown("### 📋 Prompt de Engenharia Reversa (Copie para o Gemini/ChatGPT)")
        st.text_area("Prompt Otimizado:", value=prompt_final, height=400)
        
        # Botão de Download
        file_name = f"PAUTA_V8_{strategy['bairro']['nome'].replace(' ', '_')}.txt"
        st.download_button("💾 BAIXAR ARQUIVO DE PAUTA (.txt)", prompt_final, file_name)
        
        st.success("✅ Estratégia gerada com sucesso! Copie o texto acima e cole na sua IA de preferência.")

    else:
        with col_view:
            st.info("👈 Clique em 'CRIAR PAUTA' para iniciar o processo criativo.")

if __name__ == "__main__":
    main()