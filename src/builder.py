# src/builder.py
import datetime
import re
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
        """Gera as tags (marcadores) do post com base na inteligência de cluster e texto."""
        tags = ["Indaiatuba", "Indaiatuba SP"]
        
        # Tags dinâmicas baseadas no modo
        if d.get('tipo_pauta') == "PORTAL" or (d.get('cluster_tecnico') == "PORTAL"):
            tags.append("Notícias Indaiatuba")
            tags.append("Utilidade Pública")
            tags.append("Portal da Cidade")
            tags.append("Viver em Indaiatuba")
        else:
            tags.append("Imóveis Indaiatuba")
            tags.append("Mercado Imobiliário")
            
            # Mapa de tags por cluster (Hardcoded para performance)
            cluster_map = {
                "HIGH_END": ["Altíssimo Padrão", "Casas de Luxo", "Condomínios Fechados", "Mansões Indaiatuba"],
                "FAMILY": ["Qualidade de Vida", "Casas em Condomínio", "Morar com Família", "Segurança"],
                "URBAN": ["Apartamentos", "Centro de Indaiatuba", "Oportunidade", "Imóveis Urbanos"],
                "INVESTOR": ["Investimento Imobiliário", "Mercado Imobiliário", "Valorização", "Terrenos"],
                "LOGISTICS": ["Galpões Industriais", "Logística", "Área Industrial", "Aeroporto Viracopos"],
                "CORPORATE": ["Salas Comerciais", "Escritórios", "Imóveis Corporativos"]
            }
            tags.extend(cluster_map.get(d.get('cluster_tecnico', 'FAMILY'), []))

        # Adiciona tags específicas do bairro (se houver)
        if d['modo'] == "BAIRRO" and d['bairro']:
            tags.append(d['bairro']['nome'])
            tags.append(f"Viver no {d['bairro']['nome']}")

        # Adiciona o tipo de ativo limpo
        if d['ativo_definido']:
            ativo_clean = d['ativo_definido'].split("(")[0].strip()
            tags.append(ativo_clean)

        # Remove duplicatas mantendo a ordem
        seen = set()
        final_tags = []
        for t in tags:
            t_clean = t.replace("/", "").strip()
            if t_clean and t_clean not in seen:
                seen.add(t_clean)
                final_tags.append(t_clean)

        return ", ".join(final_tags[:12])

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
        Decide qual 'Cérebro' usar: Corretor ou Jornalista.
        """
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

        # Bloco JSON-LD (Schema.org)
        script_json_ld = self._get_json_ld(data_pub, data_mod, "Imobiliária Saber", d['ativo_definido'])

        # Contexto geográfico
        if d['modo'] == "BAIRRO" and d['bairro']:
            contexto_geo = f"Bairro Específico: {d['bairro']['nome']}"
            zoning_info = f"Zoneamento oficial: {d['bairro']['zona']} ({d['obs_tecnica']})"
        else:
            contexto_geo = "Cidade: Indaiatuba (Panorama Geral, sem bairro específico)"
            zoning_info = "Macro-zoneamento urbano (foco na cidade como um todo)."

        # Regras Anti-Alucinação
        anti_hallucination_txt = "\n".join([f"- {rule}" for rule in GenesisConfig.STRICT_GUIDELINES])

        # CSS inline
        estilo_html = f"""<style>
.post-body h2 {{ color: {GenesisConfig.COLOR_PRIMARY}; font-family: 'Segoe UI', Arial, sans-serif; }}
.post-body h3 {{ color: {GenesisConfig.COLOR_PRIMARY}; font-family: 'Segoe UI', Arial, sans-serif; }}
.post-body p {{ font-size: 19px; line-height: 1.6; }}
</style>"""

        # Âncora
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

        return f"""
## GENESIS MAGNETO V.7.0 — IMOBILIÁRIA MODE
**Objetivo:** Texto de Conversão Imobiliária (HTML Fragment).

### 🛡️ PROTOCOLO DE VERACIDADE
{anti_hallucination_txt}

---

## ⛔ TRAVA ANTI-ANÚNCIO (CRÍTICO)
1. **VOCÊ NÃO ESTÁ VENDENDO UMA UNIDADE ESPECÍFICA.** Não descreva uma casa como se ela existisse.
2. **VOCÊ ESTÁ VENDENDO O CONCEITO.** Fale sobre o **Padrão Construtivo** da região.
   - ERRADO: "Esta casa tem..."
   - CERTO: "Nesta região, as casas costumam oferecer..."
3. **Foco na Curadoria:** Aja como um consultor explicando por que aquele *tipo* de imóvel naquele *bairro* resolve a dor do cliente.

---

## 1. O CLIENTE ALVO
**PERFIL:** {p['nome']}
- **Dor:** {p['dor']}
- **Desejo:** {p['desejo']}
- **Gatilho:** {d['gatilho']}

## 2. O PRODUTO E CONTEXTO
- **ATIVO (TIPOLOGIA):** {ativo} (Trate como categoria/padrão da região, não unidade única)
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
1. **Introdução Conectiva:** (Conecte a dor do cliente ao cenário atual do mercado e do bairro).
2. **Diagnóstico do Local:** (Por que {d['bairro']['nome'] if d['bairro'] else 'Indaiatuba'} é a solução? Cite as âncoras locais).
3. **Análise da Tipologia:** (Fale sobre as vantagens de morar em "{ativo}" de forma genérica/técnica).
4. **Conclusão Estratégica:** (Convite para receber uma curadoria personalizada de imóveis desse perfil).

