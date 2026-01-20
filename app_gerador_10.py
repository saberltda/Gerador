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
# 🏛️ GENESIS AGENCY CORE (V9.1)
# Atualização: Correção de Encapsulamento JSON-LD e Compliance REGRAS.txt
# ==============================================================================

class AgencyConfig:
    VERSION = "GENESIS 9.1 (STABLE COMPLIANCE MODE)"
    BLOG_URL = "https://blog.saber.imb.br"
    # Script de captura conforme REGRAS.txt
    LEAD_SCRIPT = '<div style="text-align:center; margin: 40px 0;"><script async data-uid="d188d73e78" src="https://sabernovidades.kit.com/d188d73e78/index.js"></script></div>'
    
    THEME = {
        "primary": "#003366", # Azul Saber
        "accent": "#D4AF37",  # Ouro (Premium)
        "bg": "#f4f6f9"
    }

    SEMANTIC_ENTITIES = {
        "FAMILY": ["Colégio Objetivo", "Parque Ecológico", "Segurança Monitorada", "Ciclovias", "Qualidade do Ar"],
        "INVESTOR": ["Valorização do m²", "Liquidez", "Plano Diretor", "Vetores de Crescimento", "Hub Logístico"],
        "HIGH_END": ["Helvetia", "Arquitetura Contemporânea", "Privacidade Absoluta", "Pé Direito Duplo", "Acabamento Premium"],
        "LOGISTICS": ["Aeroporto de Viracopos", "Rodovia Santos Dumont", "Galpões Modulares", "Last Mile"]
    }

    NEURO_TRIGGERS = {
        "ESCASSEZ_REAL": "Enfatize que lotes/imóveis nesta zona específica são finitos e raros de aparecer à venda.",
        "CONTRASTE_DOR": "Comece descrevendo vividamente o caos de SP (trânsito/barulho) para contrastar com a paz de Indaiatuba.",
        "AUTORIDADE_DADOS": "Use números precisos (distâncias em minutos, metros quadrados) para gerar confiança racional.",
        "PERTENCIMENTO": "Descreva a comunidade local como um clube exclusivo de pessoas que valorizam o bem-viver.",
        "PROVA_SOCIAL_IMPLICITA": "Mencione como 'novas famílias estão migrando' para validar a decisão de compra."
    }

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
# 🧠 CÉREBRO DA AGÊNCIA
# =========================================================

class AgencyBrain:
    def __init__(self):
        self.bairros = self._load_bairros()
        
    def _load_bairros(self):
        try:
            with open("bairros.json", "r", encoding="utf-8") as f:
                raw = json.load(f)
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
        p_key = random.choice(list(AgencyConfig.PERSONAS.keys()))
        persona = AgencyConfig.PERSONAS[p_key]
        
        candidatos = [b for b in self.bairros if b['zona_norm'] in persona['zonas_alvo']]
        if not candidatos: candidatos = self.bairros
        bairro = random.choice(candidatos)
        
        ativo = self._definir_ativo(persona['cluster'], bairro['zona_norm'])
        
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
# ✍️ PROMPT ARCHITECT (ENCAPSULADO)
# =========================================================

