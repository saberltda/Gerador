# src/builder.py
import datetime
import json
from .config import GenesisConfig

class PromptBuilder:
    """
    O 'Redator' (Versão 64 - Brasilia Timezone Forced).
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
        if d.get('tipo_pauta') == "PORTAL":
            tags = ["Indaiatuba", "Notícias Indaiatuba", "Portal da Cidade", "Giro de Notícias", "Aconteceu em Indaiatuba"]
        else:
            tags = ["Indaiatuba", "Imóveis Indaiatuba", "Mercado Imobiliário", "Morar em Indaiatuba"]

        if d.get('bairro') and d['bairro']['nome'] != "Indaiatuba":
            tags.append(d['bairro']['nome'])
        
        raw_ativo = d.get('ativo_definido', '')
        ativo_limpo = raw_ativo.split('(')[0].strip()
        if ativo_limpo: tags.append(ativo_limpo)
        
        if d.get('topico'): tags.append(d['topico'])
        
        seen = set()
        final_tags = [x for x in tags if not (x in seen or seen.add(x))]
        
        return ", ".join(final_tags[:10])

    def _get_portal_structure(self, formato_key, editoria, tema):
        if "Resumo" in editoria or "Notícias" in editoria:
            return f"""
## 5. ESTRUTURA: REVISTA DIGITAL DIÁRIA (LONGFORM)
**OBJETIVO:** Prender o leitor por 10 minutos.
**ORDEM DE EXECUÇÃO:**
1. **Varredura Completa:** Busque TUDO o que é relevante hoje em Indaiatuba.
2. **Seleção:** Escolha os 4 ou 5 temas mais quentes.

**ESTRUTURA DO TEXTO:**
**MANCHETE DE CAPA:** (Impactante e Local)
**1. A NOTÍCIA PRINCIPAL:** Matéria Completa (Mínimo 4 parágrafos).
**2. O GIRO PELA CIDADE:** 3 a 4 Sub-Manchetes (H3). Desenvolva o texto.
**3. COLUNA SOCIAL & EVENTOS:** O que vai acontecer hoje/amanhã?
**4. SERVIÇO DE UTILIDADE PÚBLICA:** Previsão do Tempo e Trânsito.
**5. A IMAGEM DO DIA:** Descrição poética de uma cena da cidade.
"""
        # Mantém a lógica dos outros formatos...
        if formato_key == "EXPLAINER":
            return "## 5. ESTRUTURA: EXPLAINER\nAula completa sobre o tema. Cronologia, Detalhes Técnicos e Impacto Real."
        elif formato_key == "DOSSIE_INVESTIGATIVO":
            return "## 5. ESTRUTURA: DOSSIÊ INVESTIGATIVO\nAnálise profunda. Manchete, Problema, Causas, Contraponto e Vozes da Cidade."
        elif formato_key == "CHECAGEM_FATOS":
            return "## 5. ESTRUTURA: CHECAGEM DE FATOS\nContexto do boato, Investigação, Evidências e Veredito."
        elif formato_key == "LISTA_CURADORIA":
            return "## 5. ESTRUTURA: GUIA COMPLETO\nRoteiro comentado. Intro, Top 5 com resenha e Dica de Insider."
        elif formato_key == "SERVICO_PASSO_A_PASSO":
            return "## 5. ESTRUTURA: MANUAL DO CIDADÃO\nIntrodução, Documentação, Procedimento Passo a Passo e Onde Ir."
        elif formato_key == "NOTICIA_IMPACTO":
            return "## 5. ESTRUTURA: HARD NEWS COMPLETA\nLide detalhado, Desenvolvimento, Histórico e Repercussão."
        elif formato_key == "ENTREVISTA_PING_PONG":
            return "## 5. ESTRUTURA: A GRANDE ENTREVISTA\nPerfil, Perguntas e Respostas profundas e Bastidores."
        else:
            return "## 5. ESTRUTURA LIVRE (LONGFORM)\nDesenvolva uma matéria extensa."

    def _get_real_estate_guidelines(self, formato_key, cluster, bairro):
        base_instruction = f"""
