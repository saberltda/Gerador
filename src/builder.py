# src/builder.py
import datetime
import json
from .config import GenesisConfig

class PromptBuilder:
    CTA_CAPTURE_CODE = """<div style="text-align:center; margin: 40px 0;"><script async data-uid="d188d73e78" src="https://sabernovidades.kit.com/d188d73e78/index.js"></script></div>"""

    def _format_date_blogger(self, iso_date_str):
        try:
            if isinstance(iso_date_str, datetime.datetime): dt = iso_date_str
            else: dt = datetime.datetime.strptime(iso_date_str.split("T")[0], "%Y-%m-%d")
            meses = {1:"jan.", 2:"fev.", 3:"mar.", 4:"abr.", 5:"mai.", 6:"jun.", 7:"jul.", 8:"ago.", 9:"set.", 10:"out.", 11:"nov.", 12:"dez."}
            return f"{dt.day} de {meses[dt.month]} de {dt.year}"
        except: return iso_date_str

    def _generate_seo_tags(self, d):
        tags = ["Indaiatuba", "Imóveis Indaiatuba"]
        if d.get('bairro'): tags.append(d['bairro']['nome'])
        if d.get('ativo_definido'): tags.append(d['ativo_definido'].split('/')[0])
        if d.get('formato'): tags.append(d['formato'])
        return ", ".join(tags[:10])

    def _get_structural_guidelines(self, formato_key, cluster_key, bairro_nome):
        # ... (Mantém as estruturas que já definimos para Imobiliária) ...
        # (Código omitido para brevidade, mantém igual ao V.56)
        if formato_key == "LISTA_POLEMICA": return f"## 5. ESTRUTURA: LISTA POLÊMICA\n- H2: Mito #1\n- H2: Mito #2\n- H2: A Verdade"
        if formato_key == "COMPARATIVO_TECNICO": return f"## 5. ESTRUTURA: BATALHA (VS)\n- H2: Round 1\n- H2: Round 2\n- H2: Veredito"
        if formato_key == "GUIA_DEFINITIVO": return f"## 5. ESTRUTURA: MANUAL COMPLETO\n- H2: Cap 1: Raio-X\n- H2: Cap 2: Infra\n- H2: Checklist"
        if formato_key == "PERGUNTAS_RESPOSTAS": return f"## 5. ESTRUTURA: FAQ\n- H2: Pergunta 1\n- H2: Pergunta 2"
        return f"## 5. ESTRUTURA PADRÃO\n- H2: Contexto\n- H2: Análise\n- H2: Conclusão"

    def _get_tone_guidelines(self, gatilho_key):
        # ... (Mantém igual ao V.56) ...
        if gatilho_key == "ESCASSEZ": return "### TOM: ESCASSEZ\nFoco em 'última chance', raro, exclusivo."
        if gatilho_key == "URGENCIA": return "### TOM: URGÊNCIA\nFoco em 'agora', tempo acabando."
        if gatilho_key == "AUTORIDADE": return "### TOM: AUTORIDADE\nFoco em dados, seriedade, 'eu sei'."
        if gatilho_key == "CURIOSIDADE": return "### TOM: CURIOSIDADE\nFoco em segredo, 'poucos sabem'."
        return "### TOM: PADRÃO\nInformativo e prestativo."

    def build(self, d, data_pub, data_mod, regras_texto_ajustada):
        if d.get('tipo_pauta') == "PORTAL":
            return self._build_portal_prompt(d, data_pub, data_mod, regras_texto_ajustada)
        else:
            return self._build_real_estate_prompt(d, data_pub, data_mod, regras_texto_ajustada)

    def _build_real_estate_prompt(self, d, data_pub, data_mod, regras_texto_ajustada):
        # (Mantém igual à versão anterior V.56 que você aprovou)
        data_fmt = self._format_date_blogger(data_pub)
        ativo = d['ativo_definido']
        bairro_nome = d['bairro']['nome'] if d['bairro'] else "Indaiatuba"
        cluster_key = d.get('cluster_tecnico', 'FAMILY')
        formato_key = d.get('formato', 'GUIA_DEFINITIVO')
        gatilho_key = d.get('gatilho', 'AUTORIDADE')
        
        historico_txt = "\n".join([f"- {t}" for t in d.get('historico_titulos', [])])
        
        estilo_html = f"<style>.post-body h2 {{ color: {GenesisConfig.COLOR_PRIMARY}; }}</style>" # Simplificado para visualização
        
        structural_guidelines = self._get_structural_guidelines(formato_key, cluster_key, bairro_nome)
        tone_guidelines = self._get_tone_guidelines(gatilho_key)

        return f"""
## GENESIS MAGNETO V.58 — REAL ESTATE ENGINE
... (Conteúdo padrão Imobiliária, estruturado e com tom) ...
{structural_guidelines}
{tone_guidelines}
...
""".strip()

    def _build_portal_prompt(self, d, data_pub, data_mod, regras_texto_ajustada):
        # AGORA O PORTAL TAMBÉM USA INTELIGÊNCIA DE ESTRUTURA E TOM
        data_fmt = self._format_date_blogger(data_pub)
        formato_key = d.get('formato', 'GUIA_DEFINITIVO')
        gatilho_key = d.get('gatilho', 'AUTORIDADE')
        
        # Adaptação das diretrizes para contexto de Notícia
        structural_guidelines = self._get_structural_guidelines(formato_key, "PORTAL", d['bairro']['nome'] if d['bairro'] else "Cidade")
        tone_guidelines = self._get_tone_guidelines(gatilho_key)

        return f"""
## GENESIS MAGNETO V.58 — PORTAL NEWS ENGINE
**Objetivo:** Notícia de Utilidade Pública / Blog da Cidade.

## 1. A PAUTA
- **MANCHETE (TEMA):** {d['ativo_definido']}
- **LOCAL:** {d['bairro']['nome'] if d['bairro'] else 'Indaiatuba'}
- **ÂNGULO EDITORIAL:** {d.get('topico', 'Geral')}
- **FORMATO:** {formato_key}
- **GATILHO MENTAL:** {gatilho_key}

## 2. INSTRUÇÕES DE ESTRUTURA E TOM
Embora seja uma notícia/utilidade, aplique estas diretrizes para torná-la interessante:

{structural_guidelines}

{tone_guidelines}

## 3. CTA
{self.CTA_CAPTURE_CODE}

## 4. REGRAS GERAIS
{regras_texto_ajustada}
""".strip()