class PromptArchitect:
    def format_date_pt(self, date_obj):
        meses = {1:"jan.", 2:"fev.", 3:"mar.", 4:"abr.", 5:"mai.", 6:"jun.", 
                 7:"jul.", 8:"ago.", 9:"set.", 10:"out.", 11:"nov.", 12:"dez."}
        return f"{date_obj.day} de {meses[date_obj.month]} de {date_obj.year}"

    def build_prompt(self, strategy, pub_date):
        p = strategy['persona']
        b = strategy['bairro']
        date_fmt = self.format_date_pt(pub_date)
        iso_date = pub_date.strftime("%Y-%m-%dT09:00:00-03:00")
        semantic_list = ", ".join(strategy['cluster_semantic'])
        
        # LOGO URL (Conforme REGRAS.txt)
        logo_url = "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEixiE1KghKkH0E-I53yyi5zoT7eRX0lxCGLpcWLGAmEE5st8OfHfuzbxfiygwCWRqAdSfpmjAhM8-SogHDU_1gXCX6IHrjW1BaUc87un1lF1o6y2Et7eV0m3gJgvfJs3HsAGyAcPYk8Tl_65rlQmgAp5orRZqtLDvixbCUwscTT8ZJO-7zckc36rNkWHz4/s1600/1000318124.png"

        # ENCAPSULAMENTO DO JSON-LD
        # Criamos o template separadamente para evitar quebra de f-string no bloco principal
        json_ld_template = f"""
<script type="application/ld+json">
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
        "logo": {{ "@type": "ImageObject", "url": "{logo_url}" }}
    }}
}}
</script>
        """

        # PROMPT PRINCIPAL
        return f"""
# 🛑 ZONA DE SEGURANÇA MÁXIMA (LEIS DA FÍSICA DO V9)
Você deve seguir ESTRITAMENTE as regras abaixo. A violação quebrará o site.

## 1. REGRAS TÉCNICAS (HTML PURO)
* **PROIBIDO:** Usar `<!DOCTYPE html>`, `<html>`, `<head>`, `<body>`.
* **PROIBIDO:** Incluir tags `<meta>` ou `<title>`.
* **AÇÃO:** Comece DIRETAMENTE com o conteúdo visível (`<style>`, `<h2>`, `<p>`).

## 2. REGRAS DE DESIGN DE TABELAS (ANTI-QUEBRA MOBILE)
Para qualquer tabela gerada, você OBRIGATORIAMENTE deve aplicar este CSS Inline:
1. **Wrapper:** Envolva a tabela em `<div style="overflow-x: auto; width: 100%; margin-bottom: 20px;">`.
2. **Tag Table:** `<table style="width: 100%; min-width: 600px; border-collapse: collapse;">`
3. **Células (TH/TD):** Em TODAS as células aplique `style="padding: 12px; border: 1px solid #cccccc; word-break: keep-all; hyphens: none;"`

## 3. CHECKLIST DE ENTREGA (ORDEM IMUTÁVEL)
Sua resposta final deve seguir EXATAMENTE esta ordem numérica (1 a 8):
1. **LOG DE BASTIDORES:** (Explique a estratégia e locais reais escolhidos)
2. **BLOCKCODE:** (HTML Puro + JSON-LD embutido - SEM tags de estrutura html/body)
3. **TÍTULO:** (Apenas o texto do H1)
4. **MARCADORES:** (Tags separadas por vírgula: Indaiatuba, {b['nome']}, {strategy['ativo']}, Imóveis Indaiatuba)
5. **DATA:** {date_fmt}
6. **LOCAL:** Indaiatuba
7. **DESCRIÇÃO:** (Meta description focada na dor da persona: {p['dor']})
8. **IMAGEM:** (Prompt para IA generativa)

---

# BRIEFING ESTRATÉGICO
* **Persona:** {p['nome']} (Dores: {p['dor']})
* **Local:** {b['nome']} ({b['zona']})
* **Foco:** {strategy['ativo']}
* **Tom (Neuromarketing):** {strategy['gatilho_nome']} ({strategy['gatilho_desc']})
* **Entidades Semânticas:** {semantic_list}

# PROTOCOLO DE PESQUISA (ANTI-ALUCINAÇÃO)
⚠️ **CRÍTICO:** Simule o Google Maps.
1. Use APENAS locais REAIS de Indaiatuba próximos ao {b['nome']}.
2. Use tempos realistas (ex: "A 8 minutos do Parque Ecológico").
3. NUNCA invente depoimentos.

# ESTRUTURA DO CONTEÚDO (DENTRO DO BLOCKCODE)
1. **Estilos:** Comece com `<style> h2 {{ color: #003366; }} </style>`
2. **H1:** Persuasivo e com a palavra-chave.
3. **Intro:** Conecte a dor ({p['dor']}) à solução.
4. **Tabela:** Use as REGRAS DE DESIGN DE TABELAS acima para listar distâncias.
5. **JSON-LD (OBRIGATÓRIO):** Insira este script EXATO dentro do HTML (preenchendo headline):
```html
{json_ld_template}