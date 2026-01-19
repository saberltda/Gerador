import streamlit as st
import random
import datetime
import copy
import unicodedata
import json
import urllib.request
import ssl
import sys
import os
import re
from collections import defaultdict

# =========================================================
# CONFIGURAÇÃO: GENESIS V.50.1 (PURE SEARCH MODE)
# =========================================================

class GenesisConfig:
    VERSION = "GERADOR V.50.1 (PURE SEARCH)"

    # Design System & URLs
    COLOR_PRIMARY = "#003366"   
    BLOG_URL = "https://blog.saber.imb.br"
    FUSO_PADRAO = "-03:00"

    # REGRAS DE SEGURANÇA
    STRICT_GUIDELINES = [
        "NUNCA invente nomes de clientes (ex: Ricardo, Ana, João).",
        "NUNCA invente profissões específicas para o personagem.",
        "NUNCA crie depoimentos falsos.",
        "USE linguagem hipotética: 'Imagine um investidor...', 'Para quem trabalha em...'.",
        "FALE diretamente com o leitor ('Você').",
        "OBRIGATÓRIO: Pesquise locais reais no Google Maps antes de citar. Não use exemplos genéricos."
    ]

    RULES = {
        "FORBIDDEN_WORDS": [
            "sonho", "sonhos", "oportunidade única", "excelente localização",
            "ótimo investimento", "preço imperdível", "lindo", "maravilhoso",
            "tranquilo", "localização privilegiada", "região privilegiada",
            "venha conferir", "agende sua visita", "paraíso", "espetacular",
            "imóvel dos sonhos", "toque de requinte"
        ]
    }

    # MATRIZ SEMÂNTICA (LSI KEYWORDS)
    VOCABULARY_MATRIX = {
        "SILENCIO": [
            "Isolamento acústico natural", "Baixo adensamento populacional", 
            "Privacidade sonora", "Refúgio urbano", "Atmosfera de descompressão"
        ],
        "INVESTIMENTO": [
            "Alta liquidez", "Vetor de crescimento urbano", "Reserva de valor", 
            "Proteção patrimonial", "Ativo imobiliário resiliente"
        ],
        "LOCALIZACAO": [
            "Logística estratégica", "Conectividade viária", "Acesso rápido a hubs", 
            "Otimização de deslocamento", "Ponto focal urbano"
        ]
    }

    # =====================================================
    # 1. MATRIZ DE PERSONAS (ARQUÉTIPOS)
    # =====================================================
    PERSONAS = {
        "EXODUS_SP_FAMILY": {
            "cluster_ref": "FAMILY",
            "nome": "Família em Êxodo Urbano",
            "dor": "Medo da violência e trânsito caótico da capital.",
            "desejo": "Quintal, segurança de condomínio e escolas fortes."
        },
        "INVESTOR_ROI": {
            "cluster_ref": "INVESTOR",
            "nome": "Investidor Analítico",
            "dor": "Medo da inflação e vacância do imóvel.",
            "desejo": "Rentabilidade real, valorização do m² e liquidez."
        },
        "REMOTE_WORKER": {
            "cluster_ref": "FAMILY", 
            "nome": "Profissional Home Office",
            "dor": "Internet instável e falta de espaço dedicado para trabalho.",
            "desejo": "Cômodo extra (Office), silêncio e vista livre."
        },
        "HYBRID_COMMUTER": {
            "cluster_ref": "URBAN",
            "nome": "O Pendular (SP-Indaiatuba)",
            "dor": "Cansaço da estrada e tempo perdido no trânsito.",
            "desejo": "Acesso imediato à Rodovia e serviços rápidos."
        },
        "RETIREE_ACTIVE": {
            "cluster_ref": "FAMILY",
            "nome": "Melhor Idade Ativa",
            "dor": "Solidão, escadas e distância de serviços de saúde.",
            "desejo": "Casa térrea, proximidade do Parque e farmácias."
        },
        "FIRST_HOME": {
            "cluster_ref": "URBAN",
            "nome": "Jovens (1º Imóvel)",
            "dor": "Orçamento limitado e medo de financiamento longo.",
            "desejo": "Entrada viável, baixo condomínio e potencial de venda futura."
        },
        "LUXURY_SEEKER": {
            "cluster_ref": "HIGH_END",
            "nome": "Buscador de Exclusividade",
            "dor": "Falta de privacidade e padronização excessiva.",
            "desejo": "Arquitetura autoral, terrenos duplos e lazer privativo."
        },
        "PET_LOVER": {
            "cluster_ref": "FAMILY",
            "nome": "Tutor de Grandes Animais",
            "dor": "Regras restritivas de condomínio e falta de espaço verde.",
            "desejo": "Quintal privativo gramado e parques próximos."
        },
        "MEDICAL_PRO": {
            "cluster_ref": "HIGH_END",
            "nome": "Profissional de Saúde (Médicos)",
            "dor": "Rotina exaustiva e necessidade de descanso absoluto.",
            "desejo": "Proximidade do HAOC/Santa Ignês e silêncio total."
        },
        "LOGISTICS_MANAGER": {
            "cluster_ref": "LOGISTICS",
            "nome": "Gestor de Logística/Empresário",
            "dor": "Custo logístico (Last Mile) e falta de área de manobra.",
            "desejo": "Galpão funcional, pé direito alto e acesso à SP-75."
        }
    }

    CONTENT_FORMATS = [
        "GUIA_DEFINITIVO", "LISTA_POLEMICA", "COMPARATIVO_TECNICO", 
        "CENARIO_ANALITICO", "CHECKLIST_TECNICO", "PREVISAO_MERCADO", 
        "ROTINA_SUGERIDA", "PERGUNTAS_RESPOSTAS", "INSIGHT_DE_CORRETOR", "DATA_DRIVEN"
    ]

    EMOTIONAL_TRIGGERS = [
        "MEDO_PERDA", "GANANCIA_LOGICA", "ALIVIO_IMEDIATO", 
        "STATUS_ORGULHO", "SEGURANCA_TOTAL"
    ]

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
# SCANNER DE BLOG
# =========================================================

