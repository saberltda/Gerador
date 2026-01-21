# src/builder.py
import datetime
import json
from .config import GenesisConfig

class PromptBuilder:
    """
    O 'Redator'.
    Responsável por montar a string final do Prompt que será enviada para a IA.
    Ele injeta o JSON-LD, o CSS inline e garante que as regras do arquivo TXT
    estejam visíveis para o modelo.
    """

    # Código HTML fixo para captura de leads (Newsletter)
    CTA_CAPTURE_CODE = """
<div style="background: #f0f7ff; border: 2px solid #003366; padding: 25px; border-radius: 10px; margin-top: 40px; text-align: center;">
    <h3 style="color: #003366; margin-top: 0;">📩 Não perca oportunidades como esta!</h3>
    <p style="font-size: 18px;">Receba nossa curadoria exclusiva de imóveis e notícias de Indaiatuba diretamente no seu e-mail.</p>
    <a href="https://conteudo.saber.imb.br/newsletter" target="_blank" style="background-color: #003366; color: white; padding: 15px 30px; text-decoration: none; font-weight: bold; border-radius: 5px; font-size: 18px; display: inline-block; margin-top: 10px;">👉 QUERO ME INSCREVER AGORA</a>
</div>
"""

    def __init__(self):
        pass

    def _format_date_blogger(self, iso_date_str):
        """Converte AAAA-MM-DD para 'DD de mmm. de AAAA' (Estilo Blogger)"""
        try:
            if isinstance(iso_date_str, datetime.datetime):
                dt = iso_date_str
            else:
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
        
        # Adiciona o Bairro
        if d.get('bairro') and isinstance(d['bairro'], dict):
            tags.append(d['bairro']['nome'])
            
        # Adiciona o Cluster Técnico (ex: Alto Padrão, Investimento)
        if d.get('cluster_tecnico'):
            tags.append(d['cluster_tecnico'])
            
        # Adiciona tags específicas do tópico
        if d.get('topico'):
             # Simplificação: pega palavras chaves do tópico
             clean_topic = d['topico'].split(' ')[1] if len(d['topico'].split(' ')) > 1 else d['topico']
             tags.append(clean_topic.replace("&", "e"))

        return ", ".join(tags)

    def _get_json_ld(self, data_pub, data_mod, author_name, headline):
        """Gera o bloco JSON-LD para SEO técnico."""
        # Garante formato ISO para o JSON
        iso_pub = data_pub if isinstance(data_pub, str) else data_pub.isoformat()
        iso_mod = data_mod if isinstance(data_mod, str) else data_mod.isoformat()

        json_ld = {
            "@context": "https://schema.org",
            "@type": "NewsArticle",
            "headline": headline,
            "image": [
                "https://blog.saber.imb.br/assets/images/default_cover.jpg" 
            ],
            "datePublished": iso_pub,
            "dateModified": iso_mod,
            "author": [{
                "@type": "Organization",
                "name": author_name,
                "url": GenesisConfig.BLOG_URL
            }]
        }
        return f'<script type="application/ld+json">{json.dumps(json_ld)}</script>'

    def get_format_instructions(self, formato_key):
        """Retorna instruções específicas para cada formato de texto."""
        instrucoes = {
            "LISTA": "Crie um artigo em formato de LISTA (ex: '5 Motivos para...', 'Top 3 Bairros...'). Use <h3> para cada item.",
            "GUIA": "Crie um GUIA COMPLETO e aprofundado. Explique detalhes, prós e contras. Use tom educativo.",
            "COMPARATIVO": "Faça um COMPARATIVO (ex: Casa x Apartamento, Bairro A x Bairro B). Use tabelas se possível (em HTML).",
            "REVIEW": "Faça um REVIEW (Análise) detalhada do bairro ou condomínio como se fosse um especialista avaliando.",
            "NOTÍCIA": "Escreva como uma NOTÍCIA urgente ou novidade de mercado. Tom mais jornalístico e factual.",
            "STORYTELLING": "Use STORYTELLING. Conte a história de uma família ou persona que se mudou para lá."
        }
        return instrucoes.get(formato_key, "Escreva um artigo de blog imobiliário de alta qualidade.")

    # =========================================================================
    # 🏭 MÉTODO PRINCIPAL (ROUTER)
    # =========================================================================
    def build(self, d, data_pub, data_mod, regras_texto_ajustada):
        """
        Direciona para o construtor correto baseando-se no modo de operação.
        """
        # Se o gatilho for muito "jornalístico", usamos o modo Portal
        # Ou se explicitamente definido no futuro. Por enquanto, baseamos no formato.
        if d.get('formato') == "NOTÍCIA" or "Portal" in str(d.get('gatilho', '')):
            return self._build_portal_prompt(d, data_pub, data_mod, regras_texto_ajustada)
        else:
            # Padrão: Modo Imobiliária (Foco em Venda/Lead)
            return self._build_real_estate_prompt(d, data_pub, data_mod, regras_texto_ajustada)

    # =========================================================================
    # 🏘️ MODO 1: IMOBILIÁRIA (Foco em Venda / SEO Imobiliário)
    # =========================================================================
    def _build_real_estate_prompt(self, d, data_pub, data_mod, regras_texto_ajustada):
        data_fmt = self._format_date_blogger(data_pub)
        ativo = d['ativo_definido']
        contexto_geo = f"Indaiatuba, SP - {d['bairro']['nome']}" if d['bairro'] else "Indaiatuba, SP"
        zoning_info = d['bairro']['zona_normalizada'] if d['bairro'] else "Geral"
        
        tags_otimizadas = self._generate_seo_tags(d)
        script_json_ld = self._get_json_ld(data_pub, data_mod, "Saber Imobiliária", f"{ativo} em {contexto_geo}")
        
        anti_hallucination_txt = "\n".join([f"- {rule}" for rule in GenesisConfig.STRICT_GUIDELINES])
        ancora_instruction = f"O texto deve levar sutilmente para a venda de: {ativo}"

        estilo_html = f"""<style>
.post-body h2 {{ color: #003366; border-bottom: 2px solid #eee; padding-bottom: 10px; margin-top: 30px; }}
.post-body h3 {{ color: #cc0000; margin-top: 20px; }}
.post-body p {{ font-size: 18px; line-height: 1.6; color: #444; }}
.post-body ul {{ margin-bottom: 20px; }}
.post-body li {{ margin-bottom: 10px; }}
</style>"""

        # Prepara o bloco de regras lido do arquivo
        bloco_regras = f"""
# ==========================================
# 🔐 ZONA DE SEGURANÇA MÁXIMA (REGRAS.txt)
# ==========================================
{regras_texto_ajustada}
"""

        return f"""
## GENESIS MAGNETO V.9.2 — REAL ESTATE SALES MODE
**Objetivo:** Gerar texto final pronto para Blogger (HTML Fragment) focado em SEO e Conversão.

### 🛡️ PROTOCOLO DE VERACIDADE
{anti_hallucination_txt}

---

## 1. O PRODUTO E CONTEXTO
- **ATIVO:** {ativo}
- **LOCAL:** {contexto_geo}
- **ZONEAMENTO:** {zoning_info}
- **TEMA:** {d['topico']}
- **FORMATO:** {self.get_format_instructions(d['formato'])}
{ancora_instruction}

## 2. ESTRUTURA DO TEXTO (HTML)
Use este estilo CSS inline:
{estilo_html}

APLIQUE ESTRITAMENTE AS REGRAS DA CONSTITUIÇÃO:
{bloco_regras}

**ROTEIRO SUGERIDO:**
1. **Título (H1):** Persuasivo com SEO.
2. **Introdução:** Gancho emocional ({d['gatilho']}).
3. **Desenvolvimento:** Detalhes do imóvel/bairro e benefícios.
4. **CTA (Chamada para Ação):** Convide para visitar.

---

## 3. CHECKLIST DE ENTREGA (OBRIGATÓRIO)
1. LOG BASTIDORES (Breve análise do que foi feito).
2. BLOCKCODE HTML (Código Puro) contendo:
   - O Script JSON-LD: {script_json_ld}
   - O Conteúdo do Post (h2, h3, p, ul...).
   - **OBRIGATÓRIO: Ao final, insira EXATAMENTE este código de captura:**
     {self.CTA_CAPTURE_CODE}
3. TÍTULO (H1)
4. MARCADORES (Tags): {tags_otimizadas}
5. DATA: {data_fmt}
6. DESCRIÇÃO (Meta Description)
7. IMAGEM PROMPT (Sugestão para gerar imagem)
""".strip()

    # =========================================================================
    # 🧠 MODO 2: PORTAL DA CIDADE (Foco em Notícia -> Conversão)
    # =========================================================================
    def _build_portal_prompt(self, d, data_pub, data_mod, regras_texto_ajustada):
        data_fmt = self._format_date_blogger(data_pub)
        ativo = d['ativo_definido']
        tags_otimizadas = self._generate_seo_tags(d)
        
        # Cálculo dinâmico do ano
        ano_atual = datetime.datetime.now().year
        range_anos = f"({ano_atual-1}-{ano_atual})"

        estilo_html = f"""<style>
.post-body h2 {{ color: #2c3e50; font-family: 'Georgia', serif; border-bottom: 2px solid #eee; padding-bottom: 10px; }}
.post-body h3 {{ color: {GenesisConfig.COLOR_PRIMARY}; font-family: 'Segoe UI', Arial, sans-serif; margin-top: 25px; }}
.post-body p {{ font-size: 19px; line-height: 1.6; color: #333; }}
.post-body .destaque {{ background: #f9f9f9; padding: 15px; border-left: 4px solid {GenesisConfig.COLOR_PRIMARY}; font-style: italic; margin: 20px 0; }}
</style>"""

        script_json_ld = self._get_json_ld(data_pub, data_mod, "Imobiliária Saber", d['ativo_definido'])
        
        local_foco = d['bairro']['nome'] if (d['modo'] == "BAIRRO" and d['bairro']) else "Indaiatuba (Cidade toda)"
        
        # Prepara o bloco de regras lido do arquivo (CORREÇÃO APLICADA AQUI)
        bloco_regras = f"""
# ==========================================
# 🔐 ZONA DE SEGURANÇA MÁXIMA (REGRAS.txt)
# ==========================================
{regras_texto_ajustada}
"""

        return f"""
## GENESIS MAGNETO V.9.2 — JOURNALIST TO SALES MODE
**Objetivo:** Texto Jornalístico que converte em LEAD Imobiliário.

### 🚨 PROTOCOLO DE JORNALISMO
1. **FATOS REAIS:** Busque fatos reais recentes {range_anos} sobre "{ativo}". Se não houver, faça um GUIA DE UTILIDADE PÚBLICA.
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

APLIQUE AS REGRAS DA CONSTITUIÇÃO:
{bloco_regras}

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
