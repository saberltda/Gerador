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
# ⛔ ZONA DE SEGURANÇA MÁXIMA (DO NOT DELETE) ⛔
# As "Leis da Física" deste software. Não alterar sob pena de quebra do sistema.
# ==============================================================================

class ImmutableRules:
    # REGRA 01: OBRIGATÓRIO consultar as últimas 9999 postagens para evitar canibalização.
    MAX_RESULTS_SCAN = 9999
    
    # REGRA 02: Estrutura Técnica HTML (Blogger).
    REGRAS_TECNICAS = """
### ⛔ PROTOCOLO TÉCNICO DE SEGURANÇA (OBRIGATÓRIO)
Você está gerando um FRAGMENTO DE HTML para ser inserido dentro de um post do Blogger.
I. **PROIBIDO** usar: `<!DOCTYPE html>`, `<html>`, `<head>`, `<body>`.
II. **PROIBIDO** incluir tags `<meta>` ou `<title>`.
III. Comece DIRETAMENTE com o conteúdo visível (ex: `<style>`, `<h2>`, `<p>`, `<div>`).
IV. A violação destas regras quebrará o template do site.

### 📋 CHECKLIST DE ENTREGA (ORDEM IMUTÁVEL)
Sua resposta final deve seguir EXATAMENTE esta ordem numérica (1 a 8):
1. LOG DE BASTIDORES: (Estratégia usada)
2. BLOCKCODE (HTML Puro + JSON-LD embutido):
   - SEM tags de estrutura (html/body).
   - O JSON-LD deve estar dentro deste bloco HTML.
3. TÍTULO: (Apenas o título final, sem aspas)
4. MARCADORES: (Tags SEO separadas por vírgula)
5. DATA: (Formato: DD de mmm. de AAAA)
6. LOCAL: Indaiatuba
7. DESCRIÇÃO: (Meta description focada na dor)
8. IMAGEM: (Prompt para IA generativa)
"""

    # REGRA 03: Design de Tabelas Anti-Quebra.
    REGRAS_TABELA = """
### 🎨 REGRAS DE DESIGN DE TABELAS (ANTI-QUEBRA)
Para garantir leitura mobile, siga este CSS Inline RIGOROSAMENTE:
1. **Wrapper:** Envolva a tabela em `<div style="overflow-x: auto; width: 100%; margin-bottom: 20px;">`.
2. **Tag Table:** Use `<table style="width: 100%; min-width: 600px; border-collapse: collapse;">`.
3. **Células (TH/TD):** EM TODAS AS CÉLULAS, aplique: 
   `style="padding: 12px; border: 1px solid #cccccc; word-break: keep-all; hyphens: none;"`
"""

# =========================================================
# CONFIGURAÇÃO GERAL
# =========================================================