class BlogScanner:
    def __init__(self, blog_url=GenesisConfig.BLOG_URL):
        self.feed_url = f"{blog_url}/feeds/posts/default?alt=json&max-results=9999"
        self.bairros_publicados = set()
        self.todos_titulos = [] 

    def mapear(self):
        self.bairros_publicados = set()
        self.todos_titulos = []
        # Nota: Prints aqui vão para o console do servidor, não para a UI do Streamlit
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            with urllib.request.urlopen(self.feed_url, context=ctx, timeout=20) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode())
                    if "feed" in data and "entry" in data["feed"]:
                        for entry in data["feed"]["entry"]:
                            titulo = entry["title"]["$t"]
                            self.bairros_publicados.add(slugify(titulo))
                            self.todos_titulos.append(titulo)
        except Exception as e:
            pass # Silencioso para não quebrar a UI

    def ja_publicado(self, nome_bairro: str) -> bool:
        slug = slugify(nome_bairro)
        for post in self.bairros_publicados:
            if slug in post: return True
        return False

    def get_ultimos_titulos(self, limite=10):
        return self.todos_titulos[:limite]

# =========================================================
# DATASET MESTRE
# =========================================================

class GenesisData:
    def __init__(self):
        self.bairros = self._bairros()
        self.topics = {
            "CUSTO_VIDA": "Matemática Financeira e Custo de Vida",
            "SEGURANCA": "Segurança Pública e Patrimonial",
            "EDUCACAO": "Escolas e Formação dos Filhos",
            "LOGISTICA": "Trânsito, Estradas e Viracopos",
            "LAZER": "Gastronomia, Parques e Clubes",
            "SAUDE": "Hospitais, Médicos e Bem-estar",
            "FUTURO": "Plano Diretor e Obras Futuras",
            "CLIMA": "Microclima e Áreas Verdes",
            "ARQUITETURA": "Estilo das Casas e Tendências",
            "HOME_OFFICE": "Conectividade e Espaço de Trabalho",
            "PETS": "Infraestrutura para Animais",
            "INVESTIMENTO": "Valorização e Aluguel",
            "COMMUTE": "Vida Híbrida (SP-Indaiatuba)",
            "CONDOMINIO": "Vida em Comunidade vs Privacidade",
            "LUXO": "Mercado de Alto Padrão"
        }
        
        self.ativos_por_cluster = {
            "HIGH_END": ["Casa em Condomínio de Luxo", "Sobrado Alto Padrão", "Mansão em Condomínio"],
            "FAMILY": ["Casa de Rua (Bairro Aberto)", "Casa em Condomínio Club", "Sobrado Residencial"],
            "URBAN": ["Apartamento Moderno", "Studio/Loft", "Cobertura Duplex"],
            "INVESTOR": ["Terreno em Condomínio", "Lote para Construção", "Imóvel para Reforma (Flip)"],
            "CORPORATE": ["Sala Comercial", "Laje Corporativa", "Prédio Monousuário"],
            "LOGISTICS": ["Galpão Logístico", "Terreno Industrial", "Condomínio Logístico"],
        }
        
        self.entidades_locais = {} 

    def _bairros(self):
        try:
            with open("bairros.json", "r", encoding="utf-8") as f:
                raw = json.load(f)
        except:
            return [
                {"nome": "Jardim Pau Preto", "zona": "Bairro Residencial Aberto"},
                {"nome": "Helvetia Park", "zona": "Condomínio Residencial Fechado"},
                {"nome": "Distrito Industrial", "zona": "Industrial"},
                {"nome": "Parque Ecológico", "zona": "Mista"}
            ]

        def _map_zona(zona_texto: str):
            z = zona_texto.lower()
            if "industrial" in z or "empresarial" in z: return "industrial"
            if "condomínio residencial fechado" in z: return "residencial_fechado"
            if "condomínio de chácaras" in z: return "chacaras_fechado"
            if "chácara" in z: return "chacaras_aberto"
            if "mista" in z: return "mista"
            if "bairro residencial aberto" in z or "parque" in z or "jardim" in z: return "residencial_aberto"
            return "indefinido"

        bairros_enriquecidos = []
        for b in raw:
            b2 = dict(b)
            b2["slug"] = slugify(b["nome"])
            b2["zona_normalizada"] = _map_zona(b.get("zona", ""))
            bairros_enriquecidos.append(b2)
        return bairros_enriquecidos

