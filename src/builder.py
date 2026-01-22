# src/builder.py
import datetime
import json
from .config import GenesisConfig

class PromptBuilder:
    """
    O 'Redator' (Versão 56 - Tone & Structure Aware).
    Agora sincroniza FORMATO (Estrutura) e GATILHO (Tonalidade).
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
        if d.get('formato'): tags.append(d['formato'])
        return ", ".join(tags[:10])

    # =========================================================================
    # MOTOR DE ESTRUTURA (FORMATO)
    # =========================================================================
    def _get_structural_guidelines(self, formato_key, cluster_key, bairro_nome):
        # ... (Mantém a lógica da versão anterior 55) ...
        if formato_key == "LISTA_POLEMICA":
            return f"""
## 5. ESTRUTURA OBRIGATÓRIA: LISTA POLÊMICA
**Você NÃO está escrevendo um artigo comum.** Você está escrevendo uma LISTA NUMERADA.
Estrutura dos H2:
- **H2: Mito #1:** [Mito Comum]
- **H2: Mito #2:** [Outro Mito]
- **H2: Mito #3:** [Mito Financeiro]
- **H2: A Verdade Final:** (Conclusão).
*Tom:* Provocativo e "Contra-Intuitivo".
"""
        elif formato_key == "COMPARATIVO_TECNICO":
            return f"""
## 5. ESTRUTURA OBRIGATÓRIA: BATALHA COMPARATIVA
Estrutura dos H2:
- **H2: Round 1: Localização**
- **H2: Round 2: Custo-Benefício**
- **H2: Round 3: Vizinhança**
- **H2: Veredito**
**OBRIGATÓRIO:** Inserir TABELA HTML comparativa no meio.
"""
        elif formato_key == "GUIA_DEFINITIVO":
            return f"""
## 5. ESTRUTURA OBRIGATÓRIA: MANUAL COMPLETO
Estrutura dos H2:
- **H2: Capítulo 1: O Raio-X**
- **H2: Capítulo 2: Infraestrutura**
- **H2: Capítulo 3: O Imóvel Ideal**
- **H2: Capítulo 4: Valorização**
- **H2: Checklist Final**.
"""
        elif formato_key == "INSIGHT_DE_CORRETOR":
            return f"""
## 5. ESTRUTURA OBRIGATÓRIA: BASTIDORES (1ª PESSOA)
Estrutura dos H2:
- **H2: O que vi na visita técnica**
- **H2: O detalhe escondido**
- **H2: História real de cliente**
- **H2: Minha opinião sincera**.
"""
        elif formato_key == "PERGUNTAS_RESPOSTAS":
            return f"""
## 5. ESTRUTURA OBRIGATÓRIA: FAQ
Estrutura dos H2:
- **H2: "É longe?"**
- **H2: "É caro?"**
- **H2: "É seguro?"**
- **H2: "Vale a pena?"**.
"""
        else:
            # Fallback genérico
            return f"""
## 5. ESTRUTURA SUGERIDA (CLUSTER {cluster_key})
- H2: Análise da Localização
- H2: Pontos Fortes e Fracos
- H2: Potencial de Valorização
- H2: Conclusão
"""

    # =========================================================================
    # MOTOR DE TONALIDADE (NOVO) - DITADOR DE GATILHOS
    # =========================================================================
    def _get_tone_guidelines(self, gatilho_key):
        """
        Traduz o Gatilho Mental em ordens de comportamento e vocabulário.
        """
        if gatilho_key == "ESCASSEZ":
            return """
### 🧠 MODULAÇÃO DE TOM: ESCASSEZ (A Joia da Coroa)
- **Atitude:** "Isso está a acabar". Você está a apresentar algo raro.
- **Palavras-Chave Obrigatórias:** Raro, Último, Único, Difícil de encontrar, Exclusivo.
- **Proibido:** Dizer que "existem muitas opções".
- **Abertura:** Comece dizendo que este tipo de imóvel quase nunca aparece à venda.
"""
        elif gatilho_key == "URGENCIA":
            return """
### 🧠 MODULAÇÃO DE TOM: URGÊNCIA (Agora ou Nunca)
- **Atitude:** "O tempo está a contar". O mercado está a mudar rápido.
- **Palavras-Chave Obrigatórias:** Agora, Janela de oportunidade, Timing, Imediato.
- **Abertura:** Cite uma mudança recente (lei, obra, preço) que exige ação hoje.
"""
        elif gatilho_key == "AUTORIDADE":
            return """
### 🧠 MODULAÇÃO DE TOM: AUTORIDADE (Quem Sabe Faz)
- **Atitude:** "Eu sou o especialista". Tom sóbrio, técnico e seguro.
- **Palavras-Chave Obrigatórias:** Análise, Histórico, Dados, Comprovado, Estudo.
- **Estilo:** Use frases curtas e afirmativas. Não use "eu acho", use "os dados mostram".
"""
        elif gatilho_key == "PROVA_SOCIAL":
            return """
### 🧠 MODULAÇÃO DE TOM: PROVA SOCIAL (O Que Todos Dizem)
- **Atitude:** "Todo a gente quer isto". Foco na alta procura e desejo coletivo.
- **Palavras-Chave Obrigatórias:** Cobiçado, Disputado, Famílias procuram, Tendência.
- **Abertura:** Comece falando sobre como este bairro se tornou o queridinho da cidade.
"""
        elif gatilho_key == "NOVIDADE":
            return """
