import streamlit as st
import random
import datetime
import unicodedata
import json
import urllib.request
import ssl
import re

# =========================================================
# CONFIGURAÇÃO: GENESIS V.65 (LOGIC SHIELD)
# =========================================================

class GenesisConfig:
    VERSION = "GENESIS V.65 (LOGIC SHIELD)"
    
    # Design System
    COLOR_PRIMARY = "#003366"   
    COLOR_ACCENT = "#FF4B4B"
    BLOG_URL = "https://blog.saber.imb.br"
    FUSO_PADRAO = "-03:00"

    # REGRAS DE SEGURANÇA & ANTI-ALUCINAÇÃO
    STRICT_GUIDELINES = [
        "NUNCA invente nomes de clientes (ex: Ricardo, Ana). Use 'O Cliente', 'O Investidor'.",
        "NUNCA invente profissões específicas se não solicitado.",
        "NUNCA crie depoimentos falsos entre aspas.",
        "USE linguagem hipotética: 'Imagine um cenário...', 'Para quem busca...'.",
        "OBRIGATÓRIO: Pesquise locais reais no Google Maps (Padarias, Escolas) antes de citar."
    ]

    # MATRIZ DE COMPATIBILIDADE (O ESCUDO LÓGICO)
    # Define quais tipos de imóveis podem existir em quais zonas.
    ZONING_RULES = {
        "VERTICAL": ["zona_mista", "zona_vertical", "centro"],
        "HORIZONTAL_FECHADO": ["residencial_fechado", "chacaras_fechado"],
        "HORIZONTAL_ABERTO": ["residencial_aberto", "mista", "centro"],
        "RURAL_CHACARA": ["chacaras_aberto", "chacaras_fechado"],
        "INDUSTRIAL": ["industrial", "logistica"],
        "COMERCIAL": ["mista", "centro", "avenida"]
    }

    # CATEGORIZAÇÃO DOS ATIVOS (IMÓVEIS)
    ASSET_TAGS = {
        "Casa em Condomínio de Luxo": "HORIZONTAL_FECHADO",
        "Sobrado Alto Padrão": "HORIZONTAL_FECHADO",
        "Mansão em Condomínio": "HORIZONTAL_FECHADO",
        "Casa de Rua (Bairro Aberto)": "HORIZONTAL_ABERTO",
        "Casa em Condomínio Club": "HORIZONTAL_FECHADO",
        "Sobrado Residencial": "HORIZONTAL_ABERTO",
        "Apartamento Moderno": "VERTICAL",
        "Studio/Loft": "VERTICAL",
        "Cobertura Duplex": "VERTICAL",
        "Terreno em Condomínio": "HORIZONTAL_FECHADO",
        "Lote para Construção": "HORIZONTAL_ABERTO",
        "Imóvel para Reforma (Flip)": "HORIZONTAL_ABERTO",
        "Sala Comercial": "COMERCIAL",
        "Laje Corporativa": "COMERCIAL",
        "Galpão Logístico": "INDUSTRIAL",
        "Terreno Industrial": "INDUSTRIAL",
        "Chácara de Lazer": "RURAL_CHACARA",
        "Sítio/Harley": "RURAL_CHACARA"
    }

    # PERSONAS (Atualizadas com Preferência de Zona)
    PERSONAS = {
        "EXODUS_SP_FAMILY": {
            "cluster": "FAMILY",
            "nome": "Família em Êxodo Urbano",
            "dor": "Medo da violência e trânsito caótico da capital.",
            "desejo": "Quintal, segurança de condomínio e escolas fortes.",
            "preferred_zones": ["residencial_fechado", "chacaras_fechado"]
        },
        "INVESTOR_ROI": {
            "cluster": "INVESTOR",
            "nome": "Investidor Analítico",
            "dor": "Medo da inflação e vacância do imóvel.",
            "desejo": "Rentabilidade real, valorização do m² e liquidez.",
            "preferred_zones": ["mista", "residencial_fechado", "zona_vertical"]
        },
        "REMOTE_WORKER": {
            "cluster": "FAMILY", 
            "nome": "Profissional Home Office",
            "dor": "Internet instável e falta de espaço dedicado.",
            "desejo": "Cômodo extra (Office), silêncio e vista livre.",
            "preferred_zones": ["residencial_fechado", "residencial_aberto"]
        },
        "HYBRID_COMMUTER": {
            "cluster": "URBAN",
            "nome": "O Pendular (SP-Indaiatuba)",
            "dor": "Cansaço da estrada e tempo perdido no trânsito.",
            "desejo": "Acesso imediato à Rodovia e praticidade (Apto/Casa).",
            "preferred_zones": ["zona_vertical", "residencial_fechado", "mista"]
        },
        "RETIREE_ACTIVE": {
            "cluster": "FAMILY",
            "nome": "Melhor Idade Ativa",
            "dor": "Solidão, escadas e distância de saúde.",
            "desejo": "Casa térrea, proximidade do Parque e farmácias.",
            "preferred_zones": ["residencial_aberto", "residencial_fechado"]
        },
        "FIRST_HOME": {
            "cluster": "URBAN",
            "nome": "Jovens (1º Imóvel)",
            "dor": "Orçamento limitado e medo de juros.",
            "desejo": "Entrada viável, baixo condomínio e potencial de venda.",
            "preferred_zones": ["zona_vertical", "residencial_aberto"]
        },
        "LUXURY_SEEKER": {
            "cluster": "HIGH_END",
            "nome": "Buscador de Exclusividade",
            "dor": "Falta de privacidade e padronização excessiva.",
            "desejo": "Arquitetura autoral, terrenos duplos e lazer privativo.",
            "preferred_zones": ["residencial_fechado", "chacaras_fechado"]
        },
        "PET_LOVER": {
            "cluster": "FAMILY",
            "nome": "Tutor de Grandes Animais",
            "dor": "Regras restritivas de condomínio e falta de grama.",
            "desejo": "Quintal privativo gramado e parques próximos.",
            "preferred_zones": ["residencial_aberto", "residencial_fechado", "chacaras_fechado"]
        },
        "MEDICAL_PRO": {
            "cluster": "HIGH_END",
            "nome": "Profissional de Saúde (Médicos)",
            "dor": "Rotina exaustiva e necessidade de silêncio.",
            "desejo": "Proximidade do HAOC/Santa Ignês e isolamento.",
            "preferred_zones": ["residencial_fechado"]
        },
        "LOGISTICS_MANAGER": {
            "cluster": "LOGISTICS",
            "nome": "Gestor de Logística/Empresário",
            "dor": "Custo logístico (Last Mile) e falta de manobra.",
            "desejo": "Galpão funcional e acesso à SP-75.",
            "preferred_zones": ["industrial", "logistica"]
        }
    }

    CONTENT_FORMATS = [
        "GUIA_DEFINITIVO", "LISTA_POLEMICA", "COMPARATIVO_TECNICO", 
        "CENARIO_ANALITICO", "CHECKLIST_TECNICO", "PREVISAO_MERCADO", 
        "ROTINA_SUGERIDA", "PERGUNTAS_RESPOSTAS", "INSIGHT_DE_CORRETOR", "DATA_DRIVEN"
    ]

    EMOTIONAL_TRIGGERS = ["MEDO_PERDA", "GANANCIA_LOGICA", "ALIVIO_IMEDIATO", "STATUS_ORGULHO", "SEGURANCA_TOTAL"]