# =========================================================
# PLANO DIRETOR (LÓGICA)
# =========================================================

class PlanoDiretor:
    def refinar_ativo(self, cluster, bairro, ativos_base):
        zona = bairro.get("zona_normalizada", "indefinido")
        ativo_final = random.choice(ativos_base)
        obs = f"Compatível com {zona}"

        if zona == "residencial_aberto" and "Condomínio" in ativo_final:
            ativo_final = "Casa de Rua / Sobrado"
            obs = "Ajuste: Bairro aberto não tem condomínio."
        elif zona == "residencial_fechado" and "Rua" in ativo_final:
            ativo_final = "Casa em Condomínio Fechado"
            obs = "Ajuste: Condomínio exige casa interna."
        elif zona == "industrial" and cluster == "INVESTOR":
            ativo_final = "Terreno Industrial / Galpão"
            obs = "Ajuste: Investidor em zona industrial."
            
        return ativo_final, obs

# =========================================================
# GENESIS ENGINE V50.1 (CORE)
# =========================================================

class GenesisEngine:
    def __init__(self):
        self.config = GenesisConfig()
        self.data = GenesisData()
        self.plano = PlanoDiretor()
        self.scanner = BlogScanner()

    def run(self):
        self.scanner.mapear()
        historico_recente = self.scanner.get_ultimos_titulos(20)

        # 1. Definição da Persona
        persona_key = random.choice(list(self.config.PERSONAS.keys()))
        persona_data = self.config.PERSONAS[persona_key]
        cluster_ref = persona_data.get("cluster_ref", "FAMILY")
        
        # 2. Seleção de Bairro
        candidatos_validos = []
        for b in self.data.bairros:
            z = b.get("zona_normalizada")
            match = False
            if cluster_ref == "HIGH_END" and z in ["residencial_fechado", "chacaras_fechado"]: match = True
            elif cluster_ref == "FAMILY" and z in ["residencial_fechado", "residencial_aberto", "chacaras_fechado"]: match = True
            elif cluster_ref == "URBAN" and z in ["residencial_aberto", "mista"]: match = True
            elif cluster_ref == "INVESTOR" and z in ["industrial", "residencial_fechado", "mista", "residencial_aberto"]: match = True
            elif cluster_ref == "LOGISTICS" and z in ["industrial"]: match = True
            elif cluster_ref == "CORPORATE" and z in ["mista", "industrial", "residencial_aberto"]: match = True
            if match: candidatos_validos.append(b)

        modo = "CIDADE"
        bairro_selecionado = None
        obs_tecnica = "Foco Macro (Cidade)"
        ativo_final = random.choice(self.data.ativos_por_cluster.get(cluster_ref, ["Imóvel"]))

        if candidatos_validos and random.random() < 0.65:
            ineditos = [b for b in candidatos_validos if not self.scanner.ja_publicado(b["nome"])]
            if ineditos:
                bairro_selecionado = random.choice(ineditos)
                obs_tecnica = "Bairro Inédito Compatível"
            else:
                bairro_selecionado = random.choice(candidatos_validos)
                obs_tecnica = "Bairro Compatível (Já publicado)"
            modo = "BAIRRO"
            ativo_final, obs_ref = self.plano.refinar_ativo(cluster_ref, bairro_selecionado, self.data.ativos_por_cluster.get(cluster_ref, ["Imóvel"]))
            obs_tecnica += f" | {obs_ref}"

        topico_key, topico_nome = random.choice(list(self.data.topics.items()))
        formato = random.choice(self.config.CONTENT_FORMATS)
        gatilho = random.choice(self.config.EMOTIONAL_TRIGGERS)

        return {
            "modo": modo,
            "bairro": bairro_selecionado,
            "cluster_tecnico": cluster_ref,
            "ativo_definido": ativo_final,
            "topico": topico_nome,
            "persona": persona_data,
            "formato": formato,
            "gatilho": gatilho,
            "obs_tecnica": obs_tecnica,
            "historico_titulos": historico_recente
        }

