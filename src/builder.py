# src/builder.py
import datetime
import json
from .config import GenesisConfig

class PromptBuilder:
    """
    O 'Redator' (Versão Criativa & Estratégica).
    Principais características:
    1. Estrutura Editorial Sugerida (A IA deve criar títulos próprios).
    2. CTA Focado em Captura de E-mail (Kit.com).
    3. Injeção obrigatória do conteúdo de REGRAS.TXT.
    """

    # --- CTA OBRIGATÓRIO (CAPTURA DE E-MAIL) ---
    CTA_CAPTURE_CODE = """
<div style="text-align:center; margin: 40px 0;">
<script async data-uid="d188d73e78" src="https://sabernovidades.kit.com/d188d73e78/index.js"></script>
</div>
"""

    def __init__(self):
        pass

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
        return ", ".join(tags[:8])

    def _get_json_ld(self, data_pub, data_mod, headline):
        iso_pub = data_pub if isinstance(data_pub, str) else data_pub.isoformat()
        json_ld = {
            "@context": "https://schema.org", "@type": "BlogPosting",
            "headline": headline,
            "datePublished": iso_pub,
            "author": {"@type": "Organization", "name": "Imobiliária Saber"},
            "publisher": {"@type": "Organization", "name": "Imobiliária Saber", "logo": {"@type": "ImageObject", "url": "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhtRYbYvSxR-IRaFMCb95rCMmr1pKSkJKSVGD2SfW1h7e7M-NbCly3qk9xKK5lYpfOPYfq-xkzJ51p14cGftPHLF7MrbM0Szz62qQ-Ff5H79-dMiUcNzhrEL7LXKf089Ka2yzGaIX-UJBgTtdalNaWYPS0JSSfIMYNIE4yxhisKcU8j-gtOqXq6lSmgiSA/s600/1000324271.png"}}
        }
        return f'<script type="application/ld+json">{json.dumps(json_ld, ensure_ascii=False)}</script>'

    # =========================================================================
    # SUGESTÕES EDITORIAIS (A IA DEVE CRIAR OS TÍTULOS)
    # =========================================================================
    def _get_editorial_suggestions(self, cluster_key, ativo, bairro_nome):
        """
        Retorna um GUIA DE TÓPICOS. A IA é instruída a criar títulos originais
        baseados nestes temas, nunca copiar os nomes genéricos.
        """
        
        # 1. INVESTIDOR / LOGÍSTICA
        if cluster_key in ("INVESTOR", "LOGISTICS"):
            return f"""
## 5. GUIA ESTRUTURAL (SUGESTÃO TEMÁTICA - CRIE SEUS TÍTULOS)
Siga esta lógica de raciocínio, mas **INVENTE TÍTULOS H2 ORIGINAIS** para cada seção:

1. **Tema do H2:** Contexto da Região (Fale sobre a história ou localização estratégica de {bairro_nome}).
   *Exemplo do que NÃO fazer:* "Contexto Histórico".
   *O que fazer:* "A Evolução Logística da Zona Norte", "Por que {bairro_nome} atrai Capital".

2. **Tema do H2:** Dados de Valorização (Fale sobre números, demanda e oferta).
   *Crie um título agressivo sobre lucro/retorno.*

3. **Tema do H2:** Infraestrutura Técnica (Fale sobre energia, estradas ou topografia).
   *Crie um título técnico que passe autoridade.*

4. **Tema do H2:** O "Pulo do Gato" (Um detalhe que só especialista sabe).
   *Crie um título que gere curiosidade.*

5. **Tema do H2:** Distâncias (Use a Tabela Obrigatória aqui).
   *Título sugerido:* "Raio-X Logístico: Distâncias Reais".

6. **Tema do H2:** Conclusão Financeira.
"""
        # 2. FAMÍLIA / ALTO PADRÃO
        elif cluster_key in ("FAMILY", "HIGH_END"):
            return f"""
## 5. GUIA ESTRUTURAL (SUGESTÃO TEMÁTICA - CRIE SEUS TÍTULOS)
Siga esta lógica de raciocínio, mas **INVENTE TÍTULOS H2 ORIGINAIS** para cada seção:

1. **Tema do H2:** Atmosfera e "Vibe" (Descreva a sensação de morar em {bairro_nome}).
   *Exemplo do que NÃO fazer:* "Atmosfera Exclusiva".
   *O que fazer:* "O Silêncio que Você Procura no {bairro_nome}", "Como é Acordar no Paraíso".

2. **Tema do H2:** Vida em Família e Escolas (Fale sobre logística escolar e clubes).
   *Crie um título emocional sobre o futuro dos filhos.*

3. **Tema do H2:** Segurança Real (Fale sobre portaria, rondas ou tranquilidade da rua).
   *Crie um título que passe paz de espírito.*

4. **Tema do H2:** O Segredo Local (Algo que só moradores conhecem).
   *Crie um título de "Insider".*

5. **Tema do H2:** Por que este imóvel específico ({ativo}) funciona aqui?
   *Título focado na tipologia.*
"""
        # 3. VIDA URBANA
        elif cluster_key == "URBAN":
            return f"""
## 5. GUIA ESTRUTURAL (SUGESTÃO TEMÁTICA - CRIE SEUS TÍTULOS)
Siga esta lógica de raciocínio, mas **INVENTE TÍTULOS H2 ORIGINAIS** para cada seção:

1. **Tema do H2:** Walkability (Fazer tudo a pé).
   *Exemplo do que NÃO fazer:* "A Regra dos 15 Minutos".
   *O que fazer:* "Esqueça o Carro: A Vida a Pé no {bairro_nome}".

2. **Tema do H2:** Gastronomia e Nightlife (O que fazer à noite/fim de semana).
   *Crie um título vibrante sobre lazer.*

3. **Tema do H2:** Conectividade e Serviços (Internet, Ifood, Uber, Farmácias).
   *Crie um título sobre conveniência moderna.*

4. **Tema do H2:** Perfil do Morador (Para quem é esse bairro?).
"""
        # 4. DEFAULT
        return """
## 5. GUIA ESTRUTURAL (SUGESTÃO)
Crie 4 Títulos H2 originais cobrindo:
1. Localização e Acessos.
2. Os Diferenciais Competitivos.
3. Custo-Benefício Atual.
4. Veredito Final.
"""

    def build(self, d, data_pub, data_mod, regras_texto_ajustada):
        if d.get('tipo_pauta') == "PORTAL":
            return self._build_portal_prompt(d, data_pub, data_mod, regras_texto_ajustada)
        else:
            return self._build_real_estate_prompt(d, data_pub, data_mod, regras_texto_ajustada)

    # =========================================================================
    # MODO 1: IMOBILIÁRIA (CRIATIVIDADE + EMAIL CTA + REGRAS.TXT)
    # =========================================================================
    def _build_real_estate_prompt(self, d, data_pub, data_mod, regras_texto_ajustada):
        data_fmt = self._format_date_blogger(data_pub)
        ativo = d['ativo_definido']
        bairro_nome = d['bairro']['nome'] if d['bairro'] else "Indaiatuba"
        cluster_key = d.get('cluster_tecnico', 'FAMILY')
        
        # Histórico para Anti-Canibalismo
        historico_txt = "\n".join([f"- {t}" for t in d.get('historico_titulos', [])])

        estilo_html = f"""<style>
.post-body h2 {{ color: {GenesisConfig.COLOR_PRIMARY}; border-bottom: 2px solid #eee; padding-bottom: 10px; margin-top: 30px; }}
.post-body h3 {{ color: #cc0000; margin-top: 20px; }}
.post-body p {{ font-size: 19px; line-height: 1.6; color: #333; }}
.post-body table {{ width: 100%; min-width: 600px; border-collapse: collapse; }}
.post-body th, .post-body td {{ padding: 12px; border: 1px solid #ccc; word-break: keep-all; hyphens: none; }}
</style>"""

        return f"""
## GENESIS MAGNETO V.54 — CREATIVE MODE
**Objetivo:** Texto SEO Imobiliário com Títulos Únicos e Captura de Leads.

### 🛡️ PROTOCOLO ANTI-CANIBALISMO
Você está PROIBIDO de repetir os ângulos abordados nestes artigos passados:
{historico_txt}

---

## 1. O PRODUTO
- **ATIVO:** {ativo}
- **BAIRRO:** {bairro_nome}
- **OBS TÉCNICA/RISCO:** {d.get('obs_tecnica', 'N/A')}
- **PERSONA:** {d['persona']['nome']}

## 2. CONFIGURAÇÃO VISUAL (CSS)
Use este CSS inline (Tabelas blindadas contra quebra):
{estilo_html}

## 3. MANUAL DE ESTILO (REGRAS.TXT)
AS SEGUINTES REGRAS TÊM PRECEDÊNCIA TOTAL. SIGA CADA INSTRUÇÃO ABAIXO:
---------------------------------------------------
{regras_texto_ajustada}
---------------------------------------------------

{self._get_editorial_suggestions(cluster_key, ativo, bairro_nome)}

### 🚫 PROIBIÇÕES DE ESTRUTURA
1. **JAMAIS** use os títulos genéricos (ex: "Contexto Histórico", "Atmosfera Exclusiva") como seus H2. Eles são apenas guias do tema. Crie títulos atraentes.
2. **JAMAIS** esqueça da Tabela de Distâncias no caso de Investidores/Logística.

## 6. CTA OBRIGATÓRIO (CAPTURA)
Ao final do artigo, insira **EXATAMENTE** este código para inscrição na lista VIP.
NÃO convide para visitas, NÃO peça para chamar no WhatsApp. O único objetivo é o cadastro:
{self.CTA_CAPTURE_CODE}

## 7. REGRAS GERAIS
{GenesisConfig.RULES['FORBIDDEN_WORDS']}
NUNCA use: "Sonho", "Oportunidade única".

## 8. CHECKLIST DE ENTREGA
1. LOG BASTIDORES
2. BLOCKCODE HTML (Com JSON-LD embutido: {self._get_json_ld(data_pub, data_mod, f"{ativo} em {bairro_nome}")} + Script de Email no final)
3. TÍTULO (H1) CRIATIVO
4. MARCADORES: {self._generate_seo_tags(d)}
5. DATA: {data_fmt}
6. DESCRIÇÃO (Meta)
7. IMAGEM PROMPT (Realista)
""".strip()

    # =========================================================================
    # MODO 2: PORTAL (MANTIDO COM REGRAS.TXT)
    # =========================================================================
    def _build_portal_prompt(self, d, data_pub, data_mod, regras_texto_ajustada):
        data_fmt = self._format_date_blogger(data_pub)
        ativo = d['ativo_definido']
        estilo_html = f"""<style>
.post-body h2 {{ color: #2c3e50; font-family: 'Georgia', serif; border-bottom: 2px solid #eee; padding-bottom: 10px; }}
.post-body h3 {{ color: {GenesisConfig.COLOR_PRIMARY}; font-family: 'Segoe UI', Arial, sans-serif; margin-top: 25px; }}
.post-body p {{ font-size: 19px; line-height: 1.6; color: #333; }}
.post-body .destaque {{ background: #f9f9f9; padding: 15px; border-left: 4px solid {GenesisConfig.COLOR_PRIMARY}; font-style: italic; margin: 20px 0; }}
</style>"""

        return f"""
## GENESIS MAGNETO V.54 — JOURNALIST MODE
**Objetivo:** Notícia de Utilidade Pública que gera Autoridade.

## 1. A PAUTA
- **TEMA:** {ativo}
- **LOCAL:** {d['bairro']['nome'] if d['bairro'] else 'Indaiatuba'}
- **GATILHO:** {d['gatilho']}

## 2. ESTRUTURA SUGERIDA
Crie títulos jornalísticos para as seções (Não use "Introdução" ou "Conclusão").
Siga o roteiro lógico: Fato -> Contexto -> Impacto na Vida/Imóveis -> Fechamento.

Use este CSS:
{estilo_html}

## 3. CTA OBRIGATÓRIO
Finalize com o convite para a newsletter:
{self.CTA_CAPTURE_CODE}

## 4. DIRETRIZES DE ESTILO (REGRAS.TXT)
{regras_texto_ajustada}

## 5. CHECKLIST
1. HTML + JSON-LD
2. TÍTULO (Manchete)
3. DATA: {data_fmt}
4. IMAGEM PROMPT
""".strip()