# =========================================================
# UTILITÁRIOS
# =========================================================

def slugify(texto: str) -> str:
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
    texto = texto.lower()
    texto = texto.replace("/", "_").replace("\\", "_").replace(" ", "_")
    texto = re.sub(r'[^a-z0-9_]', '', texto)
    return texto

# =========================================================
# SCANNER DE BLOG (COM LINK REPAIR)
# =========================================================

class BlogScanner:
    def __init__(self, blog_url=GenesisConfig.BLOG_URL):
        self.feed_url = f"{blog_url}/feeds/posts/default?alt=json&max-results=50"
        self.posts_catalog = [] 
        self.status = "idle"

    def mapear(self):
        self.posts_catalog = []
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            
            with urllib.request.urlopen(self.feed_url, context=ctx, timeout=8) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode())
                    if "feed" in data and "entry" in data["feed"]:
                        for entry in data["feed"]["entry"]:
                            try:
                                titulo = entry["title"]["$t"]
                                links = entry.get("link", [])
                                href = None
                                for l in links:
                                    if l.get("rel") == "alternate":
                                        href = l.get("href")
                                        break
                                if href and titulo:
                                    self.posts_catalog.append({
                                        "title": titulo,
                                        "url": href,
                                        "slug": slugify(titulo)
                                    })
                            except Exception:
                                continue
            self.status = "success"
        except Exception:
            self.status = "error"

    def ja_publicado(self, nome_bairro: str) -> bool:
        slug = slugify(nome_bairro)
        for post in self.posts_catalog:
            if slug in post["slug"]: return True
        return False

    def get_recent_posts(self, limite=5):
        return self.posts_catalog[:limite]