# =========================================================
# PROMPT BUILDER V50.1 (FIXED)
# =========================================================

class PromptBuilder:
    
    def _format_date_blogger(self, iso_date_str):
        # FIX V50.1: Formatação blindada com ano obrigatório
        try:
            dt_part = iso_date_str.split("T")[0]
            dt = datetime.datetime.strptime(dt_part, "%Y-%m-%d")
            meses = {
                1: "jan.", 2: "fev.", 3: "mar.", 4: "abr.", 5: "mai.", 6: "jun.",
                7: "jul.", 8: "ago.", 9: "set.", 10: "out.", 11: "nov.", 12: "dez."
            }
            # FORÇA O ANO NO FINAL
            return f"{dt.day} de {meses[dt.month]} de {dt.year}"
        except Exception as e:
            # Em caso de erro extremo, retorna ISO mas tenta garantir ano atual pelo menos
            return iso_date_str

    def _generate_seo_tags(self, d):
        tags = ["Indaiatuba", "Imóveis Indaiatuba"]
        cluster_map = {
            "HIGH_END": ["Altíssimo Padrão", "Casas de Luxo", "Condomínios Fechados", "Mansões Indaiatuba"],
            "FAMILY": ["Qualidade de Vida", "Casas em Condomínio", "Morar com Família", "Segurança"],
            "URBAN": ["Apartamentos", "Centro de Indaiatuba", "Oportunidade", "Imóveis Urbanos"],
            "INVESTOR": ["Investimento Imobiliário", "Mercado Imobiliário", "Valorização", "Terrenos"],
            "LOGISTICS": ["Galpões Industriais", "Logística", "Área Industrial", "Aeroporto Viracopos"],
            "CORPORATE": ["Salas Comerciais", "Escritórios", "Imóveis Corporativos"]
        }
        tags.extend(cluster_map.get(d['cluster_tecnico'], []))

        if d['modo'] == "BAIRRO" and d['bairro']:
            tags.append(d['bairro']['nome'])
            tags.append(f"Morar no {d['bairro']['nome']}")
            tags.append(d['bairro']['zona'])

        ativo_clean = d['ativo_definido'].split("/")[0].strip()
        tags.append(ativo_clean)

        seen = set()
        final_tags = []
        for t in tags:
            if t not in seen:
                seen.add(t)
                final_tags.append(t)
        
        return ", ".join(final_tags[:8])

    def get_strict_table_rules(self):
        instrucao_pontos = "[PESQUISE E INSIRA 5 PONTOS DE REFERÊNCIA REAIS PRÓXIMOS AO LOCAL]"
        
        return f"""
### 3.3 Tabelas (Design System & CONTEÚDO DINÂMICO)
A IA deve gerar tabelas com uma única regra suprema: **LEITURA SEM HIFENIZAÇÃO**.
Siga estas regras de CSS Inline RIGOROSAMENTE:
1. **Estrutura de Rolagem (Wrapper):**
   Envolva TODA a tabela em: <div style="overflow-x: auto; width: 100%; margin-bottom: 20px;">
2. **Tag Table:**
   <table style="width: 100%; min-width: 600px; border-collapse: collapse; table-layout: auto;">
3. **Células (TH e TD) - A REGRA DE OURO:**
   Aplique o seguinte style em TODOS os `<th>` e `<td>`:
   * `style="padding: 12px; border: 1px solid #cccccc; word-break: keep-all; hyphens: none; -webkit-hyphens: none;"`
4. **Conteúdo (OBRIGATÓRIO PESQUISAR):**
   - Não use exemplos genéricos.
   - **PESQUISE** no Google Maps a distância real do bairro/local selecionado para: {instrucao_pontos}.
   - Inclua: Escolas, Supermercados, Acessos Viários ou Parques que realmente existam nas redondezas.
"""

    def get_format_instructions(self, formato):
        structures = {
            "GUIA_DEFINITIVO": "H2: Passos lógicos e técnicos. Evite narrativas pessoais.",
            "LISTA_POLEMICA": "H2 numerados. Desafie mitos de mercado (não crie mitos de pessoas).",
            "COMPARATIVO_TECNICO": "Tabela e análise de prós/contras técnicos.",
            "CENARIO_ANALITICO": "Use: 'Imagine um investidor que...', 'Considere o cenário...'. NUNCA use nomes reais.",
            "CHECKLIST_TECNICO": "Muitos Bullet Points. Foco em estrutura física e documental.",
            "PERGUNTAS_RESPOSTAS": "Formato FAQ Agressivo (Q&A).",
            "DATA_DRIVEN": "Foco em números, m², valorização e distâncias.",
            "INSIGHT_DE_CORRETOR": "Visão de bastidores do MERCADO (tendências), não de clientes específicos.",
            "ROTINA_SUGERIDA": "Rotina hipotética: 'Para quem acorda às 07:00 para ir a SP...'.",
            "PREVISAO_MERCADO": "Verbos no futuro. Análise baseada em infraestrutura e Plano Diretor."
        }
        return structures.get(formato, "Estrutura livre e técnica.")

    def build(self, d, data_pub, data_mod):
        data_fmt = self._format_date_blogger(data_pub)
        p = d['persona']
        ativo = d['ativo_definido']
        tags_otimizadas = self._generate_seo_tags(d)
        
        script_json_ld = """
{
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    "headline": "TITULO H1 DEFINIDO PELO GERADOR",
    "datePublished": "%s",
    "dateModified": "%s",
    "author": {"@type": "Organization", "name": "Imobiliária Saber"},
     "publisher": {"@type": "Organization", "name": "Imobiliária Saber", "logo": {"@type": "ImageObject", "url": "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEixiE1KghKkH0E-I53yyi5zoT7eRX0lxCGLpcWLGAmEE5st8OfHfuzbxfiygwCWRqAdSfpmjAhM8-SogHDU_1gXCX6IHrjW1BaUc87un1lF1o6y2Et7eV0m3gJgvfJs3HsAGyAcPYk8Tl_65rlQmgAp5orRZqtLDvixbCUwscTT8ZJO-7zckc36rNkWHz4/s1600/1000318124.png"}}
}
""" % (data_pub, data_mod)

        if d['modo'] == "BAIRRO":
            contexto_geo = f"Bairro Específico: **{d['bairro']['nome']}**"
            zoning_info = f"Zoneamento: {d['bairro']['zona']} ({d['obs_tecnica']})"
        else:
            contexto_geo = "Cidade: Indaiatuba (Panorama Geral)"
            zoning_info = "Macro-zoneamento urbano."

        anti_hallucination_txt = "\n".join([f"- {rule}" for rule in GenesisConfig.STRICT_GUIDELINES])

        # INSTRUÇÃO DE PESQUISA REFORÇADA
        ancora_instruction = """
        **ÂNCORAS LOCAIS (SEARCH MODE):** - A IA DEVE EXECUTAR UMA PESQUISA WEB (Search/Browse) para identificar o entorno do local: {loc}.
        - Identifique e cite nominalmente 3 a 5 estabelecimentos REAIS (Padarias, Escolas, Farmácias) que estão a menos de 10 minutos de distância.
        - PROIBIDO usar exemplos genéricos ou listas pré-prontas. Use dados do mapa.
        """.format(loc=contexto_geo)

        return f"""
## GENESIS MAGNETO V.50.1 — PURE SEARCH
**Objetivo:** Texto Inteligente, Limpo e com CONTEXTO LOCAL REAL (Pesquisado na hora).
**IMPORTANTE:** Você vai gerar o conteúdo final pronto para copiar e colar.

### 🛡️ PROTOCOLO DE VERACIDADE (ANTI-ALUCINAÇÃO)
A IA deve respeitar RIGOROSAMENTE estas regras:
{anti_hallucination_txt}

---

## 1. O CLIENTE ALVO (ARQUÉTIPO)
Você escreve para este PERFIL (Não transforme em um personagem com nome):
**PERFIL:** {p['nome']}
- **Dor Latente:** {p['dor']}
- **Desejo Secreto:** {p['desejo']}
- **Gatilho Emocional:** {d['gatilho']}

## 2. O PRODUTO E CONTEXTO
* **ATIVO:** {ativo}
* **LOCAL:** {contexto_geo}
* **TEMA:** {d['topico']}
* **FORMATO DE ESCRITA:** {self.get_format_instructions(d['formato'])}
* {ancora_instruction}

---

## 3. REGRAS TÉCNICAS E VISUAIS
Use `<style>.post-body h2 {{color: {GenesisConfig.COLOR_PRIMARY}; font-family: 'Segoe UI', sans-serif;}} p {{font-size: 19px; line-height: 1.6;}}</style>`.
{self.get_strict_table_rules()}

**CAPTURA DE LEADS (MANTENHA ESTE CÓDIGO NO FINAL DO HTML):**
`<div style="text-align:center; margin: 40px 0;"><script async data-uid="d188d73e78" src="https://sabernovidades.kit.com/d188d73e78/index.js"></script></div>`

---

## 5. CHECKLIST DE ENTREGA (ORDEM RÍGIDA)
Sua resposta deve seguir EXATAMENTE esta ordem.

1. LOG DE PESQUISA: (Liste quais locais reais você encontrou na pesquisa para usar no texto)

2. BLOCKCODE (HTML FRAGMENT + JSON-LD):
   - GERE APENAS O FRAGMENTO HTML (SEM <html>, <head>, <body>).
   - Inclua o JSON-LD dentro deste bloco usando `<script type="application/ld+json">...</script>`.
   - JSON-LD ID: {script_json_ld}
   - **NOTA:** Garanta que o texto não mencione "Ricardo", "Ana" ou empresas onde o cliente fictício trabalha.

3. TÍTULO: (Apenas O TÍTULO final escolhido, sem aspas)
4. MARCADORES: {tags_otimizadas}
5. DATA: {data_fmt} (Texto puro, exatamente como formatado)
6. LOCAL: Indaiatuba (sem ponto final)
7. DESCRIÇÃO: (Máximo 150 caracteres, focada na dor: {p['dor']})
8. IMAGEM: (Descrição técnica do ambiente, sem pessoas específicas)

""".strip()

