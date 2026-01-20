import streamlit as st
import random
import datetime
import unicodedata
import json
import urllib.request
import ssl
import re
import os

from collections import defaultdict

# =========================================================
# LÓGICA ORIGINAL: GENESIS (PURE SEARCH MODE)
# =========================================================

class GenesisConfig:
    VERSION = "GERADOR V.51.0 (PURE SEARCH PREMIUM)"

    # Design System & URLs
    COLOR_PRIMARY = "#003366"   # Azul Saber
    BLOG_URL = "https://blog.saber.imb.br"
    FUSO_PADRAO = "-03:00"

    # REGRAS DE SEGURANÇA (ALTA NÍVEL)
    STRICT_GUIDELINES = [
        "NUNCA invente nomes de clientes (ex: Ricardo, Ana, João).",
        "NUNCA invente profissões específicas para o personagem.",
        "NUNCA crie depoimentos falsos.",
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

    # MATRIZ SEMÂNTICA (LSI KEYWORDS) – pode ser usada pela IA externa como repertório
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
# SCANNER DE BLOG (EVITA REPETIÇÕES DE BAIRROS/TEMAS)
# =========================================================

class BlogScanner:
    def __init__(self, blog_url=GenesisConfig.BLOG_URL):
        self.feed_url = f"{blog_url}/feeds/posts/default?alt=json&max-results=9999"
        self.bairros_publicados = set()
        self.todos_titulos = []

    def mapear(self):
        self.bairros_publicados = set()
        self.todos_titulos = []
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
        except Exception:
            # Em caso de falha de rede, seguir sem histórico (modo resiliente)
            pass

    def ja_publicado(self, nome_bairro: str) -> bool:
        slug = slugify(nome_bairro)
        for post in self.bairros_publicados:
            if slug in post:
                return True
        return False

    def get_ultimos_titulos(self, limite=10):
        return self.todos_titulos[:limite]


# =========================================================
# CARREGAMENTO DE REGRAS (REGRAS.txt)
# =========================================================

class GenesisRules:
    """
    Carrega o arquivo REGRAS.txt como "constituição" do gerador.
    NÃO resume, NÃO altera. Apenas injeta no prompt.
    Se quiser mudar as leis, altere o arquivo REGRAS.txt, não o código.
    """
    def __init__(self, path: str = "REGRAS.txt"):
        if not os.path.exists(path):
            raise RuntimeError(
                "Arquivo REGRAS.txt não encontrado na pasta raiz. "
                "Coloque o arquivo REGRAS.txt ao lado deste aplicativo e tente novamente."
            )
        try:
            with open(path, "r", encoding="utf-8") as f:
                self.raw_text = f.read()
        except Exception as e:
            raise RuntimeError(f"Erro ao ler REGRAS.txt: {e}")

    def get_for_prompt(self, contexto_local: str) -> str:
        """
        Retorna o texto de regras ajustando apenas o placeholder {b['nome']}
        para o contexto correto (bairro ou cidade).
        O texto original é mantido intacto em self.raw_text.
        """
        txt = self.raw_text
        # Substitui placeholder de bairro por um contexto legível
        txt = txt.replace("{b['nome']}", contexto_local)
        return txt


# =========================================================
# DATASET MESTRE (BAIRROS, TÓPICOS, ATIVOS)
# =========================================================

class GenesisData:
    def __init__(self, bairros_path: str = "bairros.json"):
        self.bairros = self._carregar_bairros(bairros_path)
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

    def _carregar_bairros(self, path: str):
        if not os.path.exists(path):
            raise RuntimeError(
                f"Arquivo '{path}' não encontrado. "
                f"Coloque o arquivo bairros.json na mesma pasta do aplicativo."
            )
        try:
            with open(path, "r", encoding="utf-8") as f:
                raw = json.load(f)
        except Exception as e:
            raise RuntimeError(f"Erro ao carregar '{path}': {e}")

        def _map_zona(zona_texto: str):
            z = zona_texto.lower()
            if "industrial" in z or "empresarial" in z:
                return "industrial"
            if "condomínio residencial fechado" in z or "condominio residencial fechado" in z:
                return "residencial_fechado"
            if "condomínio de chácaras" in z or "condominio de chacaras" in z:
                return "chacaras_fechado"
            if "chácara" in z or "chacara" in z:
                return "chacaras_aberto"
            if "mista" in z:
                return "mista"
            if "bairro residencial aberto" in z or "parque" in z or "jardim" in z:
                return "residencial_aberto"
            return "indefinido"

        bairros_enriquecidos = []
        for b in raw:
            b2 = dict(b)
            b2["slug"] = slugify(b["nome"])
            b2["zona_normalizada"] = _map_zona(b.get("zona", ""))
            bairros_enriquecidos.append(b2)

        if not bairros_enriquecidos:
            raise RuntimeError("Lista de bairros está vazia em bairros.json.")
        return bairros_enriquecidos


# =========================================================
# PLANO DIRETOR (LÓGICA DE COMPATIBILIDADE ATIVO x ZONA)
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
# GENESIS ENGINE V51.0 (CORE)
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

        # 2. Seleção de Bairro com base em zona e cluster
        candidatos_validos = []
        for b in self.data.bairros:
            z = b.get("zona_normalizada")
            match = False
            if cluster_ref == "HIGH_END" and z in ["residencial_fechado", "chacaras_fechado"]:
                match = True
            elif cluster_ref == "FAMILY" and z in ["residencial_fechado", "residencial_aberto", "chacaras_fechado"]:
                match = True
            elif cluster_ref == "URBAN" and z in ["residencial_aberto", "mista"]:
                match = True
            elif cluster_ref == "INVESTOR" and z in ["industrial", "residencial_fechado", "mista", "residencial_aberto"]:
                match = True
            elif cluster_ref == "LOGISTICS" and z in ["industrial"]:
                match = True
            elif cluster_ref == "CORPORATE" and z in ["mista", "industrial", "residencial_aberto"]:
                match = True
            if match:
                candidatos_validos.append(b)

        modo = "CIDADE"
        bairro_selecionado = None
        obs_tecnica = "Foco Macro (Cidade)"
        ativo_final = random.choice(self.data.ativos_por_cluster.get(cluster_ref, ["Imóvel"]))

        # 65% de chance de modo bairro, respeitando inéditos quando possível
        if candidatos_validos and random.random() < 0.65:
            ineditos = [b for b in candidatos_validos if not self.scanner.ja_publicado(b["nome"])]
            if ineditos:
                bairro_selecionado = random.choice(ineditos)
                obs_tecnica = "Bairro Inédito Compatível"
            else:
                bairro_selecionado = random.choice(candidatos_validos)
                obs_tecnica = "Bairro Compatível (Já publicado)"
            modo = "BAIRRO"
            ativo_final, obs_ref = self.plano.refinar_ativo(
                cluster_ref,
                bairro_selecionado,
                self.data.ativos_por_cluster.get(cluster_ref, ["Imóvel"])
            )
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
# PROMPT BUILDER V51.0 (QUALIDADE DO TEXTO FINAL)
# =========================================================

class PromptBuilder:

    def __init__(self, regras_texto: str = ""):
        self.regras_texto = regras_texto

    def _format_date_blogger(self, iso_date_str):
        try:
            dt_part = iso_date_str.split("T")[0]
            dt = datetime.datetime.strptime(dt_part, "%Y-%m-%d")
            meses = {
                1: "jan.", 2: "fev.", 3: "mar.", 4: "abr.", 5: "mai.", 6: "jun.",
                7: "jul.", 8: "ago.", 9: "set.", 10: "out.", 11: "nov.", 12: "dez."
            }
            return f"{dt.day} de {meses[dt.month]} de {dt.year}"
        except Exception:
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

    def get_format_instructions(self, formato):
        structures = {
            "GUIA_DEFINITIVO": "Guia organizado em seções técnicas, com passos lógicos. Evite narrativa 'história de personagem'.",
            "LISTA_POLEMICA": "Lista numerada que confronte mitos comuns do mercado, sempre com dados e contexto local.",
            "COMPARATIVO_TECNICO": "Comparação objetiva (pode usar tabela) com prós e contras, sem adjetivos vazios.",
            "CENARIO_ANALITICO": "Construção de cenários: 'Se o investidor fizer X...', 'No cenário Y...'. Foco em análise, não em storytelling.",
            "CHECKLIST_TECNICO": "Checklists de verificação (documentos, itens físicos, entorno). Foco em uso prático.",
            "PERGUNTAS_RESPOSTAS": "Formato FAQ direto, com perguntas de quem está decidindo se compra ou não.",
            "DATA_DRIVEN": "Texto orientado a dados (m², distâncias, tempos de deslocamento, histórico de obras).",
            "INSIGHT_DE_CORRETOR": "Bastidores do mercado, visão de corretor experiente, nunca envolvendo clientes com nome.",
            "ROTINA_SUGERIDA": "Descreva rotinas típicas (sem nomes), ligando horário, deslocamento e uso de serviços.",
            "PREVISAO_MERCADO": "Análise de futuro com base em infraestrutura, obras planejadas e comportamento do mercado."
        }
        return structures.get(formato, "Estrutura livre, técnica, focada em decisão do leitor.")

    def build(self, d, data_pub, data_mod, regras_texto_ajustada: str):
        data_fmt = self._format_date_blogger(data_pub)
        p = d['persona']
        ativo = d['ativo_definido']
        tags_otimizadas = self._generate_seo_tags(d)

        # JSON-LD base para orientar a IA (deve ser inserido no <script type="application/ld+json">)
        script_json_ld = """
{
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    "headline": "TITULO H1 DEFINIDO PELO GERADOR",
    "datePublished": "%s",
    "dateModified": "%s",
    "author": {
        "@type": "Organization",
        "name": "Imobiliária Saber"
    },
    "publisher": {
        "@type": "Organization",
        "name": "Imobiliária Saber",
        "logo": {
            "@type": "ImageObject",
            "url": "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhtRYbYvSxR-IRaFMCb95rCMmr1pKSkJKSVGD2SfW1h7e7M-NbCly3qk9xKK5lYpfOPYfq-xkzJ51p14cGftPHLF7MrbM0Szz62qQ-Ff5H79-dMiUcNzhrEL7LXKf089Ka2yzGaIX-UJBgTtdalNaWYPS0JSSfIMYNIE4yxhisKcU8j-gtOqXq6lSmgiSA/s600/1000324271.png"
        }
    }
}
""" % (data_pub, data_mod)

        if d['modo'] == "BAIRRO" and d['bairro']:
            contexto_geo = f"Bairro Específico: {d['bairro']['nome']}"
            zoning_info = f"Zoneamento oficial: {d['bairro']['zona']} ({d['obs_tecnica']})"
            contexto_local_curto = d['bairro']['nome']
        else:
            contexto_geo = "Cidade: Indaiatuba (Panorama Geral, sem bairro específico)"
            zoning_info = "Macro-zoneamento urbano (foco na cidade como um todo)."
            contexto_local_curto = "Indaiatuba"

        anti_hallucination_txt = "\n".join([f"- {rule}" for rule in GenesisConfig.STRICT_GUIDELINES])

        # Instrução específica de pesquisa local (Google Maps mental)
        ancora_instruction = f"""
**ÂNCORAS LOCAIS (MODO SEARCH):**
- EXECUTE busca mental como se estivesse usando Google Maps para o contexto: {contexto_geo}.
- Identifique de 3 a 5 estabelecimentos REAIS (escolas, mercados, serviços de saúde, parques, vias principais).
- Use tempos de deslocamento REALISTAS (ex.: 5 a 12 minutos de carro).
- PROIBIDO usar nomes genéricos como "Padaria do Bairro" ou "Supermercado Local". Sempre use nomes reais.
"""

        # Regras completas vindas do REGRAS.txt (Zona de Segurança Máxima)
        bloco_regras = f"""
# ==========================================
# 🔐 ZONA DE SEGURANÇA MÁXIMA (REGRAS.txt)
# (NÃO RESUMA, NÃO IGNORE, NÃO ALTERE)
# ==========================================
{regras_texto_ajustada}
"""

        # Diretrizes de qualidade de TEXTO FINAL
        bloco_qualidade = f"""
## 4. ESTILO DO TEXTO (QUALIDADE & LEITURA MOBILE)

Você está escrevendo para humanos, em especial leitura em celular. Siga estas regras:

1. **Parágrafos Curto-Moderados**
   - Cada parágrafo deve ter no máximo 3 frases longas OU 5 frases curtas.
   - Evite blocos de texto muito densos.

2. **Frases Objetivas**
   - Prefira frases com até ~22 palavras.
   - Corte adjetivos vazios (ex.: "maravilhoso", "lindo", "oportunidade única") – eles são proibidos pelo protocolo.

3. **Escaneabilidade Visual**
   - Use subtítulos (H2/H3) que respondam perguntas do leitor, por exemplo:
     - "Como é a rotina de quem mora aqui?"
     - "O que muda no seu tempo de deslocamento?"
   - Use listas com bullet points para:
     - prós e contras
     - checklists
     - comparações

4. **Tom e Linguagem**
   - Tom profissional, mas acessível (não acadêmico).
   - Evite jargão técnico sem explicação.
   - Nunca use nomes de pessoas (Ricardo, Ana, João) ou empresas onde o cliente fictício trabalha.

5. **Conclusão de Valor (Obrigatória)**
   - Feche o texto com 1 ou 2 parágrafos de síntese que respondam:
     - "O que esse conteúdo ajuda o leitor a decidir?"
     - "Para o perfil {p['nome']}, qual é a principal mensagem prática?"

## 5. ESTRUTURA MÍNIMA DO TEXTO (SEÇÕES SUGERIDAS)

Use esta sequência como base, adaptando ao formato {d['formato']}:

1. **Introdução enxuta (máx. 2 parágrafos)**
   - Apresente o tema ({d['topico']}) e para quem ele é relevante ({p['nome']}).
   - Diga em 1 frase o que o leitor vai entender ao final.

2. **Diagnóstico da Situação**
   - Mostre o problema, dor ou dúvida central do perfil:
     - Dor principal: {p['dor']}
     - Desejo central: {p['desejo']}
   - Conecte isso com o ativo ({ativo}) e o contexto ({contexto_geo}).

3. **Corpo Técnico (2 a 4 blocos)**
   - Estruture em seções com subtítulos claros:
     - uma seção sobre rotina ou uso do lugar
     - uma seção sobre dados (distâncias, tempo, infraestrutura)
     - uma seção sobre riscos x benefícios (quando fizer sentido)
   - Sempre ligando de volta ao impacto real na vida de quem lê.

4. **Conclusão Estratégica**
   - Resuma os 2 ou 3 pontos-chave que o leitor precisa guardar.
   - Escreva explicitamente:
     - "[Para o perfil {p['nome']}], isso significa que..."
   - NÃO faça convite comercial direto (sem 'venha conferir', 'agende uma visita' etc.).
"""

        # Instruções para TABELAS (mantidas via REGRAS.txt, mas reforçadas)
        # + Estilo de texto em HTML
        estilo_html = f"""<style>
.post-body h2 {{
    color: {GenesisConfig.COLOR_PRIMARY};
    font-family: 'Segoe UI', Arial, sans-serif;
}}
.post-body h3 {{
    color: {GenesisConfig.COLOR_PRIMARY};
    font-family: 'Segoe UI', Arial, sans-serif;
}}
.post-body p {{
    font-size: 19px;
    line-height: 1.6;
}}
</style>"""

        return f"""
## GENESIS MAGNETO V.51.0 — PURE SEARCH (QUALITY MODE)
**Objetivo:** Gerar um texto final pronto para publicar no Blogger, com:
- contexto local real (pesquisado),
- leitura fluida em mobile,
- estrutura lógica clara,
- conclusão útil para o leitor.

### 🛡️ PROTOCOLO DE VERACIDADE (ANTI-ALUCINAÇÃO)
A IA deve respeitar RIGOROSAMENTE estas regras:
{anti_hallucination_txt}

---

## 1. O CLIENTE ALVO (ARQUÉTIPO)
Você escreve para este PERFIL (não transforme em personagem com nome):

**PERFIL:** {p['nome']}
- **Dor Latente:** {p['dor']}
- **Desejo Secreto:** {p['desejo']}
- **Gatilho Emocional Principal:** {d['gatilho']}

## 2. O PRODUTO E CONTEXTO
- **ATIVO EM FOCO:** {ativo}
- **LOCAL / RECORTE:** {contexto_geo}
- **ZONEAMENTO / CONTEXTO URBANO:** {zoning_info}
- **TEMA PRINCIPAL:** {d['topico']}
- **FORMATO DE ESCRITA (macroestrutura):** {self.get_format_instructions(d['formato'])}
{ancora_instruction}

---

## 3. REGRAS TÉCNICAS, VISUAIS E DE JSON-LD

Você está escrevendo um **FRAGMENTO DE HTML** para um post no Blogger, que DEVE conter também o JSON-LD de artigo.

Use este estilo mínimo de HTML:

{estilo_html}

EM SEGUIDA, aplique TODAS as regras abaixo, copiadas da constituição (REGRAS.txt). NÃO RESUMA, NÃO IGNORE NENHUMA:

{bloco_regras}

{bloco_qualidade}

---

## 6. CHECKLIST FINAL DE ENTREGA (ORDEM IMUTÁVEL)

Sua resposta final para o usuário DEVE seguir EXATAMENTE esta ordem numérica:

1. LOG DE BASTIDORES:
   - Explique em texto corrido como você pensou o conteúdo.
   - Liste quais locais reais pesquisou mentalmente (Google Maps) e por que escolheu cada um.
   - Mostre, em poucas linhas, qual é o fio condutor do texto.

2. BLOCKCODE (HTML PURO + JSON-LD EMBUTIDO):
   - Gere apenas o fragmento HTML (SEM <!DOCTYPE>, <html>, <head>, <body>, <meta>, <title>).
   - Comece direto com <style> (se usar) ou com o primeiro <h2>.
   - Dentro deste bloco HTML, inclua **um único** `<script type="application/ld+json">` com um JSON baseado neste modelo:
     {script_json_ld}
   - Respeite as datas fornecidas:
     - **datePublished:** {data_pub}
     - **dateModified:** {data_mod}
   - No final do HTML, inclua OBRIGATORIAMENTE o CTA de captura de e-mail (exatamente assim):
     `<div style="text-align:center; margin: 40px 0;"><script async data-uid="d188d73e78" src="https://sabernovidades.kit.com/d188d73e78/index.js"></script></div>`

3. TÍTULO:
   - Apenas o título final escolhido (H1), sem aspas.
   - Deve ser objetivo, técnico e descrever claramente o recorte do texto.

4. MARCADORES:
   - Lista de tags SEO separadas por vírgula.
   - Use exatamente esta lista base já otimizada:
     {tags_otimizadas}

5. DATA:
   - Data em TEXTO PURO, no formato: {data_fmt}

6. LOCAL:
   - Sempre: Indaiatuba

7. DESCRIÇÃO:
   - Meta description com no máximo 150 caracteres.
   - Foque na dor principal do perfil: {p['dor']}
   - Não use chamadas de venda explícitas.

8. IMAGEM:
   - Forneça um prompt técnico para IA generativa criar uma imagem:
     - enquadramento,
     - horário do dia,
     - tipo de via / imóveis,
     - clima geral da cena.
   - NÃO inclua pessoas identificáveis, placas de rua legíveis ou marcas.

""".strip()


# =========================================================
# UI STREAMLIT (VISUAL, LÓGICA V51.0)
# =========================================================

def main():
    THEME = {
        "primary": "#003366",  # Azul Saber
        "accent": "#D4AF37",   # Ouro (Premium)
        "bg": "#f4f6f9"
    }

    st.set_page_config(page_title="Genesis Agency v11 (Quality Mode)", page_icon="💎", layout="wide")

    st.markdown(f"""
    <style>
        .stApp {{ background-color: {THEME['bg']}; }}
        .big-card {{
            background: white; padding: 20px; border-radius: 10px;
            border-left: 6px solid {THEME['primary']};
            box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px;
        }}
        .stat-value {{ font-size: 24px; font-weight: bold; color: {THEME['primary']}; }}
        .stat-label {{ font-size: 14px; color: #666; text-transform: uppercase; letter-spacing: 1px; }}
        .highlight {{ color: {THEME['accent']}; font-weight: bold; }}
        div.stButton > button {{
            background: linear-gradient(45deg, {THEME['primary']}, #004080);
            color: white; border: none; height: 60px; font-size: 18px; font-weight: bold;
            width: 100%; border-radius: 8px; text-transform: uppercase;
        }}
        div.stButton > button:hover {{ opacity: 0.9; }}
    </style>
    """, unsafe_allow_html=True)

    # Header
    c1, c2 = st.columns([3, 1])
    with c1:
        st.title("💎 GENESIS AGENCY V11.0 — QUALITY MODE")
        st.markdown(f"**AI Content Director para Imobiliária Saber (Engine: {GenesisConfig.VERSION})**")
    with c2:
        st.image(
            "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhtRYbYvSxR-IRaFMCb95rCMmr1pKSkJKSVGD2SfW1h7e7M-NbCly3qk9xKK5lYpfOPYfq-xkzJ51p14cGftPHLF7MrbM0Szz62qQ-Ff5H79-dMiUcNzhrEL7LXKf089Ka2yzGaIX-UJBgTtdalNaWYPS0JSSfIMYNIE4yxhisKcU8j-gtOqXq6lSmgiSA/s600/1000324271.png",
            width=100
        )

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuração da Pauta")
        data_escolhida = st.date_input("Data de Publicação", datetime.date.today())
        st.markdown("---")
        st.markdown("### 🛡️ Protocolos Ativos")
        st.caption(f"✅ Logic Engine: {GenesisConfig.VERSION}")
        st.caption("✅ Anti-Alucinação (Google Maps Search Mode)")
        st.caption("✅ Lead Capture Injection (Kit.com)")
        st.caption("✅ Qualidade de Texto (Leitura Mobile + Conclusão Estratégica)")
        st.markdown("---")
        if st.button("🔄 Resetar Sistema"):
            st.rerun()

    col_main, col_view = st.columns([1, 2])

    with col_main:
        st.markdown("### Gerar Briefing Premium")
        st.write(
            "O sistema irá selecionar automaticamente a melhor oportunidade com base em personas, "
            "bairros e lógica V51.0, gerando um prompt pensado para TEXTO FINAL de alta qualidade."
        )
        generate_btn = st.button("CRIAR PAUTA ESTRATÉGICA ✨")

    if generate_btn:
        try:
            with st.spinner("Carregando bairros, regras e aplicando lógica V51.0 (Quality Mode)..."):
                # Carrega engine (usa bairros.json obrigatoriamente)
                eng = GenesisEngine()

                # Carrega regras (REGRAS.txt obrigatório)
                regras = GenesisRules()

                # Prepara datas com fuso -03:00
                hoje_iso = datetime.datetime.now().strftime(f"%Y-%m-%dT%H:%M:%S{GenesisConfig.FUSO_PADRAO}")
                d_pub = data_escolhida.strftime(f"%Y-%m-%dT00:00:00{GenesisConfig.FUSO_PADRAO}")

                # Executa engine
                dados = eng.run()

                # Ajusta texto de regras com contexto local
                if dados["modo"] == "BAIRRO" and dados["bairro"]:
                    contexto_local_curto = dados["bairro"]["nome"]
                else:
                    contexto_local_curto = "Indaiatuba"
                regras_ajustadas = regras.get_for_prompt(contexto_local_curto)

                # Constrói prompt final
                bld = PromptBuilder()
                prompt_final = bld.build(dados, d_pub, hoje_iso, regras_ajustadas)

                # Nome de arquivo
                p_name = slugify(dados['persona']['nome'])[:10]
                ativo_name = slugify(dados['ativo_definido'])[:10]
                nome_arquivo = f"{d_pub.split('T')[0]}_V51_quality_{p_name}_{ativo_name}.txt"

        except RuntimeError as e:
            # Erros críticos de arquivo (bairros.json ou REGRAS.txt)
            with col_view:
                st.error(f"⚠️ Erro crítico na configuração: {e}")
                st.info("Corrija o problema e recarregue a aplicação.")
            return

        # Exibição visual do raciocínio da agência
        bairro_display = (
            dados['bairro']['nome'] if dados['bairro'] else "Indaiatuba (Panorama Geral)"
        )
        zona_display = (
            dados['bairro']['zona'] if dados['bairro'] else "Macro-zoneamento"
        )

        with col_view:
            st.markdown(f"""
            <div class="big-card">
                <div style="display:grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                    <div>
                        <div class="stat-label">Persona Alvo</div>
                        <div class="stat-value">{dados['persona']['nome']}</div>
                        <small>{dados['persona']['dor']}</small>
                    </div>
                    <div>
                        <div class="stat-label">Localização</div>
                        <div class="stat-value">{bairro_display}</div>
                        <small>{zona_display}</small>
                    </div>
                </div>
                <hr style="opacity: 0.2">
                <div style="display:grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                    <div>
                        <div class="stat-label">Ativo Foco</div>
                        <div class="stat-value">{dados['ativo_definido']}</div>
                    </div>
                    <div>
                        <div class="stat-label">Gatilho & Formato</div>
                        <div class="stat-value highlight">{dados['gatilho']}</div>
                        <small>{dados['formato']}</small>
                    </div>
                </div>
                <hr style="opacity: 0.2">
                <div>
                    <div class="stat-label">Modo de Conteúdo</div>
                    <div class="stat-value">{dados['modo']}</div>
                    <small>{dados['obs_tecnica']}</small>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("### 📋 Prompt de Engenharia Reversa (V51.0 — Quality Mode)")
        st.text_area("Prompt Otimizado:", value=prompt_final, height=450)

        st.download_button(
            label="💾 BAIXAR ARQUIVO DE PAUTA (.txt)",
            data=prompt_final,
            file_name=nome_arquivo,
            mime="text/plain"
        )

        st.success("✅ Estratégia gerada com sucesso! Copie o texto acima e cole na sua IA de preferência para gerar o TEXTO FINAL.")
    else:
        with col_view:
            st.info("👈 Clique em **CRIAR PAUTA ESTRATÉGICA ✨** para gerar um briefing já otimizado para qualidade de texto final.")


if __name__ == "__main__":
    main()