# =========================================================
# CORE LOGIC: GENESIS ENGINE
# =========================================================

class GenesisData:
    def __init__(self):
        # Base de bairros Simulada (Se não houver JSON externo)
        # IMPORTANTE: A "zona_normalizada" deve bater com ZONING_RULES
        self.bairros_mock = [
            {"nome": "Jardim Pau Preto", "zona": "Bairro Aberto Tradicional", "zona_normalizada": "residencial_aberto"},
            {"nome": "Parque Ecológico (Marginal)", "zona": "Mista/Vertical", "zona_normalizada": "zona_vertical"},
            {"nome": "Helvetia Park", "zona": "Condomínio de Luxo", "zona_normalizada": "residencial_fechado"},
            {"nome": "Itaici", "zona": "Chácaras e Condomínios", "zona_normalizada": "chacaras_fechado"},
            {"nome": "Distrito Industrial", "zona": "Zona Industrial", "zona_normalizada": "industrial"},
            {"nome": "Jardim Esplanada", "zona": "Bairro Nobre Aberto", "zona_normalizada": "residencial_aberto"},
            {"nome": "Centro", "zona": "Comercial e Vertical", "zona_normalizada": "zona_vertical"},
            {"nome": "Swiss Park", "zona": "Condomínio Fechado", "zona_normalizada": "residencial_fechado"},
            {"nome": "Jardim Regente", "zona": "Bairro Misto", "zona_normalizada": "mista"}
        ]
        
        self.topics = {
            "CUSTO_VIDA": "Matemática Financeira",
            "SEGURANCA": "Segurança Patrimonial",
            "EDUCACAO": "Escolas e Filhos",
            "LOGISTICA": "Mobilidade Urbana",
            "LAZER": "Lifestyle e Gastronomia",
            "SAUDE": "Infraestrutura de Saúde",
            "INVESTIMENTO": "Análise de ROI",
            "ARQUITETURA": "Design e Tendências",
            "CONDOMINIO": "Vida Comunitária"
        }

    def get_bairros(self):
        # Tenta carregar arquivo, senão usa mock
        try:
            with open("bairros.json", "r", encoding="utf-8") as f:
                raw = json.load(f)
                # Normaliza
                final = []
                for b in raw:
                    b['slug'] = slugify(b['nome'])
                    if 'zona_normalizada' not in b:
                        # Fallback simples se não tiver tag no json
                        nome = b['nome'].lower()
                        if 'industrial' in nome: b['zona_normalizada'] = 'industrial'
                        elif 'condomínio' in nome: b['zona_normalizada'] = 'residencial_fechado'
                        elif 'chácara' in nome: b['zona_normalizada'] = 'chacaras_fechado'
                        else: b['zona_normalizada'] = 'residencial_aberto'
                    final.append(b)
                return final
        except:
            return self.bairros_mock

