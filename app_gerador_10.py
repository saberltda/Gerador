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
# 🏛️ GENESIS AGENCY CORE (V10.1 - FIXED JSON-LD & BLOCKCODE)
# Correção crítica: JSON-LD agora tratado como raw string segura
# ==============================================================================

class AgencyConfig:
    VERSION = "GENESIS 10.1 (FIXED JSON-LD & BLOCKCODE)"
    BLOG_URL = "https://blog.saber.imb.br"
    FUSO_PADRAO = "-03:00"

    LEAD_SCRIPT = '<div style="text-align:center; margin: 40px 0;"><script async data-uid="d188d73e78" src="https://sabernovidades.kit.com/d188d73e78/index.js"></script></div>'

    THEME = {
        "primary": "#003366",
        "accent": "#D4AF37",
        "bg": "#f4f6f9"
    }

    # Logo oficial (conforme REGRAS.txt)
    LOGO_URL = "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEixiE1KghKkH0E-I53yyi5zoT7eRX0lxCGLpcWLGAmEE5st8OfHfuzbxfiygwCWRqAdSfpmjAhM8-SogHDU_1gXCX6IHrjW1BaUc87un1lF1o6y2Et7eV0m3gJgvfJs3HsAGyAcPYk8Tl_65rlQmgAp5orRZqtLDvixbCUwscTT8ZJO-7zckc36rNkWHz4/s1600/1000318124.png"

    # JSON-LD como string RAW (evita problemas de aspas e quebras)
    @staticmethod
    def get_json_ld_template(iso_date):
        return f'''<script type="application/ld+json">
{{
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    "headline": "INSIRA O TITULO H1 AQUI",
    "datePublished": "{iso_date}",
    "dateModified": "{datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S-03:00')}",
    "author": {{ "@type": "Organization", "name": "Imobiliária Saber" }},
    "publisher": {{
        "@type": "Organization",
        "name": "Imobiliária Saber",
        "logo": {{ "@type": "ImageObject", "url": "{AgencyConfig.LOGO_URL}" }}
    }}
}}
</script>'''

    # ... (mantenha aqui as outras configurações: SEMANTIC_ENTITIES, NEURO_TRIGGERS, PERSONAS, STRICT_GUIDELINES, RULES, VOCABULARY_MATRIX, REGRAS_TECNICAS, REGRAS_TABELA, PROTOCOLO_PESQUISA)

    REGRAS_TECNICAS = """..."""   # copie exatamente do REGRAS.txt
    REGRAS_TABELA = """..."""     # copie exatamente do REGRAS.txt

# ==============================================================================
# Função auxiliar para escapar string para dentro de código markdown
# ==============================================================================
def escape_for_code_block(text):
    return text.replace("```", "\\`\\`\\`").replace("{", "{{").replace("}", "}}")

# ==============================================================================
# Lógica de geração do prompt (simplificada para foco no BLOCKCODE/JSON-LD)
# ==============================================================================

def gerar_prompt_completo(persona, bairro, estrategia, data_pub):
    p = persona
    b = bairro
    gatilho_nome = estrategia['gatilho_nome']
    gatilho_desc = estrategia['gatilho_desc']
    ativo = estrategia['ativo']
    semantic_list = ", ".join(estrategia['cluster_semantic'])

    date_fmt = data_pub.strftime("%d de %B de %Y").replace("January", "janeiro").replace("February", "fevereiro") # ... continue para todos os meses
    iso_date = data_pub.strftime(f"%Y-%m-%dT09:00:00{AgencyConfig.FUSO_PADRAO}")

    json_ld = AgencyConfig.get_json_ld_template(iso_date)

    prompt = f"""
# 🛑 ZONA DE SEGURANÇA MÁXIMA – NÃO ALTERAR NADA ABAIXO

{AgencyConfig.REGRAS_TECNICAS}

{AgencyConfig.REGRAS_TABELA}

## INSTRUÇÃO CRÍTICA SOBRE JSON-LD
Você **NÃO PODE** modificar, reescrever, indentar diferente ou alterar qualquer caractere do bloco JSON-LD abaixo.
Copie e cole **EXATAMENTE** como está dentro do BLOCKCODE HTML, no início do conteúdo.

**BLOCO JSON-LD OBRIGATÓRIO (não toque):**