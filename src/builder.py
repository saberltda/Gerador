# src/builder.py
import datetime
import json
from .config import GenesisConfig

class PromptBuilder:
    """
    O 'Redator' (Versão 61 - News Edition).
    Inclui suporte nativo para 'Resumo do Dia' com ordens de busca em tempo real.
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
        ativo_limpo = raw_ativo.split('(')[0].strip()
        if ativo_limpo: 
            tags.append(ativo_limpo)
        
        # 4. Injeção de Tópico
        if d.get('topico'): 
            tags.append(d['topico'])
        
        # 5. Deduplicação
        seen = set()
        final_tags = [x for x in tags if not (x in seen or seen.add(x))]
        
        return ", ".join(final_tags[:10])

    def _get_portal_structure(self, formato_key, editoria, tema):
        
        # --- NOVO BLOCO: RESUMO DO DIA (LÓGICA ESPECIAL) ---
        if "Resumo" in editoria or "Notícias" in editoria:
            return f"""
## 5. ESTRUTURA: RESUMO DO DIA (TEMPO REAL)
**ORDEM DE BUSCA:** Você deve agir como um agregador de notícias.
1. **Busque na Web/Base de Dados:** O que aconteceu HOJE em Indaiatuba?
2. **Filtre:** Selecione os 3 a 5 fatos mais relevantes (Trânsito, Polícia, Política, Eventos).
3. **Escreva:**
   - **Manchete do Dia:** O fato principal.
   - **Giro Rápido:** Lista com bullet points das outras notícias.
   - **Previsão do Tempo:** Para hoje à noite e amanhã.
   - **Serviço:** Farmácias de plantão ou avisos da Prefeitura (se houver).
*Estilo:* Objetivo, "Curto e Grosso".
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
"""

        # 3. CHECAGEM DE FATOS (Fact-Checking)
        elif formato_key == "CHECAGEM_FATOS":
            return f"""
## 5. ESTRUTURA: CHECAGEM DE FATOS (VERDADE OU MENTIRA?)
Há boatos circulando sobre "{tema}". Vamos esclarecer.
- **O Boato:** "Dizem por aí que..."
- **A Checagem:** O que apuramos (Fatos reais).
- **As Evidências:** Mostre provas (Dados, fotos, documentos).
- **Veredito:** É VERDADE, É MENTIRA ou É IMPRECISO?
"""

        # 4. LISTA DE CURADORIA (Serviço/Lazer)
        elif formato_key == "LISTA_CURADORIA":
            return f"""
## 5. ESTRUTURA: CURADORIA (LISTA TOP X)
O leitor quer recomendações confiáveis sobre {editoria}.
- **Intro:** Por que esse tema está em alta?
- **Item 1 a 5:** Seleção criteriosa (Onde, Quanto, Porquê).
- **Dica de Ouro:** Um segredo extra.
"""

        # 5. SERVIÇO PASSO A PASSO (Utilidade Pública)
        elif formato_key == "SERVICO_PASSO_A_PASSO":
            return f"""
## 5. ESTRUTURA: TUTORIAL DE SERVIÇO
Guia prático para resolver um problema do cidadão ({tema}).
- **O que é:** Breve definição.
- **Quem tem direito:** Critérios.
- **Passo a Passo:** Lista numerada.
- **Onde ir:** Endereços e Links.
"""

        # 6. HARD NEWS (Notícia Padrão)
        elif formato_key == "NOTICIA_IMPACTO":
            return f"""
## 5. ESTRUTURA: HARD NEWS (PIRÂMIDE INVERTIDA)
Notícia quente e objetiva sobre {editoria}.
- **Lide (Lead):** Quem, o quê, onde, quando e porquê no 1º parágrafo.
- **Corpo:** Detalhes secundários.
- **Contexto:** Histórico breve.
- **Serviço:** Telefones/Links úteis.
"""

        # 7. ENTREVISTA PING-PONG
        elif formato_key == "ENTREVISTA_PING_PONG":
            return f"""
## 5. ESTRUTURA: ENTREVISTA (PING-PONG)
Conversa direta com uma fonte relevante sobre {tema}.
- **Intro:** Quem é o entrevistado.
- **Perguntas e Respostas:** Transcrição fluida e editada.
"""

        else:
            return "## 5. ESTRUTURA LIVRE\nDesenvolva uma matéria jornalística completa."

    def _get_real_estate_guidelines(self, formato_key, cluster, bairro):
        base_instruction = f"""