class LogicShield:
    """O Guardião da Coerência"""
    
    def validar_ativo(self, ativo, zona_bairro):
        """Retorna True se o ativo pode existir na zona."""
        tag_ativo = GenesisConfig.ASSET_TAGS.get(ativo)
        if not tag_ativo: return True # Se não tem tag, assume seguro (ou genérico)
        
        zonas_permitidas = GenesisConfig.ZONING_RULES.get(tag_ativo, [])
        return zona_bairro in zonas_permitidas

    def filtrar_ativos_para_bairro(self, lista_ativos, zona_bairro):
        """Retorna apenas os ativos da lista que cabem no bairro."""
        validos = []
        for a in lista_ativos:
            if self.validar_ativo(a, zona_bairro):
                validos.append(a)
        return validos

class GenesisEngine:
    def __init__(self):
        self.config = GenesisConfig()
        self.data = GenesisData()
        self.shield = LogicShield()
        self.scanner = BlogScanner()

    def run(self):
        self.scanner.mapear()
        recent_posts = self.scanner.get_recent_posts(5)
        
        # 1. Escolher Persona
        persona_key = random.choice(list(self.config.PERSONAS.keys()))
        persona = self.config.PERSONAS[persona_key]
        
        # 2. Filtrar Bairros pela Preferência da Persona
        bairros_disponiveis = self.data.get_bairros()
        bairros_candidatos = [
            b for b in bairros_disponiveis 
            if b['zona_normalizada'] in persona['preferred_zones']
        ]
        
        # Fallback se não achar bairro específico
        if not bairros_candidatos:
            bairros_candidatos = bairros_disponiveis

        # 3. Escolher Bairro
        bairro_selecionado = None
        modo = "CIDADE"
        
        # Tenta pegar um bairro inédito (não publicado no blog)
        random.shuffle(bairros_candidatos)
        ineditos = [b for b in bairros_candidatos if not self.scanner.ja_publicado(b['nome'])]
        
        if ineditos and random.random() < 0.7:
            bairro_selecionado = ineditos[0]
            modo = "BAIRRO"
            status_bairro = "Inédito (Ouro)"
        elif bairros_candidatos:
            bairro_selecionado = bairros_candidatos[0]
            modo = "BAIRRO"
            status_bairro = "Reciclagem (Prata)"
        else:
            modo = "CIDADE" # Falar da cidade no geral
            status_bairro = "Genérico"

        # 4. Definir Ativo Compatível (LOGIC SHIELD ATIVO)
        # Pega todos os ativos possíveis para o cluster da persona (ex: FAMILY -> Casas)
        ativos_cluster_raw = []
        for ativo_nome, tag in self.config.ASSET_TAGS.items():
            # Simplificação: Associação solta baseada em lógica de negócio
            # Aqui poderíamos ter um mapa reverso Cluster->Ativos, mas vamos inferir:
            if persona['cluster'] == "URBAN" and tag == "VERTICAL": ativos_cluster_raw.append(ativo_nome)
            if persona['cluster'] == "FAMILY" and "HORIZONTAL" in tag: ativos_cluster_raw.append(ativo_nome)
            if persona['cluster'] == "HIGH_END" and "FECHADO" in tag: ativos_cluster_raw.append(ativo_nome)
            if persona['cluster'] == "INVESTOR": ativos_cluster_raw.append(ativo_nome) # Investidor pega tudo
            if persona['cluster'] == "LOGISTICS" and tag == "INDUSTRIAL": ativos_cluster_raw.append(ativo_nome)
        
        if not ativos_cluster_raw: 
            ativos_cluster_raw = ["Imóvel Residencial"] # Fallback

        # AGORA O PULO DO GATO: FILTRA PELO BAIRRO SELECIONADO
        if bairro_selecionado:
            zona_bairro = bairro_selecionado['zona_normalizada']
            ativos_finais = self.shield.filtrar_ativos_para_bairro(ativos_cluster_raw, zona_bairro)
            
            if not ativos_finais:
                # Se filtrou tudo (ex: Investidor quer galpão mas bairro é residencial), troca o ativo
                ativos_finais = ["Imóvel na Região"] 
            
            ativo_definido = random.choice(ativos_finais)
        else:
            ativo_definido = random.choice(ativos_cluster_raw)

        return {
            "modo": modo,
            "bairro": bairro_selecionado,
            "persona": persona,
            "ativo": ativo_definido,
            "topico": random.choice(list(self.data.topics.values())),
            "formato": random.choice(self.config.CONTENT_FORMATS),
            "gatilho": random.choice(self.config.EMOTIONAL_TRIGGERS),
            "recent_posts": recent_posts,
            "debug_status": status_bairro
        }

