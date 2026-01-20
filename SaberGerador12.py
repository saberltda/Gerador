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
# LÓGICA ORIGINAL: GENESIS (GOD MODE ENABLED)
# =========================================================

class GenesisConfig:
    VERSION = "GERADOR V.52.0 (GOD MODE)"

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
        txt = self.raw_text
        txt = txt.replace("{b['nome']}", contexto_local)
        return txt


# =========================================================
# DATASET MESTRE
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
        
        # Flatten para lista de todos os ativos possíveis para seleção manual
        self.todos_ativos = []
        for lista in self.ativos_por_cluster.values():
            self.todos_ativos.extend(lista)
        self.todos_ativos = list(set(self.todos_ativos)) # Remove duplicatas
        self.todos_ativos.sort()

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
# PLANO DIRETOR (LÓGICA DE COMPATIBILIDADE)
# =========================================================

class PlanoDiretor:
    def refinar_ativo(self, cluster, bairro, ativos_base):
        zona = bairro.get("zona_normalizada", "indefinido")
        
        # Se ativos_base for string (seleção manual), transforme em lista
        if isinstance(ativos_base, str):
            ativos_base = [ativos_base]
            
        ativo_final = random.choice(ativos_base)
        obs = f"Compatível com {zona}"

        # Lógica de correção de coerência física
        if zona == "residencial_aberto" and "Condomínio" in ativo_final and "Fechado" in ativo_final:
            ativo_final = "Casa de Rua / Sobrado"
            obs = "Ajuste Automático: Bairro aberto não tem condomínio."
        elif zona == "residencial_fechado" and "Rua" in ativo_final:
            ativo_final = "Casa em Condomínio Fechado"
            obs = "Ajuste Automático: Condomínio exige casa interna."
        elif zona == "industrial" and cluster == "INVESTOR":
            ativo_final = "Terreno Industrial / Galpão"
            obs = "Ajuste Automático: Investidor em zona industrial."

        return ativo_final, obs


# =========================================================
# GENESIS ENGINE V52.0 (CORE & GOD MODE)
# =========================================================

