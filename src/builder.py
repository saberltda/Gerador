# src/builder.py
import datetime
import json
from .config import GenesisConfig

class PromptBuilder:
    """
    O 'Redator' (Versão 55 - Structure Aware).
    Agora sincroniza perfeitamente o FORMATO escolhido com a ESTRUTURA do texto.
    """

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
        # Adiciona o formato e ângulo como tags para reforçar o SEO semântico
        if d.get('formato'): tags.append(d['formato'])
        return ", ".join(tags[:10])

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
    # MOTOR DE ESTRUTURA (NOVO) - DITADOR DE FORMATO
    # =========================================================================
    def _get_structural_guidelines(self, formato_key, cluster_key, bairro_nome):
        """
        Define a 'Ousadia Estrutural' do texto baseada na escolha do usuário.
        Substitui as sugestões genéricas por ordens de formatação.
        """
        
        # 1. LISTA POLÊMICA (Quebra de Padrão)
        if formato_key == "LISTA_POLEMICA":
            return f"""
## 5. ESTRUTURA OBRIGATÓRIA: LISTA POLÊMICA (MITOS & VERDADES)
**Você NÃO está escrevendo um artigo comum.** Você está escrevendo uma LISTA NUMERADA.
Sua missão é derrubar mitos sobre {bairro_nome}.

Estrutura dos H2 (Use exatamente esta formatação):
- **H2: Mito #1:** [Mito Comum sobre o bairro/imóvel]
- **H2: Mito #2:** [Outro Mito]
- **H2: Mito #3:** [Mito Financeiro ou de Segurança]
- **H2: Mito #4:** [Mito sobre Distância/Trânsito]
- **H2: A Verdade Final:** (Conclusão baseada em dados).

*Tom de Voz:* Provocativo, direto e "Contra-Intuitivo". Comece os parágrafos com "Dizem por aí que..., mas a matemática prova o contrário."
"""

        # 2. COMPARATIVO TÉCNICO (Batalha)
        elif formato_key == "COMPARATIVO_TECNICO":
            return f"""
## 5. ESTRUTURA OBRIGATÓRIA: BATALHA COMPARATIVA (VS)
O cliente está em dúvida entre {bairro_nome} e "Outras Opções". Ajude-o a decidir.

Estrutura dos H2:
- **H2: Round 1: Localização e Acessos** (Compare tempos reais).
- **H2: Round 2: Custo-Benefício do m²** (Matemática Pura).
- **H2: Round 3: Perfil de Vizinho** (Quem mora lá?).
- **H2: Veredito: Quem vence?**

**OBRIGATÓRIO:** Insira uma TABELA HTML no meio do texto comparando:
| Critério | {bairro_nome} | Outros Bairros |
|----------|---------------|----------------|
| Segurança| ... | ... |
| Lazer | ... | ... |
"""

        # 3. GUIA DEFINITIVO (Autoridade)
        elif formato_key == "GUIA_DEFINITIVO":
            return f"""
## 5. ESTRUTURA OBRIGATÓRIA: MANUAL COMPLETO (DE A a Z)
O leitor quer um mapa do tesouro. Não pule detalhes.

Estrutura dos H2:
- **H2: Capítulo 1: O Raio-X da Localização** (Mapa mental).
- **H2: Capítulo 2: Infraestrutura e Serviços** (Escolas, Mercados).
- **H2: Capítulo 3: O Perfil do Imóvel Ideal** (O que comprar aqui?).
- **H2: Capítulo 4: Potencial de Valorização** (Visão de Futuro).
- **H2: Checklist Final para Compradores**.

*Tom de Voz:* Enciclopédico, Seguro e "Professor".
"""

        # 4. INSIGHT DE CORRETOR (Bastidores)
        elif formato_key == "INSIGHT_DE_CORRETOR":
            return f"""
## 5. ESTRUTURA OBRIGATÓRIA: CONFISSÕES DE BASTIDORES
Escreva em PRIMEIRA PESSOA (Nós da Saber). Conte o que ninguém conta.

Estrutura dos H2:
- **H2: O que eu vi na visita técnica de ontem**.
- **H2: O detalhe que passa despercebido na escritura**.
- **H2: Uma história real de um cliente (Anônimo)**.
- **H2: Minha opinião sincera: Para quem NÃO é este bairro**.

*Tom de Voz:* Conversa de café, segredo, exclusividade.
"""

        # 5. PERGUNTAS E RESPOSTAS (FAQ)
        elif formato_key == "PERGUNTAS_RESPOSTAS":
            return f"""
## 5. ESTRUTURA OBRIGATÓRIA: FAQ (TIRE SUAS DÚVIDAS)
O texto deve ser puramente perguntas e respostas diretas.

Estrutura dos H2:
- **H2: "É verdade que {bairro_nome} é longe?"** (Responda com tempos).
- **H2: "O condomínio é caro?"** (Analise o custo x benefício).
- **H2: "E a segurança?"** (Dados reais).
- **H2: "Vale a pena investir agora?"**.
"""

        # FALLBACK: Se for genérico, usa a lógica antiga baseada no Cluster
        else:
            return self._get_cluster_suggestions(cluster_key, bairro_nome)

    def _get_cluster_suggestions(self, cluster_key, bairro_nome):
        """Sugestões baseadas no Cluster (Fallback para formatos livres)"""
        if cluster_key in ("INVESTOR", "LOGISTICS"):
            return f"""
## 5. ESTRUTURA SUGERIDA (INVESTIDOR)
- H2: Análise Racional da Localização.
- H2: Os Números que Importam (Valorização).
- H2: Infraestrutura para Negócios.
- H2: Conclusão Financeira.
"""
        elif cluster_key == "FAMILY":
            return f"""
## 5. ESTRUTURA SUGERIDA (FAMÍLIA)
- H2: Como é a Vida das Crianças Aqui.
- H2: Segurança e Tranquilidade na Prática.
- H2: O Que Fazer no Fim de Semana (Sem Sair do Bairro).
- H2: Por que Escolhemos Este Local.
"""
        else:
            return f"""
## 5. ESTRUTURA SUGERIDA (GERAL)
- H2: Localização Estratégica.
- H2: O Diferencial que Ninguém Vê.
- H2: Análise de Custo-Benefício.
- H2: Veredito Final.
"""

    def build(self, d, data_pub, data_mod, regras_texto_ajustada):
        if d.get('tipo_pauta') == "PORTAL":
            return self._build_portal_prompt(d, data_pub, data_mod, regras_texto_ajustada)
        else:
            return self._build_real_estate_prompt(d, data_pub, data_mod, regras_texto_ajustada)

    # =========================================================================
    # MODO IMOBILIÁRIA (AGORA COM MOTOR DE FORMATO ATIVO)
    # =========================================================================
    def _build_real_estate_prompt(self, d, data_pub, data_mod, regras_texto_ajustada):
        data_fmt = self._format_date_blogger(data_pub)
        ativo = d['ativo_definido']
        bairro_nome = d['bairro']['nome'] if d['bairro'] else "Indaiatuba"
        cluster_key = d.get('cluster_tecnico', 'FAMILY')
        formato_key = d.get('formato', 'GUIA_DEFINITIVO') # Pega o formato escolhido
        
        historico_txt = "\n".join([f"- {t}" for t in d.get('historico_titulos', [])])

        estilo_html = f"""<style>
.post-body h2 {{ color: {GenesisConfig.COLOR_PRIMARY}; border-bottom: 2px solid #eee; padding-bottom: 10px; margin-top: 30px; }}
.post-body h3 {{ color: #cc0000; margin-top: 20px; }}
.post-body p {{ font-size: 19px; line-height: 1.6; color: #333; }}
.post-body table {{ width: 100%; min-width: 600px; border-collapse: collapse; margin: 20px 0; }}
.post-body th {{ background-color: {GenesisConfig.COLOR_PRIMARY}; color: white; padding: 12px; }}
.post-body td {{ padding: 12px; border: 1px solid #ccc; }}
</style>"""

        # AQUI A MÁGICA ACONTECE: Injeta a estrutura específica do formato
        structural_guidelines = self._get_structural_guidelines(formato_key, cluster_key, bairro_nome)

        return f"""
## GENESIS MAGNETO V.55 — STRUCTURE AWARE
**Objetivo:** Texto SEO Imobiliário com ESTRUTURA RÍGIDA baseada no formato escolhido.

### 🛡️ PROTOCOLO ANTI-CANIBALISMO
Evite repetir os ângulos destes artigos passados:
{historico_txt}

---

## 1. O CONTEXTO
- **FORMATO ESCOLHIDO:** {formato_key} (Siga a estrutura abaixo RIGOROSAMENTE).
- **ÂNGULO EDITORIAL:** {d.get('topico', 'Geral')}
- **ATIVO:** {ativo}
- **BAIRRO:** {bairro_nome}
- **PERSONA:** {d['persona']['nome']}
- **GATILHO MENTAL:** {d['gatilho']}

## 2. CONFIGURAÇÃO VISUAL (CSS)
Use este CSS inline:
{estilo_html}

## 3. MANUAL DE ESTILO (REGRAS.TXT)
{regras_texto_ajustada}

{structural_guidelines}

### 🚫 PROIBIÇÕES
1. **JAMAIS** ignore o FORMATO. Se for Lista, faça Lista. Se for Comparativo, faça Tabela.
2. **JAMAIS** use títulos genéricos.

## 6. CTA OBRIGATÓRIO (CAPTURA)
Insira **EXATAMENTE** este código ao final:
{self.CTA_CAPTURE_CODE}

## 7. CHECKLIST DE ENTREGA
1. LOG BASTIDORES
2. BLOCKCODE HTML (Com JSON-LD)
3. TÍTULO (H1) - Deve refletir o formato (Ex: "7 Mitos...", "Guia Completo...").
4. MARCADORES: {self._generate_seo_tags(d)}
5. DATA: {data_fmt}
6. DESCRIÇÃO (Meta)
7. IMAGEM PROMPT
""".strip()

    def _build_portal_prompt(self, d, data_pub, data_mod, regras_texto_ajustada):
        # Mantém a lógica simples para o Portal, mas injeta o CSS novo
        return f"""
## GENESIS MAGNETO V.55 — PORTAL MODE
**Objetivo:** Notícia de Utilidade Pública.

## 1. A PAUTA
- **TEMA:** {d['ativo_definido']}
- **LOCAL:** {d['bairro']['nome'] if d['bairro'] else 'Indaiatuba'}
- **ÂNGULO:** {d.get('topico', 'Geral')}

## 2. ESTRUTURA
Use lide jornalístico (Quem, Quando, Onde, Por que).
Seja impessoal e informativo.

## 3. CTA
{self.CTA_CAPTURE_CODE}

## 4. REGRAS
{regras_texto_ajustada}
""".strip()