# =========================================================
# PROMPT BUILDER
# =========================================================

class PromptBuilder:
    def build(self, d, data_pub, data_mod):
        p = d['persona']
        b = d['bairro']
        
        # Contexto Geográfico
        if d['modo'] == "BAIRRO":
            loc_context = f"Bairro: {b['nome']} ({b['zona']})"
            search_instruction = f"Localize 3 comércios reais num raio de 1.5km de {b['nome']}."
        else:
            loc_context = "Cidade: Indaiatuba (Foco Geral)"
            search_instruction = "Localize 3 pontos de referência no centro da cidade."

        # Linkagem
        links_txt = "Nenhum link recente disponível."
        if d['recent_posts']:
            links_txt = "\n".join([f"- {post['title']} ({post['url']})" for post in d['recent_posts']])

        return f"""
## GENESIS MAGNETO V.65 — AUTHORITY MODE
**ATENÇÃO IA:** Você está operando sob o protocolo **LOGIC SHIELD**.
Não invente dados. Não alucine localizações.

### 1. PERFIL & ALVO
* **Persona:** {p['nome']}
* **Dores:** {p['dor']}
* **Desejo:** {p['desejo']}
* **Tom de Voz:** Consultivo, Maduro, Autoridade Local.

### 2. DADOS DO IMÓVEL (BLINDAGEM ATIVA)
* **Ativo Selecionado:** {d['ativo']}
* **Localização:** {loc_context}
* **Validação Lógica:** O sistema confirmou que este tipo de imóvel ({d['ativo']}) REALMENTE existe nesta zona. Não desvie deste fato.

### 3. TEMA E FORMATO
* **Tema:** {d['topico']}
* **Formato:** {d['formato']}
* **Gatilho Emocional:** {d['gatilho']}

### 4. INSTRUÇÕES DE CONTEÚDO (SEARCH MODE)
Execute os seguintes passos para gerar o conteúdo:

1. **PESQUISA TOPOGRÁFICA (OBRIGATÓRIO):**
   {search_instruction}
   *Para cada local encontrado, explique a distância real (ex: "A 5 min de caminhada...").*

2. **LINKAGEM INTERNA INTELIGENTE:**
   Escolha 1 destes artigos recentes para citar contextualmente (use HTML `<a href...>`):
   {links_txt}

3. **TABELA DE DADOS (CSS PURO):**
   Gere uma tabela comparativa ou de dados usando este estilo inline OBRIGATÓRIO para evitar quebra de linhas:
   `<table style="width:100%; border-collapse:collapse;">` e nas células: `style="padding:10px; border:1px solid #ddd; white-space:nowrap;"`.

### 5. FORMATO DE SAÍDA (HTML P/ BLOGGER)
Entregue o resultado final seguindo esta estrutura EXATA:

1. **LOG DE PESQUISA:** (Liste brevemente o que encontrou no Google Maps).
2. **CÓDIGO HTML:** (O corpo do post em HTML limpo, com H2, P, UL).
3. **JSON-LD:** (Schema.org para BlogPosting dentro de um script tag).
4. **METADADOS:**
   - Título Sugerido (SEO Otimizado)
   - Meta Description (150 chars)
   - Tags (Comma separated)
   - Data de Publicação: {data_pub}

""".strip()

