# src/builder.py
import datetime
import json
from .config import GenesisConfig

class PromptBuilder:
    """
    O 'Redator' (Versão 60.1 - Synced Editions).
    Separação total de lógica entre Portal e Imobiliária.
    Inclui Filtros Cognitivos para evitar contaminação de persona.
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
        """
        Gera tags otimizadas e sensíveis ao contexto (Portal vs Imobiliária).
        """
        # 1. Definição da Base de Tags
        if d.get('tipo_pauta') == "PORTAL":
            tags = ["Indaiatuba", "Notícias Indaiatuba", "Portal da Cidade", "Utilidade Pública"]
        else:
            tags = ["Indaiatuba", "Imóveis Indaiatuba", "Mercado Imobiliário", "Morar em Indaiatuba"]

        # 2. Injeção de Localização
        if d.get('bairro') and d['bairro']['nome'] != "Indaiatuba":
            tags.append(d['bairro']['nome'])
        
        # 3. Injeção de Ativo/Editoria (Limpo)
        raw_ativo = d.get('ativo_definido', '')
        # Remove sufixos como (Loteamento Aberto) ou (Portal)
        ativo_limpo = raw_ativo.split('(')[0].strip()
        if ativo_limpo: 
            tags.append(ativo_limpo)
        
        # 4. Injeção de Tópico
        if d.get('topico'): 
            tags.append(d['topico'])
        
        # 5. Deduplicação mantendo ordem
        seen = set()
        final_tags = [x for x in tags if not (x in seen or seen.add(x))]
        
        return ", ".join(final_tags[:10])

    def _get_portal_structure(self, formato_key, editoria, tema):
        """
        Define a arquitetura da informação para Jornalismo Moderno.
        """
        
        # 1. EXPLAINER (Jornalismo Didático)
        if formato_key == "EXPLAINER":
            return f"""
## 5. ESTRUTURA: EXPLAINER (ENTENDA O CASO)
O leitor está confuso. Sua missão é explicar o tema "{tema}" de forma didática.
- **Intro:** O que aconteceu? (Resumo em 1 parágrafo).
- **Contexto:** Como chegamos até aqui? (Background).
- **O que muda na prática:** 3 pontos fundamentais que afetam a vida do leitor.
- **Próximos passos:** O que esperar do futuro?
*Estilo:* Use analogias simples. Evite "juridiquês" ou "politiquês".
"""

        # 2. DOSSIÊ INVESTIGATIVO (Profundidade)
        elif formato_key == "DOSSIE_INVESTIGATIVO":
            return f"""
## 5. ESTRUTURA: DOSSIÊ INVESTIGATIVO (LONGFORM)
Uma análise profunda sobre {editoria}.
- **Manchete Impactante.**
- **O Problema:** Dados e fatos que mostram a dimensão da questão.
- **As Causas:** Por que isso acontece em Indaiatuba?
- **O Outro Lado:** O que dizem as autoridades ou envolvidos?
- **Impacto Humano:** Histórias reais de quem é afetado.
*Estilo:* Jornalismo sério, baseada em dados, mas com narrativa envolvente.
"""

        # 3. CHECAGEM DE FATOS (Fact-Checking)
        elif formato_key == "CHECAGEM_FATOS":
            return f"""
## 5. ESTRUTURA: CHECAGEM DE FATOS (VERDADE OU MENTIRA?)
Há boatos circulando sobre "{tema}". Vamos esclarecer.
- **O Boato:** "Dizem por aí que..." (Cite o que circula no WhatsApp/Redes).
- **A Checagem:** O que apuramos (Fomos até o local, ligamos para o órgão, checamos a lei).
- **As Evidências:** Mostre provas (Dados, fotos, documentos).
- **Veredito:** É VERDADE, É MENTIRA ou É IMPRECISO?
*Estilo:* Direto, seco e baseado puramente em evidências.
"""

        # 4. LISTA DE CURADORIA (Serviço/Lazer)
        elif formato_key == "LISTA_CURADORIA":
            return f"""
## 5. ESTRUTURA: CURADORIA (LISTA TOP X)
O leitor quer recomendações confiáveis sobre {editoria}.
- **Intro:** Por que esse tema está em alta?
- **Item 1 a 5:** Seleção criteriosa. Para cada item, explique ONDE fica, QUANTO custa e POR QUE vale a pena.
- **Dica de Ouro:** Um segredo extra para quem leu até o fim.
*Estilo:* Leve, convidativo e útil. Como uma dica de amigo expert.
"""

        # 5. SERVIÇO PASSO A PASSO (Utilidade Pública)
        elif formato_key == "SERVICO_PASSO_A_PASSO":
            return f"""