### 🧠 MODULAÇÃO DE TOM: NOVIDADE (O Novo)
- **Atitude:** "Você viu isto primeiro aqui". Entusiasmo de descoberta.
- **Palavras-Chave Obrigatórias:** Inédito, Lançamento, Novo conceito, Moderno, Estreia.
- **Foco:** O que mudou? O que é diferente do passado?
"""
        elif gatilho_key == "MEDO":
            return """
### 🧠 MODULAÇÃO DE TOM: MEDO (Aversão à Perda)
- **Atitude:** "Cuidado para não errar". O papel de protetor/alerta.
- **Palavras-Chave Obrigatórias:** Risco, Cuidado, Atenção, Erro comum, Prejuízo.
- **Abertura:** Comece com um alerta: "Muitos compram errado neste bairro por não saberem disto...".
"""
        elif gatilho_key == "CURIOSIDADE":
            return """
### 🧠 MODULAÇÃO DE TOM: CURIOSIDADE (O Segredo)
- **Atitude:** "Tenho um segredo". Fale baixo, confessional.
- **Palavras-Chave Obrigatórias:** Poucos sabem, Segredo, Detalhe, Escondido.
- **Técnica:** Abra loops no início ("Vou te contar o porquê no final...") e feche só na conclusão.
"""
        else:
            return """
### 🧠 MODULAÇÃO DE TOM: PADRÃO (Lógico & Emocional)
- Equilibre razão (dados) e emoção (benefícios).
- Seja consultivo e prestativo.
"""

    def build(self, d, data_pub, data_mod, regras_texto_ajustada):
        if d.get('tipo_pauta') == "PORTAL":
            return self._build_portal_prompt(d, data_pub, data_mod, regras_texto_ajustada)
        else:
            return self._build_real_estate_prompt(d, data_pub, data_mod, regras_texto_ajustada)

    def _build_real_estate_prompt(self, d, data_pub, data_mod, regras_texto_ajustada):
        data_fmt = self._format_date_blogger(data_pub)
        ativo = d['ativo_definido']
        bairro_nome = d['bairro']['nome'] if d['bairro'] else "Indaiatuba"
        cluster_key = d.get('cluster_tecnico', 'FAMILY')
        formato_key = d.get('formato', 'GUIA_DEFINITIVO')
        gatilho_key = d.get('gatilho', 'AUTORIDADE') # Pega o gatilho
        
        historico_txt = "\n".join([f"- {t}" for t in d.get('historico_titulos', [])])

        estilo_html = f"""<style>
.post-body h2 {{ color: {GenesisConfig.COLOR_PRIMARY}; border-bottom: 2px solid #eee; padding-bottom: 10px; margin-top: 30px; }}
.post-body h3 {{ color: #cc0000; margin-top: 20px; }}
.post-body p {{ font-size: 19px; line-height: 1.6; color: #333; }}
.post-body table {{ width: 100%; min-width: 600px; border-collapse: collapse; margin: 20px 0; }}
.post-body th {{ background-color: {GenesisConfig.COLOR_PRIMARY}; color: white; padding: 12px; }}
.post-body td {{ padding: 12px; border: 1px solid #ccc; }}
</style>"""

        # GERAÇÃO DAS DIRETRIZES DINÂMICAS
        structural_guidelines = self._get_structural_guidelines(formato_key, cluster_key, bairro_nome)
        tone_guidelines = self._get_tone_guidelines(gatilho_key)

        return f"""
## GENESIS MAGNETO V.56 — TONE & STRUCTURE ENGINE
**Objetivo:** Texto Imobiliário com ESTRUTURA RÍGIDA e TOM CONTROLADO.

### 🛡️ PROTOCOLO ANTI-CANIBALISMO
Evite repetir os ângulos destes artigos passados:
{historico_txt}

---

## 1. O CONTEXTO
- **FORMATO:** {formato_key}
- **GATILHO MENTAL:** {gatilho_key}
- **ATIVO:** {ativo}
- **BAIRRO:** {bairro_nome}
- **PERSONA:** {d['persona']['nome']}
- **DOR DA PERSONA:** {d['persona']['dor']}

## 2. CONFIGURAÇÃO VISUAL (CSS)
Use este CSS inline:
{estilo_html}

## 3. MANUAL DE ESTILO (REGRAS.TXT)
{regras_texto_ajustada}

{structural_guidelines}

{tone_guidelines}

### 🚫 PROIBIÇÕES FINAIS
1. **JAMAIS** ignore o FORMATO.
2. **JAMAIS** saia do TOM definido acima (respeite as palavras-chave obrigatórias).

## 6. CTA OBRIGATÓRIO (CAPTURA)
Insira **EXATAMENTE** este código ao final:
{self.CTA_CAPTURE_CODE}

## 7. CHECKLIST DE ENTREGA
1. LOG BASTIDORES
2. BLOCKCODE HTML (Com JSON-LD)
3. TÍTULO (H1) - Deve refletir o GATILHO e o FORMATO.
4. MARCADORES: {self._generate_seo_tags(d)}
5. DATA: {data_fmt}
6. DESCRIÇÃO (Meta)
7. IMAGEM PROMPT
""".strip()

    def _build_portal_prompt(self, d, data_pub, data_mod, regras_texto_ajustada):
        return f"""
## GENESIS MAGNETO V.56 — PORTAL MODE
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