---

## 6. CHECKLIST FINAL DE ENTREGA

1. LOG DE BASTIDORES
2. BLOCKCODE (HTML PURO + JSON-LD)
   - Inclua o Script JSON-LD:
     {script_json_ld}
   - Inclua o CTA Kit.com no final.
3. TÍTULO (H1) - (Deve ser atrativo e focar no benefício/bairro)
4. MARCADORES: {tags_otimizadas}
5. DATA: {data_fmt}
6. LOCAL: Indaiatuba
7. DESCRIÇÃO (Meta)
8. IMAGEM (Prompt)
""".strip()

    # =========================================================================
    # 🧠 MODO 2: PORTAL DA CIDADE (Foco em Notícia -> Conversão)
    # =========================================================================
    def _build_portal_prompt(self, d, data_pub, data_mod, regras_texto_ajustada):
        data_fmt = self._format_date_blogger(data_pub)
        ativo = d['ativo_definido'] # Ex: "Notícia de Trânsito", "Inauguração"
        tags_otimizadas = self._generate_seo_tags(d)
        
        estilo_html = f"""<style>
.post-body h2 {{ color: #2c3e50; font-family: 'Georgia', serif; border-bottom: 2px solid #eee; padding-bottom: 10px; }}
.post-body h3 {{ color: {GenesisConfig.COLOR_PRIMARY}; font-family: 'Segoe UI', Arial, sans-serif; margin-top: 25px; }}
.post-body p {{ font-size: 19px; line-height: 1.6; color: #333; }}
.post-body .destaque {{ background: #f9f9f9; padding: 15px; border-left: 4px solid {GenesisConfig.COLOR_PRIMARY}; font-style: italic; margin: 20px 0; }}
</style>"""

        script_json_ld = self._get_json_ld(data_pub, data_mod, "Portal Saber Indaiatuba", d['ativo_definido'])

        local_foco = d['bairro']['nome'] if (d['modo'] == "BAIRRO" and d['bairro']) else "Indaiatuba (Cidade toda)"

        # Regras Anti-Alucinação Simplificadas para Portal
        anti_hallucination_txt = "\n".join([f"- {rule}" for rule in GenesisConfig.STRICT_GUIDELINES])

        return f"""
## GENESIS MAGNETO V.7.0 — JOURNALIST TO SALES MODE
**Objetivo:** Texto Jornalístico/Utilidade que converte em LEAD Imobiliário.

### 🚨 PROTOCOLO DE JORNALISMO & VERACIDADE
1. **FATOS REAIS:** Busque fatos reais recentes em Indaiatuba (2025-2026) sobre "{ativo}".
   - Se não houver notícia "quente", transforme em **GUIA DE UTILIDADE PÚBLICA** (ex: "Como funciona X em Indaiatuba").
   - JAMAIS invente acidentes, crimes ou obras fictícias.
2. **TOM DE VOZ:** Comece informativo/jornalístico, termine consultivo.
3. **BIFURCAÇÃO DE CONVERSÃO:** Use a notícia para validar a qualidade de vida da cidade e atrair moradores.

---

## 1. A PAUTA
- **TEMA PRINCIPAL:** {ativo}
- **LOCAL:** {local_foco}
- **GATILHO:** {d['gatilho']} (Use para atrair a leitura).

## 2. ESTRUTURA DO TEXTO (HTML)
Use este estilo HTML:
{estilo_html}

**ROTEIRO OBRIGATÓRIO:**
1. **Manchete (H1):** Direta e informativa (Sem "clickbait" barato).
2. **Lide e Desenvolvimento:** Entregue a informação de valor (notícia ou guia). O que, onde, como.
3. **A PONTE (CRÍTICO):** Crie um parágrafo de transição que conecte o tema (infraestrutura, segurança, lazer, economia) com a vantagem de **MORAR** em Indaiatuba.
   - *Exemplo:* "Com investimentos contínuos em [tema da notícia], Indaiatuba se consolida como uma das melhores cidades para se viver..."
4. **CONCLUSÃO DE VENDA (CTA):**
   - **NÃO ENCERRE PEDINDO PARA COMPARTILHAR.**
   - Encerre oferecendo ajuda para encontrar imóveis na cidade.
   - Use o CTA Padrão: "Está pensando em se mudar para cá ou investir na cidade? A Imobiliária Saber tem as melhores opções..."

---

## 3. CHECKLIST DE ENTREGA
1. LOG BASTIDORES
2. BLOCKCODE HTML (Com JSON-LD)
   {script_json_ld}
   - **INCLUA O CTA FINAL DA IMOBILIÁRIA (Kit.com/Lead Capture)**
3. TÍTULO (H1 Jornalístico)
4. MARCADORES: {tags_otimizadas}
5. DATA: {data_fmt}
6. DESCRIÇÃO
7. IMAGEM PROMPT
""".strip()

    def _get_json_ld(self, d_pub, d_mod, author_name, headline):
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
""" % (headline, d_pub, d_mod, author_name)