## 5. ESTRUTURA: TUTORIAL DE SERVIÇO
Guia prático para resolver um problema do cidadão ({tema}).
- **O que é:** Breve definição.
- **Quem tem direito/Quem é afetado:** Critérios claros.
- **Passo a Passo:** Lista numerada (1, 2, 3...) de como proceder.
- **Documentos/Locais:** Onde ir, o que levar.
*Estilo:* Imperativo ("Faça", "Leve", "Acesse"). Foco total em utilidade.
"""

        # 6. HARD NEWS (Notícia Padrão)
        elif formato_key == "NOTICIA_IMPACTO":
            return f"""
## 5. ESTRUTURA: HARD NEWS (PIRÂMIDE INVERTIDA)
Notícia quente e objetiva sobre {editoria}.
- **Lide (Lead):** Quem, o quê, onde, quando e porquê no 1º parágrafo.
- **Corpo:** Detalhes secundários, falas de testemunhas/autoridades.
- **Contexto:** Isso já aconteceu antes? Dados relacionados.
- **Serviço:** Telefones ou links úteis se necessário.
"""

        # 7. ENTREVISTA PING-PONG
        elif formato_key == "ENTREVISTA_PING_PONG":
            return f"""
## 5. ESTRUTURA: ENTREVISTA (PING-PONG)
Conversa direta com uma fonte relevante sobre {tema}.
- **Intro:** Quem é o entrevistado e por que ele importa agora.
- **Pergunta 1:** (Sobre o problema atual).
- **Pergunta 2:** (Sobre soluções).
- **Pergunta 3:** (Mensagem para a população).
*Estilo:* Transcreva as respostas de forma fluida, mantendo a voz do entrevistado.
"""

        # FALLBACK
        else:
            return "## 5. ESTRUTURA LIVRE\nDesenvolva uma matéria jornalística completa, com início, meio e fim, focada no interesse público."

    def _get_real_estate_guidelines(self, formato_key, cluster, bairro):
        # Lógica "Unchained" para Imobiliária
        
        base_instruction = f"""
## 5. CAMINHOS PARA EXPLORAR A FUNDO (MERCADO IMOBILIÁRIO)
Escreva um texto ÉPICO e detalhado sobre {bairro}.
Não economize palavras. Use storytelling, dados técnicos e persuasão.
Disserte sobre estilo de vida, valorização e diferenciais ocultos.
"""

        if formato_key == "LISTA_POLEMICA":
            return base_instruction + "\n- Quebre mitos comuns sobre o bairro.\n- Use 'Mito vs Verdade'."
        elif formato_key == "COMPARATIVO_TECNICO":
            return base_instruction + "\n- Compare com outros bairros similares.\n- Seja brutalmente honesto nos prós e contras."
        elif formato_key == "INSIGHT_DE_CORRETOR":
            return base_instruction + "\n- Use Primeira Pessoa (Eu/Nós).\n- Conte segredos de bastidores."
        else:
            return base_instruction

    def _get_tone_guidelines(self, gatilho_key):
        if gatilho_key == "NEUTRAL_JOURNALISM":
            return """
### 🧠 MENTALIDADE DE ESCRITOR (JORNALISTA)
- **Tom:** Imparcial, objetivo e focado em fatos.
- **Proibido:** Adjetivos de venda ("maravilhoso", "oportunidade").
- **Foco:** Informar e prestar serviço.
"""
        else:
            return """
### 🧠 MENTALIDADE DE ESCRITOR (DEEP FLOW / COPYWRITER)
- **Profundidade:** Não seja raso. Aprofunde-se nas causas e consequências.
- **Fluidez:** Escreva parágrafos encadeados, sem quebras bruscas.
- **Conexão:** Use uma linguagem persuasiva e envolvente.
"""

    def build(self, d, data_pub, data_mod, regras_texto_ajustada):
        if d.get('tipo_pauta') == "PORTAL":
            return self._build_portal_prompt(d, data_pub, data_mod, regras_texto_ajustada)
        else:
            return self._build_real_estate_prompt(d, data_pub, data_mod, regras_texto_ajustada)

    # =========================================================================
    # MODO PORTAL (MODERN JOURNALISM)
    # =========================================================================
    def _build_portal_prompt(self, d, data_pub, data_mod, regras_texto_ajustada):
        data_fmt = self._format_date_blogger(data_pub)
        formato_key = d.get('formato', 'NOTICIA_IMPACTO')
        editoria = d.get('ativo_definido', 'Geral') # Agora 'ativo' é a Editoria
        tema = d.get('topico', 'Geral')
        
        structure_guide = self._get_portal_structure(formato_key, editoria, tema)
        tone_guide = self._get_tone_guidelines("NEUTRAL_JOURNALISM")
        
        return f"""
