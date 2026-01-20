# src/builder.py
import datetime
from .config import GenesisConfig

class PromptBuilder:
    """
    O 'Redator'.
    Responsável por montar a string final do Prompt que será enviada para a IA.
    Ele injeta o JSON-LD, o CSS inline e garante que as regras do arquivo TXT
    estejam visíveis para o modelo.
    """

    def __init__(self):
        pass

    def _format_date_blogger(self, iso_date_str):
        """Converte AAAA-MM-DD para 'DD de mmm. de AAAA' (Estilo Blogger)"""
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
        """Gera as tags (marcadores) do post com base na inteligência de cluster."""
        tags = ["Indaiatuba", "Imóveis Indaiatuba"]
        
        # Mapa de tags por cluster (Hardcoded para performance)
        cluster_map = {
            "HIGH_END": ["Altíssimo Padrão", "Casas de Luxo", "Condomínios Fechados", "Mansões Indaiatuba"],
            "FAMILY": ["Qualidade de Vida", "Casas em Condomínio", "Morar com Família", "Segurança"],
            "URBAN": ["Apartamentos", "Centro de Indaiatuba", "Oportunidade", "Imóveis Urbanos"],
            "INVESTOR": ["Investimento Imobiliário", "Mercado Imobiliário", "Valorização", "Terrenos"],
            "LOGISTICS": ["Galpões Industriais", "Logística", "Área Industrial", "Aeroporto Viracopos"],
            "CORPORATE": ["Salas Comerciais", "Escritórios", "Imóveis Corporativos"]
        }
        
        # Adiciona tags do cluster técnico
        tags.extend(cluster_map.get(d['cluster_tecnico'], []))

        # Adiciona tags específicas do bairro (se houver)
        if d['modo'] == "BAIRRO" and d['bairro']:
            tags.append(d['bairro']['nome'])
            tags.append(f"Morar no {d['bairro']['nome']}")
            tags.append(d['bairro']['zona'])

        # Adiciona o tipo de ativo limpo (ex: "Casa / Sobrado" -> "Casa")
        ativo_clean = d['ativo_definido'].split("/")[0].strip()
        tags.append(ativo_clean)

        # Remove duplicatas mantendo a ordem (set não garante ordem)
        seen = set()
        final_tags = []
        for t in tags:
            if t not in seen:
                seen.add(t)
                final_tags.append(t)

        return ", ".join(final_tags[:10]) # Limita a 10 tags

    def get_format_instructions(self, formato):
        """Instruções de redação específicas para cada formato de conteúdo."""
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
        """
        O GRANDE MONTADOR.
        Junta todas as peças (Persona, Bairro, Regras, SEO) e cria o texto final.
        """
        data_fmt = self._format_date_blogger(data_pub)
        p = d['persona']
        ativo = d['ativo_definido']
        tags_otimizadas = self._generate_seo_tags(d)

        # Bloco JSON-LD (Schema.org) para o Google entender o post
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

        # Contexto geográfico para o prompt
        if d['modo'] == "BAIRRO" and d['bairro']:
            contexto_geo = f"Bairro Específico: {d['bairro']['nome']}"
            zoning_info = f"Zoneamento oficial: {d['bairro']['zona']} ({d['obs_tecnica']})"
        else:
            contexto_geo = "Cidade: Indaiatuba (Panorama Geral, sem bairro específico)"
            zoning_info = "Macro-zoneamento urbano (foco na cidade como um todo)."

        # Regras de Anti-Alucinação (extraídas do Config)
        anti_hallucination_txt = "\n".join([f"- {rule}" for rule in GenesisConfig.STRICT_GUIDELINES])

        # Instrução de Âncora (Google Maps mental)
        ancora_instruction = f"""
**ÂNCORAS LOCAIS (MODO SEARCH):**
- EXECUTE busca mental como se estivesse usando Google Maps para o contexto: {contexto_geo}.
- Identifique de 3 a 5 estabelecimentos REAIS (escolas, mercados, serviços de saúde).
- Use tempos de deslocamento REALISTAS.
- PROIBIDO usar nomes genéricos.
"""

        # Bloco de Regras lido do arquivo TXT (Já com o nome do bairro injetado)
        bloco_regras = f"""
# ==========================================
# 🔐 ZONA DE SEGURANÇA MÁXIMA (REGRAS.txt)
# ==========================================
{regras_texto_ajustada}
"""

        # CSS inline para garantir beleza no Blogger
        estilo_html = f"""<style>
.post-body h2 {{ color: {GenesisConfig.COLOR_PRIMARY}; font-family: 'Segoe UI', Arial, sans-serif; }}
.post-body h3 {{ color: {GenesisConfig.COLOR_PRIMARY}; font-family: 'Segoe UI', Arial, sans-serif; }}
.post-body p {{ font-size: 19px; line-height: 1.6; }}
</style>"""

        # RETORNO FINAL: O Prompt completo
        return f"""
## GENESIS MAGNETO V.53.0 — QUALITY GOD MODE
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

## 4. ESTRUTURA MÍNIMA DO TEXTO
1. **Introdução enxuta**
2. **Diagnóstico da Situação** (Dor: {p['dor']} -> Desejo: {p['desejo']})
3. **Corpo Técnico** (Rotina, Dados, Riscos x Benefícios)
4. **Conclusão Estratégica** (Sem convite comercial direto, foco em clareza).

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