class GenesisEngine:
    def __init__(self, data_instance):
        self.config = GenesisConfig()
        self.data = data_instance
        self.plano = PlanoDiretor()
        self.scanner = BlogScanner()

    def run(self, user_selection: dict):
        """
        user_selection espera:
        {
            "persona_key": "ALEATÓRIO" ou chave str,
            "bairro_nome": "ALEATÓRIO" ou nome str,
            "topico": "ALEATÓRIO" ou nome str,
            "ativo": "ALEATÓRIO" ou nome str,
            "formato": "ALEATÓRIO" ou nome str,
            "gatilho": "ALEATÓRIO" ou nome str
        }
        """
        self.scanner.mapear()
        historico_recente = self.scanner.get_ultimos_titulos(20)

        # 1. Definição da Persona
        if user_selection['persona_key'] != "ALEATÓRIO":
            persona_key = user_selection['persona_key']
            obs_persona = "Seleção Manual"
        else:
            persona_key = random.choice(list(self.config.PERSONAS.keys()))
            obs_persona = "Seleção IA"
            
        persona_data = self.config.PERSONAS[persona_key]
        cluster_ref = persona_data.get("cluster_ref", "FAMILY")

        # 2. Definição do Bairro
        bairro_selecionado = None
        modo = "CIDADE"
        obs_tecnica = "Foco Macro (Cidade)"

        # Se o usuário escolheu um bairro específico
        if user_selection['bairro_nome'] != "ALEATÓRIO":
            # Encontrar objeto bairro
            for b in self.data.bairros:
                if b['nome'] == user_selection['bairro_nome']:
                    bairro_selecionado = b
                    break
            if bairro_selecionado:
                modo = "BAIRRO"
                obs_tecnica = "Bairro Definido pelo Usuário"
        
        # Se for ALEATÓRIO, usar lógica inteligente da V11
        else:
            # Filtrar candidatos válidos para o Cluster da Persona
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

            # Sorteio inteligente (65% chance de ser Bairro Específico)
            if candidates_validos := candidatos_validos:
                if random.random() < 0.65:
                    ineditos = [b for b in candidatos_validos if not self.scanner.ja_publicado(b["nome"])]
                    if ineditos:
                        bairro_selecionado = random.choice(ineditos)
                        obs_tecnica = "Bairro Inédito Compatível (IA)"
                    else:
                        bairro_selecionado = random.choice(candidatos_validos)
                        obs_tecnica = "Bairro Compatível (IA - Já publicado)"
                    modo = "BAIRRO"

        # 3. Definição de Ativo
        if user_selection['ativo'] != "ALEATÓRIO":
            ativo_final = user_selection['ativo']
            obs_ref = "Ativo Definido pelo Usuário"
            # Mesmo manual, passamos pelo refinador se houver bairro para checar lógica física
            if bairro_selecionado:
                 ativo_final, obs_ajuste = self.plano.refinar_ativo(cluster_ref, bairro_selecionado, [ativo_final])
                 obs_ref += f" | {obs_ajuste}"
        else:
            ativo_base_list = self.data.ativos_por_cluster.get(cluster_ref, ["Imóvel Padrão"])
            ativo_final = random.choice(ativo_base_list)
            obs_ref = "Ativo Aleatório"
            if modo == "BAIRRO" and bairro_selecionado:
                ativo_final, obs_ajuste = self.plano.refinar_ativo(
                    cluster_ref,
                    bairro_selecionado,
                    ativo_base_list
                )
                obs_ref = obs_ajuste

        obs_tecnica += f" | {obs_ref}"

        # 4. Tópico, Formato e Gatilho
        if user_selection['topico'] != "ALEATÓRIO":
            topico_nome = user_selection['topico']
        else:
            _, topico_nome = random.choice(list(self.data.topics.items()))

        if user_selection['formato'] != "ALEATÓRIO":
            formato = user_selection['formato']
        else:
            formato = random.choice(self.config.CONTENT_FORMATS)

        if user_selection['gatilho'] != "ALEATÓRIO":
            gatilho = user_selection['gatilho']
        else:
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
# PROMPT BUILDER
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
            "GUIA_DEFINITIVO": "Guia organizado em seções técnicas, com passos lógicos.",
            "LISTA_POLEMICA": "Lista numerada que confronte mitos comuns do mercado.",
            "COMPARATIVO_TECNICO": "Comparação objetiva (pode usar tabela) com prós e contras.",
            "CENARIO_ANALITICO": "Construção de cenários: 'Se o investidor fizer X...', 'No cenário Y...'.",
            "CHECKLIST_TECNICO": "Checklists de verificação (documentos, itens físicos, entorno).",
            "PERGUNTAS_RESPOSTAS": "Formato FAQ direto, com perguntas de quem está decidindo.",
            "DATA_DRIVEN": "Texto orientado a dados (m², distâncias, tempos de deslocamento).",
            "INSIGHT_DE_CORRETOR": "Bastidores do mercado, visão de corretor experiente.",
            "ROTINA_SUGERIDA": "Descreva rotinas típicas ligando horário, deslocamento e uso de serviços.",
            "PREVISAO_MERCADO": "Análise de futuro com base em infraestrutura e obras planejadas."
        }
        return structures.get(formato, "Estrutura livre, técnica, focada em decisão do leitor.")

    def build(self, d, data_pub, data_mod, regras_texto_ajustada: str):
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
        else:
            contexto_geo = "Cidade: Indaiatuba (Panorama Geral, sem bairro específico)"
            zoning_info = "Macro-zoneamento urbano (foco na cidade como um todo)."

        anti_hallucination_txt = "\n".join([f"- {rule}" for rule in GenesisConfig.STRICT_GUIDELINES])

        ancora_instruction = f"""
**ÂNCORAS LOCAIS (MODO SEARCH):**
- EXECUTE busca mental como se estivesse usando Google Maps para o contexto: {contexto_geo}.
- Identifique de 3 a 5 estabelecimentos REAIS (escolas, mercados, serviços de saúde).
- Use tempos de deslocamento REALISTAS.
- PROIBIDO usar nomes genéricos.
"""

        bloco_regras = f"""
# ==========================================
# 🔐 ZONA DE SEGURANÇA MÁXIMA (REGRAS.txt)
# ==========================================
{regras_texto_ajustada}
"""

        bloco_qualidade = f"""
## 4. ESTILO DO TEXTO (QUALIDADE & LEITURA MOBILE)
1. **Parágrafos Curto-Moderados** (máx 5 linhas).
2. **Frases Objetivas**.
3. **Escaneabilidade Visual** (Use H2/H3 e Bullet Points).
4. **Tom e Linguagem** Profissional mas acessível. Sem jargão solto.
5. **Conclusão de Valor (Obrigatória)**: Responda "O que esse conteúdo ajuda o leitor a decidir?".

## 5. ESTRUTURA MÍNIMA DO TEXTO
1. **Introdução enxuta**
2. **Diagnóstico da Situação** (Dor: {p['dor']} -> Desejo: {p['desejo']})
3. **Corpo Técnico** (Rotina, Dados, Riscos x Benefícios)
4. **Conclusão Estratégica** (Sem convite comercial direto, foco em clareza).
"""

        estilo_html = f"""<style>
.post-body h2 {{ color: {GenesisConfig.COLOR_PRIMARY}; font-family: 'Segoe UI', Arial, sans-serif; }}
.post-body h3 {{ color: {GenesisConfig.COLOR_PRIMARY}; font-family: 'Segoe UI', Arial, sans-serif; }}
.post-body p {{ font-size: 19px; line-height: 1.6; }}
</style>"""

        return f"""
## GENESIS MAGNETO V.52.0 — QUALITY GOD MODE
**Objetivo:** Gerar texto final pronto para Blogger (HTML Fragment).

### 🛡️ PROTOCOLO DE VERACIDADE
{anti_hallucination_txt}

---

## 1. O CLIENTE ALVO
**PERFIL:** {p['nome']}
- **Dor:** {p['dor']}
- **Desejo:** {p['desejo']}
- **Gatilho:** {d['gatilho']}

## 2. O PRODUTO E CONTEXTO
- **ATIVO:** {ativo}
- **LOCAL:** {contexto_geo}
- **ZONEAMENTO:** {zoning_info}
- **TEMA:** {d['topico']}
- **FORMATO:** {self.get_format_instructions(d['formato'])}
{ancora_instruction}

---

## 3. REGRAS TÉCNICAS E JSON-LD
Você está escrevendo um **FRAGMENTO DE HTML** com JSON-LD embutido.

Use este estilo mínimo:
{estilo_html}

APLIQUE AS REGRAS DA CONSTITUIÇÃO:
{bloco_regras}

{bloco_qualidade}

---

## 6. CHECKLIST FINAL DE ENTREGA

1. LOG DE BASTIDORES
2. BLOCKCODE (HTML PURO + JSON-LD)
   - Inclua o Script JSON-LD:
     {script_json_ld}
   - Inclua o CTA Kit.com no final.
3. TÍTULO (H1)
4. MARCADORES: {tags_otimizadas}
5. DATA: {data_fmt}
6. LOCAL: Indaiatuba
7. DESCRIÇÃO (Meta)
8. IMAGEM (Prompt)
""".strip()