class GenesisConfig:
    VERSION = "APP_GERADOR_7 (JSON CONNECTED)"
    COLOR_PRIMARY = "#003366"   
    COLOR_ACCENT = "#FF4B4B"
    BLOG_URL = "https://blog.saber.imb.br"
    FUSO_PADRAO = "-03:00"

    FORBIDDEN_WORDS = [
        "sonho", "sonhos", "oportunidade única", "excelente localização",
        "ótimo investimento", "preço imperdível", "lindo", "maravilhoso",
        "tranquilo", "localização privilegiada", "região privilegiada",
        "venha conferir", "agende sua visita", "fale com nossos consultores",
        "paraíso", "espetacular", "top"
    ]

    MANDATORY_TERMS = [
        "Troque 'Lugar calmo' por 'Isolamento acústico' ou 'Baixo adensamento'",
        "Troque 'Ótimo investimento' por 'Liquidez', 'Vetor de crescimento' ou 'Reserva de valor'",
        "Troque 'Perto de tudo' por 'Logística urbana' ou 'Tempo de deslocamento'"
    ]

    PERSONAS = {
        "EXODUS_SP_FAMILY": {
            "cluster": "FAMILY", "nome": "Família em Êxodo Urbano",
            "dor": "Medo da violência e trânsito caótico da capital.",
            "desejo": "Quintal, segurança de condomínio e escolas fortes.",
            "preferred_zones": ["residencial_fechado", "chacaras_fechado"],
            "template_mode": "ANALISTA"
        },
        "INVESTOR_ROI": {
            "cluster": "INVESTOR", "nome": "Investidor Analítico",
            "dor": "Medo da inflação e vacância do imóvel.",
            "desejo": "Rentabilidade real, valorização do m² e liquidez.",
            "preferred_zones": ["mista", "residencial_fechado", "zona_vertical", "industrial"],
            "template_mode": "ANALISTA"
        },
        "REMOTE_WORKER": {
            "cluster": "FAMILY", "nome": "Profissional Home Office",
            "dor": "Internet instável e falta de espaço dedicado.",
            "desejo": "Cômodo extra (Office), silêncio e vista livre.",
            "preferred_zones": ["residencial_fechado", "residencial_aberto"],
            "template_mode": "LIFESTYLE"
        },
        "LUXURY_SEEKER": {
            "cluster": "HIGH_END", "nome": "Buscador de Exclusividade",
            "dor": "Falta de privacidade e padronização excessiva.",
            "desejo": "Arquitetura autoral, terrenos duplos e lazer privativo.",
            "preferred_zones": ["residencial_fechado", "chacaras_fechado"],
            "template_mode": "LIFESTYLE"
        },
        "LOGISTICS_MANAGER": {
            "cluster": "LOGISTICS", "nome": "Gestor de Logística/Empresário",
            "dor": "Custo logístico (Last Mile) e falta de manobra.",
            "desejo": "Galpão funcional e acesso à SP-75.",
            "preferred_zones": ["industrial", "logistica"],
            "template_mode": "ORACULO"
        },
        "FIRST_HOME": {
            "cluster": "URBAN", "nome": "Jovens (1º Imóvel)",
            "dor": "Orçamento limitado e medo de juros.",
            "desejo": "Entrada viável, baixo condomínio e potencial de venda.",
            "preferred_zones": ["zona_vertical", "residencial_aberto"],
            "template_mode": "ORACULO"
        }
    }

    ASSETS = {
        "HIGH_END": ["Casa Alto Padrão em Condomínio", "Mansão em Condomínio", "Terreno de Luxo"],
        "FAMILY": ["Casa de Rua (Bairro Aberto)", "Sobrado Residencial", "Casa Térrea"],
        "URBAN": ["Apartamento Central", "Studio/Loft", "Cobertura Duplex"],
        "INVESTOR": ["Terreno para Incorporação", "Lote em Condomínio (Flip)", "Imóvel Comercial"],
        "LOGISTICS": ["Galpão Logístico AAA", "Terreno Industrial", "Centro de Distribuição"],
        "CHACARAS": ["Chácara de Lazer", "Sítio", "Haras Privativo"]
    }

# =========================================================
# UTILITÁRIOS
# =========================================================

def slugify(texto: str) -> str:
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
    texto = texto.lower()
    texto = re.sub(r'[^a-z0-9_]', '', texto.replace(" ", "_"))
    return texto

# =========================================================
# DADOS GEOGRÁFICOS (JSON LOADER)
# =========================================================