## 5. CAMINHOS PARA EXPLORAR A FUNDO (MERCADO IMOBILIÁRIO)
Escreva um texto ÉPICO e detalhado sobre {bairro}.
Não economize palavras. Use storytelling, dados técnicos e persuasão.
"""
        if formato_key == "LISTA_POLEMICA": return base_instruction + "\n- Quebre mitos comuns (Mito vs Verdade)."
        elif formato_key == "COMPARATIVO_TECNICO": return base_instruction + "\n- Compare com outros bairros. Seja honesto."
        elif formato_key == "INSIGHT_DE_CORRETOR": return base_instruction + "\n- Use Primeira Pessoa (Eu/Nós). Conte bastidores."
        else: return base_instruction

    def _get_tone_guidelines(self, gatilho_key):
        if gatilho_key == "NEUTRAL_JOURNALISM":
            return "### 🧠 MENTALIDADE (JORNALISMO)\n- Escreva MUITO. Profundidade e Contexto. Proibido textos rasos."
        else:
            return "### 🧠 MENTALIDADE (COPYWRITING)\n- Texto longo e envolvente. Gatilhos mentais e Storytelling."

    def build(self, d, data_pub, data_mod, regras_texto_ajustada):
        if d.get('tipo_pauta') == "PORTAL":
            return self._build_portal_prompt(d, data_pub, data_mod, regras_texto_ajustada)
        else:
            return self._build_real_estate_prompt(d, data_pub, data_mod, regras_texto_ajustada)

    def _build_portal_prompt(self, d, data_pub, data_mod, regras_texto_ajustada):
        # ⚠️ AQUI ESTÁ A GARANTIA DO FUSO DE BRASÍLIA
        # O argumento data_mod já deve vir com o fuso correto do app.py, mas reforçamos a formatação
        
        data_fmt = self._format_date_blogger(data_pub)
        formato_key = d.get('formato', 'NOTICIA_IMPACTO')
        editoria = d.get('ativo_definido', 'Geral')
        tema = d.get('topico', 'Geral')
        
        structure_guide = self._get_portal_structure(formato_key, editoria, tema)
        tone_guide = self._get_tone_guidelines("NEUTRAL_JOURNALISM")
        
        return f"""
## GENESIS MAGNETO V.64 — PORTAL NEWS ENGINE (LONGFORM)
**Objetivo:** JORNALISMO LOCAL DE PROFUNDIDADE (5-10 MINUTOS DE LEITURA).
**Persona:** PORTAL DA CIDADE (Editor-Chefe).
**Timestamp:** {data_mod} (Horário de Brasília)

## 1. A PAUTA
- **EDITORIA:** {editoria}
- **TEMA:** {tema}
- **LOCAL:** Indaiatuba (Cidade Inteira)
- **FORMATO:** {formato_key}

## 2. MISSÃO JORNALÍSTICA
Você é um repórter sênior. EXPANDA CADA TÓPICO.
- **Dados:** Use dados reais (busque fatos recentes de Indaiatuba). 
- **Busca:** Se for "Resumo do Dia", A BUSCA É OBRIGATÓRIA (considere o fuso de Brasília).

{structure_guide}

{tone_guide}

## 3. INSUMOS (FILTRO COGNITIVO)
**DIRETRIZ SUPREMA:**
1. IGNORAR a persona de Vendas/Imobiliária.
2. ENCARNAR a persona de JORNALISTA SÊNIOR.
3. Foco: Verdade, Detalhe e Utilidade Pública.

<REGRAS_DO_SISTEMA>
{regras_texto_ajustada}
</REGRAS_DO_SISTEMA>

## 4. CTA
{self.CTA_CAPTURE_CODE}

## 5. CHECKLIST FINAL
1. TÍTULO (H1)
2. LIDE
3. CONTEÚDO (H2/H3)
4. JSON-LD: Schema 'NewsArticle'.
5. MARCADORES: {self._generate_seo_tags(d)}
""".strip()

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
## GENESIS MAGNETO V.64 — REAL ESTATE (UNCHAINED)
**Objetivo:** Copywriting Imobiliário Persuasivo e Extenso.
**Persona:** IMOBILIÁRIA SABER.
**Timestamp:** {data_mod} (Horário de Brasília)

## 1. O CENÁRIO
- **ATIVO:** {ativo}
- **LOCAL:** {bairro_nome}
- **CLIENTE:** {d['persona']['nome']}
- **FORMATO:** {formato}
- **GATILHO:** {gatilho}

## 2. CARTA DE ALFORRIA
Escreva um texto rico, longo e detalhado. Venda o sonho com profundidade.
{structure}
{tone}

## 3. INSUMOS (FILTRO COGNITIVO)
**DIRETRIZ SUPREMA:**
1. IGNORAR a persona de Jornalismo.
2. ENCARNAR a persona de CORRETOR ESPECIALISTA.

<REGRAS_DO_SISTEMA>
{regras_texto_ajustada}
</REGRAS_DO_SISTEMA>

## 4. CTA
{self.CTA_CAPTURE_CODE}

## 5. CHECKLIST FINAL
1. TÍTULO (H1)
2. CONTEÚDO
3. MARCADORES: {self._generate_seo_tags(d)}
4. JSON-LD: Schema 'BlogPosting'.
""".strip()