# =========================================================
# INTERFACE STREAMLIT
# =========================================================

def main():
    st.set_page_config(page_title="Genesis V.50.1", page_icon="🚀", layout="wide")

    st.title(f"🚀 {GenesisConfig.VERSION}")
    st.markdown("---")

    # BARRA LATERAL (CONFIGURAÇÕES)
    with st.sidebar:
        st.header("Configurações")
        
        # Input de Data
        data_escolhida = st.date_input("Data de Publicação", datetime.date.today())
        
        # Botão de Ação
        btn_gerar = st.button("🎰 GERAR PROMPT", type="primary")

    # ÁREA PRINCIPAL
    if btn_gerar:
        with st.spinner("Escaneando blog e aplicando lógica híbrida..."):
            # Instancia as classes
            eng = GenesisEngine()
            bld = PromptBuilder()

            # Prepara as datas
            hoje_iso = datetime.datetime.now().strftime(f"%Y-%m-%dT%H:%M:%S{GenesisConfig.FUSO_PADRAO}")
            
            # Formata a data escolhida para o formato que sua classe espera
            d_pub = data_escolhida.strftime(f"%Y-%m-%dT00:00:00{GenesisConfig.FUSO_PADRAO}")

            # Executa a engine (seu código original)
            dados = eng.run()
            prompt_final = bld.build(dados, d_pub, hoje_iso)

            # Define nomes para arquivo
            p_name = slugify(dados['persona']['nome'])[:10]
            ativo_name = slugify(dados['ativo_definido'])[:10]
            nome_arquivo = f"{d_pub.split('T')[0]}_V50_1_{p_name}_{ativo_name}.txt"

        # EXIBIÇÃO DOS DADOS GERADOS (VISUAL BONITO)
        col1, col2 = st.columns(2)
        
        with col1:
            st.success("✅ Prompt Gerado com Sucesso!")
            st.info(f"**Persona:** {dados['persona']['nome']}")
            st.info(f"**Cluster:** {dados['cluster_tecnico']}")
            st.info(f"**Bairro:** {dados['bairro']['nome'] if dados['bairro'] else 'Cidade (Geral)'}")

        with col2:
            st.warning(f"**Ativo:** {dados['ativo_definido']}")
            st.warning(f"**Formato:** {dados['formato']}")
            st.warning(f"**Gatilho:** {dados['gatilho']}")

        st.markdown("### 📝 Prompt Final (Copie ou Baixe)")
        
        # Área de texto para copiar manualmente
        st.text_area("Conteúdo do Prompt", value=prompt_final, height=400)

        # Botão de Download
        st.download_button(
            label="💾 Baixar Arquivo .txt",
            data=prompt_final,
            file_name=nome_arquivo,
            mime="text/plain"
        )

if __name__ == "__main__":
    main()