class GenesisData:
    def __init__(self):
        self.filename = "bairros.json"
        
    def _normalizar_zona(self, descricao_zona):
        """Traduz a descrição do JSON para a chave lógica do sistema."""
        d = descricao_zona.lower()
        if "industrial" in d or "empresarial" in d: return "industrial"
        if "chácaras fechado" in d: return "chacaras_fechado"
        if "residencial fechado" in d: return "residencial_fechado"
        if "residencial aberto" in d: return "residencial_aberto"
        if "zona mista" in d or "vertical" in d: return "zona_vertical"
        if "chácaras" in d: return "chacaras_aberto"
        return "residencial_aberto" # Default seguro

    def get_bairros(self):
        status = "MOCK (Arquivo não encontrado)"
        bairros_finais = []

        try:
            if os.path.exists(self.filename):
                with open(self.filename, "r", encoding="utf-8") as f:
                    raw_data = json.load(f)
                    
                for b in raw_data:
                    # Enriquecer com a normalização para o Logic Shield funcionar
                    b['zona_normalizada'] = self._normalizar_zona(b.get('zona', ''))
                    bairros_finais.append(b)
                status = f"JSON CARREGADO ({len(bairros_finais)} bairros)"
            else:
                raise FileNotFoundError

        except Exception as e:
            # Fallback para Mock se der erro ou não achar arquivo
            bairros_finais = [
                {"nome": "Jardim do Sol", "zona": "Bairro Residencial Aberto", "zona_normalizada": "residencial_aberto"},
            ]
            status = f"ERRO NO JSON ({str(e)}) - Usando Mock"

        return bairros_finais, status

# =========================================================
# PLANO DIRETOR (LÓGICA BLINDADA)
# =========================================================

class PlanoDiretor:
    def validar_e_corrigir(self, cluster_key, ativo_sugerido, bairro_obj):
        zona_norm = bairro_obj.get("zona_normalizada", "residencial_aberto")
        ativo_final = ativo_sugerido
        correcao_nota = None
        status = "OK"

        # REGRA INDUSTRIAL
        if zona_norm == "industrial":
            termos_proibidos = ["Casa", "Sobrado", "Apartamento", "Mansão", "Condomínio Fechado"]
            if any(t in ativo_sugerido for t in termos_proibidos):
                status = "CORRIGIDO"
                if cluster_key == "INVESTOR":
                    ativo_final = "Terreno Industrial/Comercial"
                else:
                    ativo_final = "Galpão Logístico Modular"
                correcao_nota = f"⚠️ BLOQUEIO DE ZONEAMENTO: '{ativo_sugerido}' é ilegal em Zona Industrial. Alterado para '{ativo_final}'."

        # REGRA CONDOMÍNIO FECHADO
        elif zona_norm == "residencial_fechado":
            termos_proibidos = ["Galpão", "Loja", "Comércio", "Aberto", "Casa de Rua"]
            if any(t in ativo_sugerido for t in termos_proibidos):
                status = "CORRIGIDO"
                ativo_final = "Casa em Condomínio de Alto Padrão"
                correcao_nota = f"⚠️ BLOQUEIO DE PRIVACIDADE: '{ativo_sugerido}' não existe dentro de Condomínios. Alterado para '{ativo_final}'."

        # REGRA VERTICALIZAÇÃO
        elif zona_norm == "zona_vertical":
            if "Chácara" in ativo_sugerido or "Galpão" in ativo_sugerido:
                status = "CORRIGIDO"
                ativo_final = "Apartamento de Alto Padrão"
                correcao_nota = f"⚠️ BLOQUEIO URBANO: '{ativo_sugerido}' incompatível com Zona Vertical. Alterado para '{ativo_final}'."

        return status, ativo_final, correcao_nota

# =========================================================
# SCANNER DE BLOG (REGRA 9999 POSTS)
# =========================================================