## GENESIS MAGNETO V.60 — PORTAL NEWS ENGINE
**Objetivo:** JORNALISMO LOCAL DE ALTO NÍVEL.
**Persona:** PORTAL DA CIDADE (Credibilidade, Utilidade e Imparcialidade).

## 1. A PAUTA
- **EDITORIA:** {editoria}
- **TEMA/ÂNGULO:** {tema}
- **LOCAL:** Indaiatuba (Abrangência Municipal)
- **FORMATO:** {formato_key}

## 2. MISSÃO JORNALÍSTICA
Você é um repórter investigativo e comunitário.
- **Foco:** Interesse Público. Como isso afeta a vida do cidadão?
- **Tom:** Profissional, mas próximo. Evite sensacionalismo barato.
- **Dados:** Sempre que possível, cite dados (invente dados realistas para o exercício se necessário, mantendo coerência).

{structure_guide}

{tone_guide}

## 3. INSUMOS (REGRAS & CONTEXTO)
**DIRETRIZ SUPREMA DE PERSONA (FILTRO COGNITIVO):**
1. Você deve **IGNORAR** completamente a "OPÇÃO A (IMOBILIÁRIA)" do arquivo de regras abaixo.
2. Você DEVE encarnar **APENAS** a "OPÇÃO B (PORTAL DA CIDADE)".
3. Seu compromisso é com a verdade jornalística, não com a venda.

<REGRAS_DO_SISTEMA>
{regras_texto_ajustada}
</REGRAS_DO_SISTEMA>

## 4. CTA (ENGAGEMENT)
{self.CTA_CAPTURE_CODE}

## 5. CHECKLIST FINAL
1. TÍTULO (H1): Manchete jornalística (curta e direta).
2. LIDE: Primeiro parágrafo respondendo às questões chaves.
3. CONTEÚDO: Corpo robusto e informativo.
4. JSON-LD: Schema de 'NewsArticle'.
5. MARCADORES: {self._generate_seo_tags(d)}
""".strip()

    # =========================================================================
    # MODO IMOBILIÁRIA (UNCHAINED LEGACY)
    # =========================================================================
    def _build_real_estate_prompt(self, d, data_pub, data_mod, regras_texto_ajustada):
        data_fmt = self._format_date_blogger(data_pub)
        ativo = d['ativo_definido']
        bairro_nome = d['bairro']['nome'] if d['bairro'] else "Indaiatuba"
        cluster = d.get('cluster_tecnico', 'FAMILY')
        formato = d.get('formato', 'GUIA_DEFINITIVO')
        gatilho = d.get('gatilho', 'AUTORIDADE')
        
        structure = self._get_real_estate_guidelines(formato, cluster, bairro_nome)
        tone = self._get_tone_guidelines(gatilho)

        return f"""
## GENESIS MAGNETO V.60 — REAL ESTATE (UNCHAINED)
**Objetivo:** Copywriting Imobiliário Persuasivo e Profundo.
**Persona:** IMOBILIÁRIA SABER (Vendas).

## 1. O CENÁRIO
- **ATIVO:** {ativo}
- **LOCAL:** {bairro_nome}
- **CLIENTE:** {d['persona']['nome']}
- **FORMATO:** {formato}
- **GATILHO:** {gatilho}

## 2. CARTA DE ALFORRIA (LIBERDADE TOTAL)
Escreva um texto rico, longo e detalhado. Venda o sonho e a realidade técnica.
{structure}
{tone}

## 3. INSUMOS
**DIRETRIZ SUPREMA DE PERSONA (FILTRO COGNITIVO):**
1. Você deve **IGNORAR** completamente a "OPÇÃO B (PORTAL)" do arquivo de regras abaixo.
2. Você DEVE encarnar **APENAS** a "OPÇÃO A (IMOBILIÁRIA SABER)".
3. Seu objetivo é encantar, persuadir e vender.

<REGRAS_DO_SISTEMA>
{regras_texto_ajustada}
</REGRAS_DO_SISTEMA>

## 4. CTA
{self.CTA_CAPTURE_CODE}

## 5. CHECKLIST FINAL
1. TÍTULO (H1): Persuasivo e com SEO.
2. CONTEÚDO: Rico e detalhado.
3. MARCADORES: {self._generate_seo_tags(d)}
4. JSON-LD: Schema de 'BlogPosting'.
""".strip()
