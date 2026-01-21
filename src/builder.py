# src/builder.py
import datetime
import re
from .config import GenesisConfig

class PromptBuilder:
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
        
        # Tags dinâmicas baseadas no modo
        if d['tipo_pauta'] == "PORTAL":
            tags.append("Notícias Indaiatuba")
            tags.append("Utilidade Pública")
            tags.append("Portal da Cidade")
        else:
            tags.append("Imóveis Indaiatuba")
            tags.append("Mercado Imobiliário")
            cluster_map = {
                "HIGH_END": ["Altíssimo Padrão", "Luxo"],
                "FAMILY": ["Casas em Condomínio", "Família"],
                "URBAN": ["Apartamentos", "Centro"],
                "INVESTOR": ["Investimento", "Oportunidade"],
                "LOGISTICS": ["Industrial", "Galpões"],
            }
            tags.extend(cluster_map.get(d['cluster_tecnico'], []))

        if d['modo'] == "BAIRRO" and d['bairro']:
            tags.append(d['bairro']['nome'])
            tags.append(f"Viver no {d['bairro']['nome']}")

        # Limpa o ativo para tag
        ativo_clean = d['ativo_definido'].split("(")[0].strip()
        tags.append(ativo_clean)

        seen = set()
        final_tags = []
        for t in tags:
            t_c = t.replace("/", "").strip()
            if t_c and t_c not in seen:
                seen.add(t_c)
                final_tags.append(t_c)
        return ", ".join(final_tags[:12])

    def get_format_instructions(self, formato):
        structures = {
            "GUIA_DEFINITIVO": "Guia organizado em seções técnicas, com passos lógicos.",
            "LISTA_POLEMICA": "Lista numerada que confronte mitos comuns.",
            "COMPARATIVO_TECNICO": "Comparação objetiva (tabela/lista) Prós vs Contras.",
            "DATA_DRIVEN": "Texto orientado a fatos, datas e números reais.",
        }
        return structures.get(formato, "Estrutura clara, objetiva e informativa.")

    def build(self, d, data_pub, data_mod, regras_texto_ajustada: str):
        """
        O GRANDE MONTADOR.
        Decide qual 'Cérebro' usar: Corretor ou Jornalista.
        """
        if d['tipo_pauta'] == "PORTAL":
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
        
        # ... (Mantém a lógica de JSON-LD e CSS igual) ...
        estilo_html = f"""<style>
.post-body h2 {{ color: {GenesisConfig.COLOR_PRIMARY}; font-family: 'Segoe UI', Arial, sans-serif; }}
.post-body h3 {{ color: {GenesisConfig.COLOR_PRIMARY}; font-family: 'Segoe UI', Arial, sans-serif; }}
.post-body p {{ font-size: 19px; line-height: 1.6; }}
</style>"""

        script_json_ld = self._get_json_ld(data_pub, data_mod, "Imobiliária Saber", d['ativo_definido'])

        if d['modo'] == "BAIRRO" and d['bairro']:
            contexto_geo = f"Bairro Específico: {d['bairro']['nome']}"
            zoning_info = f"Zoneamento: {d['bairro']['zona']}"
        else:
            contexto_geo = "Cidade: Indaiatuba (Panorama Geral)"
            zoning_info = "Macro-zoneamento urbano."

        anti_hallucination_txt = "\n".join([f"- {rule}" for rule in GenesisConfig.STRICT_GUIDELINES])

        return f"""
## GENESIS MAGNETO V.7.0 — IMOBILIÁRIA MODE
**Objetivo:** Texto de Conversão Imobiliária (HTML Fragment).

### 🛡️ PROTOCOLO DE VERACIDADE
{anti_hallucination_txt}

---

## ⛔ TRAVA ANTI-ANÚNCIO
1. **VOCÊ NÃO ESTÁ VENDENDO UMA UNIDADE ESPECÍFICA.**
2. **VENDA O CONCEITO.** Fale sobre o Padrão Construtivo da região.
3. **Foco na Curadoria:** Aja como um consultor, não um classificado.

---

## 1. O CLIENTE
**PERFIL:** {p['nome']}
- **Dor:** {p['dor']}
- **Desejo:** {p['desejo']}
- **Gatilho:** {d['gatilho']}

## 2. O PRODUTO
- **TIPOLOGIA:** {ativo}
- **LOCAL:** {contexto_geo}
- **ZONEAMENTO:** {zoning_info}
- **TEMA:** {d['topico']}
- **FORMATO:** {self.get_format_instructions(d['formato'])}

---

## 3. REGRAS E ESTRUTURA
Estilo HTML Mínimo:
{estilo_html}

REGRAS:
{regras_texto_ajustada}

**ESTRUTURA SUGERIDA:**
1. **Introdução:** Conecte a dor ({p['dor']}) ao cenário de {contexto_geo}.
2. **Diagnóstico:** Por que esse bairro/região resolve o problema?
3. **Tipologia:** Fale sobre "{ativo}" como solução de estilo de vida.
4. **Conclusão:** Convite para curadoria personalizada.

---

## 4. CHECKLIST DE ENTREGA
1. LOG BASTIDORES
2. BLOCKCODE HTML (Com JSON-LD)
   {script_json_ld}
   - Inclua CTA Kit.com
3. TÍTULO (H1 Persuasivo)
4. MARCADORES: {tags_otimizadas}
5. DATA: {data_fmt}
6. DESCRIÇÃO
7. IMAGEM PROMPT
""".strip()

    # =========================================================================
    # 🧠 MODO 2: PORTAL DA CIDADE (Foco em Notícia, Utilidade, Fatos)
    # =========================================================================
    def _build_portal_prompt(self, d, data_pub, data_mod, regras_texto_ajustada):
        data_fmt = self._format_date_blogger(data_pub)
        ativo = d['ativo_definido'] # Ex: "Notícia de Trânsito"
        tags_otimizadas = self._generate_seo_tags(d)
        
        estilo_html = f"""<style>
.post-body h2 {{ color: #2c3e50; font-family: 'Georgia', serif; border-bottom: 2px solid #eee; padding-bottom: 10px; }}
.post-body h3 {{ color: {GenesisConfig.COLOR_PRIMARY}; font-family: 'Segoe UI', Arial, sans-serif; margin-top: 25px; }}
.post-body p {{ font-size: 19px; line-height: 1.6; color: #333; }}
.post-body .destaque {{ background: #f9f9f9; padding: 15px; border-left: 4px solid {GenesisConfig.COLOR_PRIMARY}; font-style: italic; }}
</style>"""

        script_json_ld = self._get_json_ld(data_pub, data_mod, "Portal Saber Indaiatuba", d['ativo_definido'])

        local_foco = d['bairro']['nome'] if (d['modo'] == "BAIRRO" and d['bairro']) else "Indaiatuba (Cidade toda)"

        return f"""
## GENESIS MAGNETO V.7.0 — JOURNALIST MODE (PORTAL)
**Objetivo:** Texto Jornalístico ou Utilidade Pública (HTML Fragment).

### 🚨 PROTOCOLO DE JORNALISMO (CRÍTICO)
1. **FATOS REAIS:** Se o tema for notícia (ex: Trânsito, Obras), você DEVE buscar fatos reais recentes em Indaiatuba.
   - **AÇÃO OBRIGATÓRIA:** Faça uma busca mental por eventos REAIS recentes sobre "{ativo}" em Indaiatuba (2025-2026).
   - **SE NÃO HOUVER NOTÍCIA RECENTE:** Transforme o texto em um **GUIA DE UTILIDADE PÚBLICA** atemporal (ex: "Como evitar trânsito", "Telefones úteis", "Direitos do cidadão").
2. **NÃO INVENTE EVENTOS:** Jamais invente um acidente ou uma obra que não existe. Se não achar, escreva sobre *prevenção* ou *orientação*.
3. **TOM DE VOZ:** Imparcial, informativo, prestação de serviço. Sem "adjetivos de vendedor" (lindo, maravilhoso).
4. **USE O BAIRRO:** Se foi selecionado "{local_foco}", cite ele como contexto, mas apenas se fizer sentido factual.

---

## 1. A PAUTA
- **TEMA PRINCIPAL:** {ativo}
- **LOCAL DE COBERTURA:** {local_foco}
- **PÚBLICO ALVO:** Cidadãos de Indaiatuba (Foco em utilidade, não venda).
- **GATILHO:** {d['gatilho']} (Use apenas para atrair leitura, não venda).

## 2. ESTRUTURA JORNALÍSTICA
Use este estilo HTML:
{estilo_html}

**ROTEIRO:**
1. **Manchete (H1):** Direta e informativa. (Ex: "Cronograma de Coleta de Lixo...", "Novas regras para...")
2. **Lide (1º parágrafo):** O que, onde, quando e por que. Responda a dúvida do cidadão imediatamente.
3. **Desenvolvimento:** Detalhes técnicos, horários, endereços, telefones úteis.
   - Use a classe CSS: <div class="destaque">Dica importante ou Resumo</div>
4. **Serviço:** Links úteis, telefones da prefeitura/órgãos competentes.
5. **Conclusão:** Convite para compartilhar a informação.

---

## 3. CHECKLIST DE ENTREGA
1. LOG BASTIDORES (Explique se achou notícia real ou se fez guia atemporal)
2. BLOCKCODE HTML (Com JSON-LD)
   {script_json_ld}
3. TÍTULO (H1 Jornalístico)
4. MARCADORES: {tags_otimizadas}
5. DATA: {data_fmt}
6. DESCRIÇÃO (Resumo da notícia)
7. IMAGEM PROMPT (Fotojornalismo ou Ilustrativa neutra)
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