class BlogScanner:
    def __init__(self, blog_url=GenesisConfig.BLOG_URL):
        self.feed_url = f"{blog_url}/feeds/posts/default?alt=json&max-results={ImmutableRules.MAX_RESULTS_SCAN}"
        self.posts_history = [] 

    def mapear(self):
        self.posts_history = []
        status_msg = "Inicializando..."
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            
            with urllib.request.urlopen(self.feed_url, context=ctx, timeout=10) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode())
                    if "feed" in data and "entry" in data["feed"]:
                        for entry in data["feed"]["entry"]:
                            try:
                                titulo = entry["title"]["$t"]
                                links = entry.get("link", [])
                                href = next((l["href"] for l in links if l.get("rel") == "alternate"), "#")
                                
                                self.posts_history.append({
                                    "title": titulo,
                                    "url": href,
                                    "slug": slugify(titulo)
                                })
                            except Exception:
                                continue
            status_msg = f"Sucesso: {len(self.posts_history)} posts indexados."
        except Exception as e:
            status_msg = f"Modo Offline (Erro: {str(e)})"
        
        return status_msg

    def verificar_canibalizacao(self, nome_bairro, topico):
        slug_bairro = slugify(nome_bairro)
        slug_topico = slugify(topico)
        conflitos = []
        for post in self.posts_history:
            if slug_bairro in post['slug']:
                conflitos.append(post)
            elif slug_topico in post['slug'] and len(slug_topico) > 4:
                conflitos.append(post)
        return conflitos[:5]

    def get_recent_titles(self, limit=10):
        return [p['title'] for p in self.posts_history[:limit]]

# =========================================================
# ENGINE PRINCIPAL
# =========================================================

class GenesisEngine:
    def __init__(self):
        self.config = GenesisConfig()
        self.data = GenesisData()
        self.plano = PlanoDiretor()
        self.scanner = BlogScanner()

    def run(self):
        scan_status = self.scanner.mapear()
        bairros_lista, dados_status = self.data.get_bairros()
        
        # 1. Escolher Persona e Cluster
        persona_key = random.choice(list(self.config.PERSONAS.keys()))
        persona = self.config.PERSONAS[persona_key]
        cluster = persona['cluster']
        
        # 2. Filtrar Bairros (Agora usando a lista do JSON)
        candidatos = [b for b in bairros_lista if b['zona_normalizada'] in persona['preferred_zones']]
        
        # Fallback: Se não achar bairro compatível, pega qualquer um
        if not candidatos: candidatos = bairros_lista 
        
        # 3. Escolher Bairro
        if candidatos:
            bairro = random.choice(candidatos)
        else:
            # Fallback extremo se a lista estiver vazia
            bairro = {"nome": "Indaiatuba (Geral)", "zona": "Cidade", "zona_normalizada": "residencial_aberto"}
        
        # 4. Definir Ativo Inicial
        ativos_possiveis = self.config.ASSETS.get(cluster, ["Imóvel Residencial"])
        ativo_inicial = random.choice(ativos_possiveis)
        
        # 5. APLICAR PLANO DIRETOR
        status_plano, ativo_blindado, nota_correcao = self.plano.validar_e_corrigir(cluster, ativo_inicial, bairro)

        # 6. VERIFICAR CANIBALIZAÇÃO
        topico = random.choice(["Custo de Vida", "Segurança", "Educação", "Valorização", "Qualidade de Vida"])
        posts_conflitantes = self.scanner.verificar_canibalizacao(bairro['nome'], topico)
        recent_posts = self.scanner.get_recent_titles(8)

        return {
            "modo": "BAIRRO",
            "template_mode": persona['template_mode'],
            "bairro": bairro,
            "persona": persona,
            "ativo": ativo_blindado,
            "nota_correcao": nota_correcao,
            "topico": topico,
            "gatilho": random.choice(["Medo da Perda", "Ganância Lógica", "Exclusividade", "Segurança Familiar"]),
            "scan_status": scan_status,
            "dados_status": dados_status,
            "conflitos": posts_conflitantes,
            "recent_posts": recent_posts
        }

# =========================================================
# PROMPT BUILDER
# =========================================================