## 5. CAMINHOS PARA EXPLORAR A FUNDO (MERCADO IMOBILIÁRIO)
Escreva um texto ÉPICO e detalhado sobre {bairro}.
Não economize palavras. Use storytelling, dados técnicos e persuasão.
"""
        if formato_key == "LISTA_POLEMICA":
            return base_instruction + "\n- Quebre mitos comuns (Mito vs Verdade)."
        elif formato_key == "COMPARATIVO_TECNICO":
            return base_instruction + "\n- Compare com outros bairros. Seja honesto."
        elif formato_key == "INSIGHT_DE_CORRETOR":
            return base_instruction + "\n- Use Primeira Pessoa (Eu/Nós). Conte bastidores."
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
### 🧠 MENTALIDADE DE ESCRITOR (COPYWRITER)
- **Profundidade:** Não seja raso. Aprofunde-se.
- **Conexão:** Use linguagem persuasiva e envolvente.
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
        editoria = d.get('ativo_definido', 'Geral')
        tema = d.get('topico', 'Geral')
        
        structure_guide = self._get_portal_structure(formato_key, editoria, tema)
        tone_guide = self._get_tone_guidelines("NEUTRAL_JOURNALISM")
        
        return f"""
## GENESIS MAGNETO V.61 — PORTAL NEWS ENGINE
**Objetivo:** JORNALISMO LOCAL DE ALTO NÍVEL.
**Persona:** PORTAL DA CIDADE.

## 1. A PAUTA
- **EDITORIA:** {editoria}
- **TEMA:** {tema}
- **LOCAL:** Indaiatuba (Cidade Inteira)
- **FORMATO:** {formato_key}

## 2. MISSÃO JORNALÍSTICA
Você é um repórter investigativo e comunitário.
- **Foco:** Interesse Público.
- **Dados:** Use dados reais sempre que possível (ou simule com coerência extrema se for exercício).
- **Busca:** Se for "Resumo do Dia", FAÇA A BUSCA DE FATOS REAIS.

{structure_guide}

{tone_guide}

## 3. INSUMOS (FILTRO COGNITIVO)
**DIRETRIZ SUPREMA:**
1. IGNORAR completamente a "OPÇÃO A (IMOBILIÁRIA)".
2. ENCARNAR apenas a "OPÇÃO B (PORTAL DA CIDADE)".
3. Compromisso total com a verdade jornalística.

<REGRAS_DO_SISTEMA>
{regras_texto_ajustada}
</REGRAS_DO_SISTEMA>

## 4. CTA (ENGAGEMENT)
{self.CTA_CAPTURE_CODE}

## 5. CHECKLIST FINAL
1. TÍTULO (H1): Manchete jornalística.
2. LIDE: Resumo inicial (Quem, Quando, Onde).
3. CONTEÚDO: Robusto e informativo.
4. JSON-LD: Schema 'NewsArticle'.
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
## GENESIS MAGNETO V.61 — REAL ESTATE (UNCHAINED)
**Objetivo:** Copywriting Imobiliário Persuasivo.
**Persona:** IMOBILIÁRIA SABER.

## 1. O CENÁRIO
- **ATIVO:** {ativo}
- **LOCAL:** {bairro_nome}
- **CLIENTE:** {d['persona']['nome']}
- **FORMATO:** {formato}
- **GATILHO:** {gatilho}

## 2. CARTA DE ALFORRIA
Escreva um texto rico, longo e detalhado. Venda o sonho.
{structure}
{tone}

## 3. INSUMOS (FILTRO COGNITIVO)
**DIRETRIZ SUPREMA:**
1. IGNORAR completamente a "OPÇÃO B (PORTAL)".
2. ENCARNAR apenas a "OPÇÃO A (IMOBILIÁRIA SABER)".
3. Objetivo: Encantar e Vender.

<REGRAS_DO_SISTEMA>
{regras_texto_ajustada}
</REGRAS_DO_SISTEMA>

## 4. CTA
{self.CTA_CAPTURE_CODE}

## 5. CHECKLIST FINAL
1. TÍTULO (H1): Persuasivo.
2. CONTEÚDO: Rico e detalhado.
3. MARCADORES: {self._generate_seo_tags(d)}
4. JSON-LD: Schema 'BlogPosting'.
""".strip()