# =========================================================
# UI STREAMLIT
# =========================================================

def main():
    THEME = {
        "primary": "#003366",
        "accent": "#D4AF37",
        "bg": "#f4f6f9"
    }

    st.set_page_config(page_title="Genesis Agency v12 (God Mode)", page_icon="⚡", layout="wide")

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

    # Inicializar dados fora do botão para preencher os selects
    try:
        dados_mestre = GenesisData()
        config_mestre = GenesisConfig()
    except RuntimeError as e:
        st.error(f"Erro ao carregar dados: {e}")
        return

    # Mapeamento para nomes amigáveis nos Selects
    persona_map = {k: v['nome'] for k, v in config_mestre.PERSONAS.items()}
    persona_reverse_map = {v: k for k, v in persona_map.items()} # Nome -> Key
    
    lista_bairros = sorted([b['nome'] for b in dados_mestre.bairros])
    lista_topicos = sorted(list(dados_mestre.topics.values()))
    lista_ativos = dados_mestre.todos_ativos
    
    # Sidebar: Personalização Total
    with st.sidebar:
        st.header("⚡ GOD MODE CONFIG")
        data_escolhida = st.date_input("Data de Publicação", datetime.date.today())
        
        st.markdown("---")
        st.markdown("**Personalização Fina**")
        st.caption("Deixe em 'ALEATÓRIO' para usar a IA.")

        sel_persona_nome = st.selectbox("1. Persona / Cliente", ["ALEATÓRIO"] + list(persona_map.values()))
        sel_bairro = st.selectbox("2. Bairro ou Macro", ["ALEATÓRIO"] + lista_bairros)
        sel_topico = st.selectbox("3. Tópico / Tema", ["ALEATÓRIO"] + lista_topicos)
        sel_ativo = st.selectbox("4. Tipo de Imóvel", ["ALEATÓRIO"] + lista_ativos)
        sel_formato = st.selectbox("5. Formato do Texto", ["ALEATÓRIO"] + config_mestre.CONTENT_FORMATS)
        sel_gatilho = st.selectbox("6. Gatilho Emocional", ["ALEATÓRIO"] + config_mestre.EMOTIONAL_TRIGGERS)

        st.markdown("---")
        if st.button("🔄 Resetar"):
            st.rerun()

    # Header
    c1, c2 = st.columns([3, 1])
    with c1:
        st.title("⚡ GENESIS AGENCY V12.0")
        st.markdown(f"**AI Content Director (Engine: {GenesisConfig.VERSION})**")
    with c2:
        st.image(
            "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhtRYbYvSxR-IRaFMCb95rCMmr1pKSkJKSVGD2SfW1h7e7M-NbCly3qk9xKK5lYpfOPYfq-xkzJ51p14cGftPHLF7MrbM0Szz62qQ-Ff5H79-dMiUcNzhrEL7LXKf089Ka2yzGaIX-UJBgTtdalNaWYPS0JSSfIMYNIE4yxhisKcU8j-gtOqXq6lSmgiSA/s600/1000324271.png",
            width=100
        )

    col_main, col_view = st.columns([1, 2])

    with col_main:
        st.info("Personalize as variáveis na barra lateral ou clique direto para modo surpresa.")
        generate_btn = st.button("CRIAR PAUTA CUSTOMIZADA ✨")

    if generate_btn:
        try:
            with st.spinner("Compilando estratégia personalizada..."):
                # Instancia engine
                eng = GenesisEngine(dados_mestre)
                regras = GenesisRules()

                # Datas
                hoje_iso = datetime.datetime.now().strftime(f"%Y-%m-%dT%H:%M:%S{GenesisConfig.FUSO_PADRAO}")
                d_pub = data_escolhida.strftime(f"%Y-%m-%dT00:00:00{GenesisConfig.FUSO_PADRAO}")

                # Prepara dicionário de seleção do usuário
                # Precisamos converter o nome amigável da persona de volta para a KEY
                persona_key_sel = "ALEATÓRIO"
                if sel_persona_nome != "ALEATÓRIO":
                    persona_key_sel = persona_reverse_map[sel_persona_nome]

                user_selection = {
                    "persona_key": persona_key_sel,
                    "bairro_nome": sel_bairro,
                    "topico": sel_topico,
                    "ativo": sel_ativo,
                    "formato": sel_formato,
                    "gatilho": sel_gatilho
                }

                # Executa engine com as preferências
                dados = eng.run(user_selection)

                # Ajusta regras locais
                if dados["modo"] == "BAIRRO" and dados["bairro"]:
                    contexto_local = dados["bairro"]["nome"]
                else:
                    contexto_local = "Indaiatuba"
                regras_ajustadas = regras.get_for_prompt(contexto_local)

                # Gera Prompt
                bld = PromptBuilder()
                prompt_final = bld.build(dados, d_pub, hoje_iso, regras_ajustadas)

                # Nome arquivo
                p_name = slugify(dados['persona']['nome'])[:10]
                ativo_name = slugify(dados['ativo_definido'])[:10]
                nome_arquivo = f"{d_pub.split('T')[0]}_V52_GodMode_{p_name}_{ativo_name}.txt"

        except Exception as e:
            with col_view:
                st.error(f"Erro na execução: {e}")
            return

        # Visualização
        bairro_display = dados['bairro']['nome'] if dados['bairro'] else "Indaiatuba (Geral)"
        zona_display = dados['bairro']['zona'] if dados['bairro'] else "Macro-zona"

        with col_view:
            st.markdown(f"""
            <div class="big-card">
                <div style="display:grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                    <div>
                        <div class="stat-label">Persona</div>
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
                        <div class="stat-label">Tópico & Gatilho</div>
                        <div class="stat-value highlight">{dados['topico']}</div>
                        <small>{dados['gatilho']}</small>
                    </div>
                </div>
                <hr style="opacity: 0.2">
                <small>Modo: {dados['modo']} | {dados['obs_tecnica']}</small>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("### 📋 Prompt Final (God Mode)")
            st.text_area("Copie para a IA:", value=prompt_final, height=450)
            
            st.download_button(
                label="💾 BAIXAR PAUTA (.txt)",
                data=prompt_final,
                file_name=nome_arquivo,
                mime="text/plain"
            )

if __name__ == "__main__":
    main()