class PromptBuilder:
    def _generate_json_ld(self, d, data_pub):
        return f"""
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "TÍTULO DO POST AQUI",
  "description": "RESUMO SEO AQUI",
  "author": {{
    "@type": "Organization",
    "name": "Imobiliária Saber"
  }},
  "datePublished": "{data_pub}",
  "mainEntityOfPage": "https://blog.saber.imb.br"
}}
</script>
"""

    def build(self, d, data_pub):
        json_ld = self._generate_json_ld(d, data_pub)
        forbidden = ", ".join(GenesisConfig.FORBIDDEN_WORDS)
        mandatory = "\n".join(GenesisConfig.MANDATORY_TERMS)
        
        # Anti-Canibalização Contextual
        anti_cannibal_text = "Nenhum conflito direto detectado."
        if d['conflitos']:
            lista_conflitos = "\n".join([f"- {p['title']} ({p['url']})" for p in d['conflitos']])
            anti_cannibal_text = f"""
🚨 **ALERTA DE CANIBALIZAÇÃO:**
Os seguintes artigos JÁ EXISTEM sobre este tema/bairro. Você DEVE abordar um ângulo completamente diferente.
{lista_conflitos}
"""

        recent_posts_text = "\n".join([f"- {t}" for t in d['recent_posts']])

        base_header = f"""
## {GenesisConfig.VERSION} — AUTHORITY MODE
**DATA DE PUBLICAÇÃO:** {data_pub}

{ImmutableRules.REGRAS_TECNICAS}

---

### 🛡️ PROTOCOLO DE CONTEÚDO
1. **VOCABULÁRIO PROIBIDO:** {forbidden}.
2. **SUBSTITUIÇÕES OBRIGATÓRIAS:** {mandatory}
3. **HISTÓRICO RECENTE DO BLOG (NÃO REPITA ESTES TEMAS):**
{recent_posts_text}

{anti_cannibal_text}

---
"""
        
        template = ""
        if d['template_mode'] == "ANALISTA":
            template = f"""
### 🧠 MODO: O ANALISTA (Racional & Matemático)
**Persona:** {d['persona']['nome']} (Cluster: {d['persona']['cluster']})
**Tom de Voz:** Frio, Calculado, Baseado em Dados.
**Missão:** Provar por A + B que {d['bairro']['nome']} é a escolha correta.

**Estrutura do Artigo:**
1. **O Diagnóstico:** A dor validada ({d['persona']['dor']}).
2. **A Matemática:** Comparativo de custo/benefício.
3. **O Ativo Blindado:** Detalhes técnicos sobre {d['ativo']}.
4. **Tabela de Prova:** Comparativo de preços ou distâncias.
"""

        elif d['template_mode'] == "LIFESTYLE":
            template = f"""
### 🌿 MODO: CURADOR DE LIFESTYLE (Inspiracional)
**Persona:** {d['persona']['nome']} (Cluster: {d['persona']['cluster']})
**Tom de Voz:** Sofisticado, Descritivo.
**Missão:** Conectar o hobby/desejo ({d['persona']['desejo']}) com a realidade do imóvel.

**Regra 80/20:**
- 80% do texto sobre o Estilo de Vida.
- 20% conectando como o imóvel ({d['ativo']}) viabiliza isso em {d['bairro']['nome']}.
"""

        else: # ORACULO
            template = f"""
### 🔮 MODO: ORÁCULO LOCAL (Guia & Autoridade)
**Persona:** {d['persona']['nome']}
**Tom de Voz:** Enciclopédico, Seguro.
**Missão:** Ensinar tudo sobre {d['bairro']['nome']} e {d['ativo']}.

**Estrutura:**
1. **Raio-X do Local:** Infraestrutura real num raio de 1.5km.
2. **Perfil de Morador:** Quem vive aqui?
3. **O Ativo:** Por que {d['ativo']} funciona nesta zona.
"""

        footer = f"""
---
### 📝 DADOS PARA O ARTIGO
* **Bairro Alvo:** {d['bairro']['nome']} ({d['bairro']['zona']})
* **Imóvel/Ativo:** {d['ativo']}
* **Tema Central:** {d['topico']}
* **Gatilho Emocional:** {d['gatilho']}

{ImmutableRules.REGRAS_TABELA}

### 📋 CHECKLIST DE ENTREGA (JSON EMBUTIDO)
Sua resposta final deve conter EXATAMENTE:
1. **LOG DE BASTIDORES:** (Estratégia usada).
2. **BLOCKCODE HTML:** - O JSON-LD abaixo deve ser copiado e colado DENTRO do seu HTML (no início):
   {json_ld}
   - O restante do artigo em HTML puro (h2, p, ul, table).
3. **TÍTULO:** (Sem aspas)
4. **MARCADORES:**
5. **DATA:**
6. **LOCAL:**
7. **DESCRIÇÃO (Meta):**
8. **IMAGEM:**
"""
        return base_header + template + footer

