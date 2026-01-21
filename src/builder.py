# src/builder.py
import datetime
import re
from .config import GenesisConfig

class PromptBuilder:
    """
    O 'Redator'.
    Responsável por montar a string final do Prompt que será enviada para a IA.
    Agora com CTA de Captura (Kit.com) obrigatório em todos os modos e JSON-LD seguro.
    """

    # O HTML EXATO QUE VOCÊ QUER NO FINAL DOS POSTS
    CTA_CAPTURE_CODE = """<div style="text-align:center; margin: 40px 0;"><script async data-uid="d188d73e78" src="https://sabernovidades.kit.com/d188d73e78/index.js"></script></div>"""

    def __init__(self):
        pass

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
        tags = ["Indaiatuba", "Indaiatuba SP"]
        
        # Usa o código robusto (IMOBILIARIA ou PORTAL)
        if d.get('tipo_pauta') == "PORTAL" or (d.get('cluster_tecnico') == "PORTAL"):
            tags.append("Notícias Indaiatuba")
            tags.append("Utilidade Pública")
            tags.append("Portal da Cidade")
            tags.append("Viver em Indaiatuba")
        else:
            tags.append("Imóveis Indaiatuba")
            tags.append("Mercado Imobiliário")
            
            cluster_map = {
                "HIGH_END": ["Altíssimo Padrão", "Casas de Luxo", "Condomínios Fechados", "Mansões Indaiatuba"],
                "FAMILY": ["Qualidade de Vida", "Casas em Condomínio", "Morar com Família", "Segurança"],
                "URBAN": ["Apartamentos", "Centro de Indaiatuba", "Oportunidade", "Imóveis Urbanos"],
                "INVESTOR": ["Investimento Imobiliário", "Mercado Imobiliário", "Valorização", "Terrenos"],
                "LOGISTICS": ["Galpões Industriais", "Logística", "Área Industrial", "Aeroporto Viracopos"],
                "CORPORATE": ["Salas Comerciais", "Escritórios", "Imóveis Corporativos"]
            }
            tags.extend(cluster_map.get(d.get('cluster_tecnico', 'FAMILY'), []))

        if d['modo'] == "BAIRRO" and d['bairro']:
            tags.append(d['bairro']['nome'])
            tags.append(f"Viver no {d['bairro']['nome']}")

        if d['ativo_definido']:
            ativo_clean = d['ativo_definido'].split("(")[0].strip()
            tags.append(ativo_clean)

        seen = set()
        final_tags = []
        for t in tags:
            t_clean = t.replace("/", "").strip()
            if t_clean and t_clean not in seen:
                seen.add(t_clean)
                final_tags.append(t_clean)

        return ", ".join(final_tags[:12])

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
        # Proteção extra: aplica placeholders de forma redundante se o app.py ou database não tiverem aplicado
        if d['modo'] == "BAIRRO" and d['bairro']:
            local_nome = d['bairro']['nome']
        else:
            local_nome = "Indaiatuba"
            
        regras_texto_ajustada = regras_texto_ajustada.replace("{{BAIRRO}}", local_nome)
        regras_texto_ajustada = regras_texto_ajustada.replace("{{LOCAL}}", local_nome)

        if d.get('tipo_pauta') == "PORTAL" or (d.get('cluster_tecnico') == "PORTAL"):
            return self._build_portal_prompt(d, data_pub, data_mod, regras_texto_ajustada)
        else:
            return self._build_real_estate_prompt(d, data_pub, data_mod, regras_texto_ajustada)

    # =========================================================================
    # 🧠 MODO 1: IMOBILIÁRIA (Foco em Vendas, Dor, Desejo)
    # =========================================================================
    def _build_real_estate_prompt(self, d, data_pub, data_mod, regras_texto_ajustada):
        data_fmt = self._format_date_blogger(data_pub)
        p = d['persona']
        ativo = d['ativo_definido']
        tags_otimizadas = self._generate_seo_tags(d)

        script_json_ld = self._get_json_ld(data_pub, data_mod, "Imobiliária Saber", d['ativo_definido'])

        if d['modo'] == "BAIRRO" and d['bairro']:
            contexto_geo = f"Bairro Específico: {d['bairro']['nome']}"
            zoning_info = f"Zoneamento oficial: {d['bairro']['zona']} ({d['obs_tecnica']})"
        else:
            contexto_geo = "Cidade: Indaiatuba (Panorama Geral, sem bairro específico)"
            zoning_info = "Macro-zoneamento urbano (foco na cidade como um todo)."

        anti_hallucination_txt = "\n".join([f"- {rule}" for rule in GenesisConfig.STRICT_GUIDELINES])

        estilo_html = f"""<style>
.post-body h2 {{ color: {GenesisConfig.COLOR_PRIMARY}; font-family: 'Segoe UI', Arial, sans-serif; }}
.post-body h3 {{ color: {GenesisConfig.COLOR_PRIMARY}; font-family: 'Segoe UI', Arial, sans-serif; }}
.post-body p {{ font-size: 19px; line-height: 1.6; }}
</style>"""

        ancora_instruction = f"""
**ÂNCORAS LOCAIS (MODO SEARCH):**
- EXECUTE busca mental como se estivesse usando Google Maps para o contexto: {contexto_geo}.
- Identifique de 3 a 5 estabelecimentos REAIS.
- Use tempos de deslocamento REALISTAS.
- ALERTA: Cuidado com nomes de bairros similares que são distantes entre si.
"""

        bloco_regras = f"""
# ==========================================
# 🔐 ZONA DE SEGURANÇA MÁXIMA (REGRAS.txt)
# ==========================================
{regras_texto_ajustada}
"""

        return f"""
## GENESIS MAGNETO V.7.5 — IMOBILIÁRIA MODE
**Objetivo:** Texto de Conversão Imobiliária (SOMENTE VENDAS - NÃO TRABALHAMOS COM LOCAÇÃO).

### 🛡️ PROTOCOLO DE VERACIDADE
{anti_hallucination_txt}

---

## ⛔ TRAVA ANTI-ANÚNCIO (CRÍTICO)
1. **NÃO VENDA UMA UNIDADE ESPECÍFICA.** Não descreva uma casa como se ela existisse (ex: "esta sala").
2. **VENDA O CONCEITO.** Fale sobre o **Padrão Construtivo** da região.
   - ERRADO: "Esta casa tem piscina."
   - CERTO: "Imóveis neste condomínio costumam oferecer lazer completo..."
3. **ZERO LOCAÇÃO:** Não mencione aluguel ou inquilinos. Foco total em Compra/Venda/Investimento.

---

## 1. O CLIENTE ALVO
**PERFIL:** {p['nome']}
- **Dor:** {p['dor']}
- **Desejo:** {p['desejo']}
- **Gatilho:** {d['gatilho']}

## 2. O PRODUTO E CONTEXTO
- **ATIVO (TIPOLOGIA):** {ativo}
- **LOCAL:** {contexto_geo}
- **ZONEAMENTO:** {zoning_info}
- **TEMA:** {d['topico']}
- **FORMATO:** {self.get_format_instructions(d['formato'])}
{ancora_instruction}

---

## 3. ESTRUTURA DO TEXTO
Use este estilo HTML:
{estilo_html}

APLIQUE AS REGRAS:
{bloco_regras}

**Estrutura:**
1. **Introdução:** Conecte a dor do cliente ao bairro.
2. **Diagnóstico:** Por que {d['bairro']['nome'] if d['bairro'] else 'Indaiatuba'} é a solução?
3. **Tipologia:** Vantagens de "{ativo}" (categoria).
4. **Conclusão:** NÃO CONVIDE PARA CONVERSAR/WHATSAPP. O objetivo é fazer o leitor baixar o material ou se inscrever na lista abaixo. Encerre gerando curiosidade para o conteúdo extra.

---

## 4. CHECKLIST DE ENTREGA (OBRIGATÓRIO)
1. LOG DE BASTIDORES
2. BLOCKCODE HTML (Código Puro) contendo:
   - O Script JSON-LD abaixo:
     {script_json_ld}
   - **OBRIGATÓRIO: Ao final do texto, insira EXATAMENTE este código de captura:**
     {self.CTA_CAPTURE_CODE}
3. TÍTULO (H1)
4. MARCADORES: {tags_otimizadas}
5. DATA: {data_fmt}
6. DESCRIÇÃO
7. IMAGEM PROMPT
""".strip()

    # =========================================================================
    # 🧠 MODO 2: PORTAL DA CIDADE (Foco em Notícia -> Conversão)
    # =========================================================================
    def _build_portal_prompt(self, d, data_pub, data_mod, regras_texto_ajustada):
        data_fmt = self._format_date_blogger(data_pub)
        ativo = d['ativo_definido']
        tags_otimizadas = self._generate_seo_tags(d)
        
        estilo_html = f"""<style>
.post-body h2 {{ color: #2c3e50; font-family: 'Georgia', serif; border-bottom: 2px solid #eee; padding-bottom: 10px; }}
.post-body h3 {{ color: {GenesisConfig.COLOR_PRIMARY}; font-family: 'Segoe UI', Arial, sans-serif; margin-top: 25px; }}
.post-body p {{ font-size: 19px; line-height: 1.6; color: #333; }}
.post-body .destaque {{ background: #f9f9f9; padding: 15px; border-left: 4px solid {GenesisConfig.COLOR_PRIMARY}; font-style: italic; margin: 20px 0; }}
</style>"""

        script_json_ld = self._get_json_ld(data_pub, data_mod, "Portal Saber Indaiatuba", d['ativo_definido'])
        local_foco = d['bairro']['nome'] if (d['modo'] == "BAIRRO" and d['bairro']) else "Indaiatuba (Cidade toda)"
        anti_hallucination_txt = "\n".join([f"- {rule}" for rule in GenesisConfig.STRICT_GUIDELINES])

        return f"""
## GENESIS MAGNETO V.7.5 — JOURNALIST TO SALES MODE
**Objetivo:** Texto Jornalístico que converte em LEAD Imobiliário.

### 🚨 PROTOCOLO DE JORNALISMO
1. **FATOS REAIS:** Busque fatos reais recentes (2025-2026) sobre "{ativo}". Se não houver, faça um GUIA DE UTILIDADE PÚBLICA.
2. **TOM:** Comece informativo, termine consultivo.
3. **A PONTE:** Use a notícia para provar que a cidade é boa para MORAR.

---

## 1. A PAUTA
- **TEMA:** {ativo}
- **LOCAL:** {local_foco}
- **GATILHO:** {d['gatilho']}

## 2. ESTRUTURA DO TEXTO (HTML)
Use este estilo HTML:
{estilo_html}

**ROTEIRO OBRIGATÓRIO:**
1. **Manchete (H1):** Informativa.
2. **Desenvolvimento:** O que, onde, quando (Notícia ou Guia).
3. **A PONTE (CRÍTICO):** Conecte o tema (ex: nova obra) com a valorização imobiliária ou qualidade de vida.
4. **CONCLUSÃO DE VENDA:**
   - Encerre oferecendo ajuda para morar na cidade.
   - NÃO CONVIDE PARA BATE-PAPO. O foco é a inscrição na newsletter abaixo.

---

## 3. CHECKLIST DE ENTREGA (OBRIGATÓRIO)
1. LOG BASTIDORES
2. BLOCKCODE HTML (Código Puro) contendo:
   - O Script JSON-LD abaixo:
     {script_json_ld}
   - **OBRIGATÓRIO: Ao final do texto, insira EXATAMENTE este código de captura:**
     {self.CTA_CAPTURE_CODE}
3. TÍTULO (H1)
4. MARCADORES: {tags_otimizadas}
5. DATA: {data_fmt}
6. DESCRIÇÃO
7. IMAGEM PROMPT
""".strip()

    def _get_json_ld(self, d_pub, d_mod, author_name, headline):
        # PROTEÇÃO: Escapar aspas para não quebrar o JSON
        safe_headline = headline.replace('"', '\\"')
        safe_author = author_name.replace('"', '\\"')
        
        return """
<script type="application/ld+json">
{
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    "headline": "%s",
    "datePublished": "%s",
    "dateModified": "%s",
    "author": { "@type": "Organization", "name": "%s" },
    "publisher": {
        "@type": "Organization",
        "name": "Imobiliária Saber",
        "logo": { "@type": "ImageObject", "url": "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhtRYbYvSxR-IRaFMCb95rCMmr1pKSkJKSVGD2SfW1h7e7M-NbCly3qk9xKK5lYpfOPYfq-xkzJ51p14cGftPHLF7MrbM0Szz62qQ-Ff5H79-dMiUcNzhrEL7LXKf089Ka2yzGaIX-UJBgTtdalNaWYPS0JSSfIMYNIE4yxhisKcU8j-gtOqXq6lSmgiSA/s600/1000324271.png" }
    }
}
</script>
""" % (safe_headline, d_pub, d_mod, safe_author)