# =========================================================
# UI: STREAMLIT V3.0 (VISUAL RESTORED)
# =========================================================

def main():
    st.set_page_config(page_title="Genesis V.65", page_icon="🛡️", layout="wide")

    # CSS CUSTOMIZADO (RESTAURANDO A BELEZA)
    st.markdown("""
    <style>
        .main { background-color: #f4f6f9; }
        .stButton>button {
            width: 100%; height: 65px; border-radius: 10px;
            background: linear-gradient(90deg, #003366 0%, #004080 100%);
            color: white; font-size: 20px; font-weight: 600; border: none;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: all 0.3s;
        }
        .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 6px 12px rgba(0,0,0,0.15); }
        .metric-card {
            background: white; padding: 20px; border-radius: 12px;
            border-left: 5px solid #003366; box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        .metric-label { font-size: 14px; color: #666; text-transform: uppercase; letter-spacing: 1px; }
        .metric-value { font-size: 24px; font-weight: 700; color: #333; }
        .highlight-box {
            background-color: #e3f2fd; border: 1px solid #bbdefb;
            padding: 15px; border-radius: 8px; color: #0d47a1;
        }
    </style>
    """, unsafe_allow_html=True)

    # SIDEBAR
    with st.sidebar:
        st.title("🛡️ GENESIS CONTROL")
        st.caption(f"System: {GenesisConfig.VERSION}")
        st.markdown("---")
        data_escolhida = st.date_input("📅 Data de Publicação", datetime.date.today())
        st.markdown("---")
        st.info("**Logic Shield:** Ativo\n\nImpede combinações bizarras como 'Studio em Chácara'.")

    # HEADER
    st.markdown("## 🏙️ Gerador de Pautas Imobiliárias")
    st.markdown(f"**Saber Imobiliária** | Intelligence Engine V.65")

    # TABS
    tab_gerador, tab_manual, tab_logs = st.tabs(["🚀 Gerador de Prompt", "📘 Masterclass (Manual)", "⚙️ Logs do Sistema"])

    # --- ABA 1: GERADOR ---
    with tab_gerador:
        st.write("")
        col_btn, col_info = st.columns([1, 2])
        
        with col_btn:
            btn_gerar = st.button("DADOS, GIRO, AÇÃO! 🎲")
        
        with col_info:
            st.markdown("""
            <div style="padding: 10px; font-size: 14px; color: #555;">
            Clique para cruzar <b>Personas</b>, <b>Zoneamento</b> e <b>Tendências</b>.<br>
            O sistema validará a lógica automaticamente.
            </div>
            """, unsafe_allow_html=True)

        if btn_gerar:
            eng = GenesisEngine()
            
            with st.status("🔄 Processando Inteligência...", expanded=True) as status:
                st.write("📡 Conectando ao Blog Saber (Feed RSS)...")
                eng.run() # Executa a lógica
                dados = eng.run() # Re-executa para pegar os dados frescos (bug fix simples)
                
                st.write("🛡️ Aplicando Logic Shield (Validando Zona vs Imóvel)...")
                if dados['bairro']:
                    st.write(f"✅ Bairro '{dados['bairro']['nome']}' validado para '{dados['ativo']}'.")
                
                builder = PromptBuilder()
                hoje = datetime.datetime.now().strftime("%Y-%m-%d")
                d_pub = data_escolhida.strftime("%Y-%m-%d")
                prompt = builder.build(dados, d_pub, hoje)
                
                status.update(label="Prompt Gerado com Sucesso!", state="complete", expanded=False)

            # EXIBIÇÃO VISUAL (METRIC CARDS)
            st.markdown("<br>", unsafe_allow_html=True)
            c1, c2, c3, c4 = st.columns(4)
            
            def card(col, label, value):
                col.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                </div>
                """, unsafe_allow_html=True)

            card(c1, "Persona Alvo", dados['persona']['nome'].split(" ")[0])
            card(c2, "Cluster", dados['persona']['cluster'])
            local_nome = dados['bairro']['nome'] if dados['bairro'] else "Indaiatuba (Geral)"
            card(c3, "Localização", local_nome)
            card(c4, "Ativo Blindado", dados['ativo'].split(" ")[0])

            st.markdown("---")
            
            # AREA DO PROMPT
            col_txt, col_down = st.columns([3, 1])
            with col_txt:
                st.subheader("📋 Prompt Final")
                st.text_area("Copie e cole na IA", value=prompt, height=400)
            
            with col_down:
                st.markdown("<br><br>", unsafe_allow_html=True)
                st.download_button(
                    label="💾 Baixar .txt",
                    data=prompt,
                    file_name=f"pauta_{slugify(dados['topico'])}.txt",
                    mime="text/plain"
                )
                st.info("Dica: Use no Claude 3.5 Sonnet ou GPT-4o.")

    # --- ABA 2: MANUAL MASTERCLASS ---
    with tab_manual:
        st.markdown("""
        # 📘 Manual de Operações: Genesis V.65
        
        Bem-vindo ao **Painel de Controle de Conteúdo**. Este sistema não apenas "cria ideias", ele projeta estratégias baseadas em dados reais e lógica de mercado.

        ---

        ### 🧠 O Cérebro (Logic Shield)
        Nas versões anteriores, a IA podia cometer erros como oferecer um *Apartamento Studio* em um bairro de *Chácaras*.
        A V.65 introduziu o **Logic Shield**:
        1. O sistema escolhe a Persona.
        2. O sistema verifica quais zonas a Persona aceita.
        3. O sistema escolhe um Bairro compatível.
        4. **CRUCIAL:** O sistema filtra a lista de imóveis. Se o bairro é "Residencial Fechado", ele remove "Galpão" e "Loft da lista", deixando apenas Casas.

        ---

        ### 🛠️ Protocolos de Uso
        
        #### Protocolo Alpha: Geração
        1. Defina a **Data de Publicação** na barra lateral.
        2. Clique no botão **DADOS, GIRO, AÇÃO**.
        3. Observe os "Cards" para ver o resumo da estratégia.

        #### Protocolo Beta: Execução na IA
        1. Copie o prompt gerado.
        2. Cole no **ChatGPT (GPT-4)** ou **Claude (Opus/Sonnet)**.
        3. **Não peça para reescrever imediatamente.** Leia o resultado. A IA foi instruída a buscar dados reais no Google Maps.
        4. Verifique se os links (se houver) estão funcionando.

        ---

        ### 🚨 Troubleshooting (Resolução de Problemas)
        
        | Problema | Causa Provável | Solução |
        | :--- | :--- | :--- |
        | **Prompt sem links internos** | O Blog pode estar instável ou bloqueando o scanner. | O sistema gera o prompt mesmo sem links (modo fallback). |
        | **Bairro "Genérico"** | As restrições da Persona foram muito altas e não achou bairro específico no mock. | O sistema cria um post sobre a cidade (macro). |
        | **Erro de Data** | Formato inválido. | Use o calendário da barra lateral. |

        """)

    # --- ABA 3: LOGS ---
    with tab_logs:
        st.write("System Logs & Raw Data:")
        if 'dados' in locals():
            st.json(dados)
        else:
            st.warning("Nenhum dado gerado nesta sessão ainda.")

if __name__ == "__main__":
    main()