# =========================================================
# UI: STREAMLIT
# =========================================================

def main():
    st.set_page_config(page_title="Genesis App 7", page_icon="🛡️", layout="wide")

    st.markdown(f"""
    <style>
        .main {{ background-color: #f4f6f9; }}
        .stButton>button {{
            width: 100%; height: 70px; border-radius: 8px;
            background: linear-gradient(90deg, #003366 0%, #00509e 100%);
            color: white; font-size: 22px; font-weight: 700; border: none;
            box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        }}
        .metric-card {{
            background: white; padding: 15px; border-radius: 10px;
            border-left: 5px solid {GenesisConfig.COLOR_ACCENT}; box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }}
    </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.title("🛡️ APP GERADOR 7")
        st.caption("JSON Connected Edition")
        st.markdown("---")
        data_escolhida = st.date_input("📅 Data de Publicação", datetime.date.today())
        
        st.success("**STATUS DO SISTEMA:**")
        st.markdown("- ✅ Regras Imutáveis: ATIVAS")
        st.markdown(f"- ✅ Scan Anti-Canibal: {ImmutableRules.MAX_RESULTS_SCAN} Posts")

    st.markdown("## 🏙️ Gerador de Pautas Blindadas")
    
    col_btn, col_info = st.columns([1, 2])
    with col_btn:
        st.write("")
        btn_gerar = st.button("GERAR PAUTA")
    
    with col_info:
        st.info("O sistema carrega 'bairros.json', consulta o blog e aplica o Logic Shield.")

    if btn_gerar:
        eng = GenesisEngine()
        builder = PromptBuilder()
        
        with st.status("🔄 Processando Inteligência...", expanded=True) as status:
            dados = eng.run()
            
            st.write(f"📁 Bairros: {dados['dados_status']}")
            st.write(f"📡 Blog Scan: {dados['scan_status']}")
            
            if dados['conflitos']:
                st.warning(f"⚠️ {len(dados['conflitos'])} Conflitos de tema encontrados.")
            
            d_pub_str = data_escolhida.strftime("%Y-%m-%dT09:00:00-03:00")
            prompt_final = builder.build(dados, d_pub_str)
            
            status.update(label="Prompt Gerado com Sucesso!", state="complete", expanded=False)

        # Cards
        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f"<div class='metric-card'><b>PERSONA</b><br>{dados['persona']['nome']}</div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='metric-card'><b>BAIRRO</b><br>{dados['bairro']['nome']}</div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='metric-card'><b>ATIVO</b><br>{dados['ativo']}</div>", unsafe_allow_html=True)
        c4.markdown(f"<div class='metric-card'><b>RISCO CANIBAL</b><br>{'ALTO' if dados['conflitos'] else 'BAIXO'}</div>", unsafe_allow_html=True)

        if dados.get("nota_correcao"):
            st.error(f"🚨 **INTERVENÇÃO DO PLANO DIRETOR:** {dados['nota_correcao']}")

        # Output
        st.markdown("### 📋 Prompt Final")
        st.text_area("Copie para a IA:", value=prompt_final, height=450)
        st.download_button("💾 Baixar Pauta (.txt)", prompt_final, "pauta_gerador_7.txt")

if __name__ == "__main__":
    main()