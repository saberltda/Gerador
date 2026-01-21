# src/builder.py
import datetime
import json
from .config import GenesisConfig

class PromptBuilder:
    """
    O 'Redator' (Versão Híbrida Definitiva).
    Combina:
    1. A inteligência de 'Esqueletos Editoriais' da V35 (Investidor, Família, etc).
    2. O CTA Focado em Captura de E-mail (Kit.com) solicitado.
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
    # ESQUELETOS EDITORIAIS (RECUPERADOS DA V35)
    # Garante que o texto tenha estrutura profissional e não genérica.
    # =========================================================================
    def _get_editorial_skeleton(self, cluster_key, ativo, bairro_nome):
        """Retorna a estrutura de H2 rígida para cada perfil de cliente."""
        
        # 1. INVESTIDOR / LOGÍSTICA
        if cluster_key in ("INVESTOR", "LOGISTICS"):
            return f"""
## 5. ESTRUTURA EDITORIAL OBRIGATÓRIA (MODO: {cluster_key})
Siga exatamente esta ordem de tópicos (H2):
0. (Título H1 oculto)
1. <h2>Contexto Histórico e Urbanístico de {bairro_nome}</h2>
2. <h2>A Verdade Sobre a Valorização na Zona</h2>
3. <h2>Infraestrutura e Mobilidade: O Que os Dados Revelam</h2>
4. <h2>O Detalhe Invisível Que Impacta Seu Investimento</h2>
5. <h2>Tabela de Distâncias Estratégicas</h2> (Use o CSS de Tabela Anti-Quebra).
6. <h2>Conclusão: O Veredito do Analista</h2>
"""
        # 2. FAMÍLIA / ALTO PADRÃO
        elif cluster_key in ("FAMILY", "HIGH_END"):
            return f"""
## 5. ESTRUTURA EDITORIAL OBRIGATÓRIA (MODO: {cluster_key})
Siga exatamente esta ordem de tópicos (H2):
1. <h2>A Atmosfera Exclusiva de {bairro_nome}</h2>
2. <h2>Logística Familiar & Escolas Próximas</h2>
3. <h2>Segurança e Vizinhança: O Que Esperar?</h2>
4. <h2>O "Segredo" do Bairro que Poucos Conhecem</h2>
5. <h2>Por que {ativo} é a Melhor Escolha Aqui?</h2>
"""
        # 3. VIDA URBANA
        elif cluster_key == "URBAN":
            return f"""
## 5. ESTRUTURA EDITORIAL OBRIGATÓRIA (MODO: URBAN)
Siga exatamente esta ordem de tópicos (H2):
1. <h2>A Regra dos 15 Minutos (Walkability)</h2>
2. <h2>Gastronomia e Lazer no Entorno</h2>
3. <h2>Conectividade Inteligente e Serviços</h2>
4. <h2>Raio-X: Este Bairro é Para Você?</h2>
"""
        # 4. DEFAULT
        return """
## 5. ESTRUTURA EDITORIAL GENÉRICA
1. <h2>Visão Geral da Localização</h2>
2. <h2>Pontos Fortes e Diferenciais</h2>
3. <h2>Análise de Custo-Benefício</h2>
4. <h2>Considerações Finais</h2>
"""

    def build(self, d, data_pub, data_mod, regras_texto_ajustada):
        if d.get('tipo_pauta') == "PORTAL":
            return self._build_portal_prompt(d, data_pub, data_mod, regras_texto_ajustada)
        else:
            return self._build_real_estate_prompt(d, data_pub, data_mod, regras_texto_ajustada)

    # =========================================================================
    # MODO 1: IMOBILIÁRIA (INTELLIGENCE + EMAIL CTA)
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
## GENESIS MAGNETO V.53 — EMAIL CONVERSION MODE
**Objetivo:** Texto SEO Imobiliário com Inteligência de Mercado e Captura de Leads.

### 🛡️ PROTOCOLO ANTI-CANIBALISMO
Você está PROIBIDO de repetir os temas abaixo. Escolha um ângulo novo:
{historico_txt}

---

## 1. O PRODUTO
- **ATIVO:** {ativo}
- **BAIRRO:** {bairro_nome}
- **OBS TÉCNICA/RISCO:** {d.get('obs_tecnica', 'N/A')}
- **PERSONA:** {d['persona']['nome']}

## 2. ESTRUTURA DO TEXTO (HTML)
Use este CSS inline (Tabelas blindadas contra quebra):
{estilo_html}

{self._get_editorial_skeleton(cluster_key, ativo, bairro_nome)}

## 6. CTA OBRIGATÓRIO (CAPTURA)
Ao final do artigo, insira **EXATAMENTE** este código para inscrição na lista de e-mail da "Imobiliária Saber".
NÃO convide para visitas, NÃO peça para chamar no WhatsApp. O único objetivo é o cadastro:
{self.CTA_CAPTURE_CODE}

## 7. REGRAS DE OURO (CONFIG)
{GenesisConfig.RULES['FORBIDDEN_WORDS']}
NUNCA use: "Sonho", "Oportunidade única".

## 8. CHECKLIST DE ENTREGA
1. LOG BASTIDORES
2. BLOCKCODE HTML (Com JSON-LD embutido: {self._get_json_ld(data_pub, data_mod, f"{ativo} em {bairro_nome}")} + Script de Email no final)
3. TÍTULO (H1)
4. MARCADORES: {self._generate_seo_tags(d)}
5. DATA: {data_fmt}
6. DESCRIÇÃO (Meta)
7. IMAGEM PROMPT (Realista)
""".strip()

    # =========================================================================
    # MODO 2: PORTAL (MANTER PADRÃO)
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
## GENESIS MAGNETO V.53 — JOURNALIST MODE
**Objetivo:** Notícia de Utilidade Pública que gera Autoridade.

## 1. A PAUTA
- **TEMA:** {ativo}
- **LOCAL:** {d['bairro']['nome'] if d['bairro'] else 'Indaiatuba'}
- **GATILHO:** {d['gatilho']}

## 2. ESTRUTURA
Use este CSS:
{estilo_html}

**ROTEIRO:**
1. Manchete (H1)
2. Fatos Recentes (O que, onde, quando)
3. A Ponte (Conecte a notícia com a qualidade de vida/imóveis)
4. Conclusão

## 3. CTA OBRIGATÓRIO
Finalize com o convite para a newsletter:
{self.CTA_CAPTURE_CODE}

## 4. CHECKLIST
1. HTML + JSON-LD
2. TÍTULO
3. DATA: {data_fmt}
4. IMAGEM PROMPT
""".strip()

