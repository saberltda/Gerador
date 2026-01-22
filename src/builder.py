# src/builder.py
import datetime
import json
from .config import GenesisConfig

class PromptBuilder:
    """
    O 'Redator' (Versão 62 - Longform News Edition).
    Focado em RETENÇÃO DE LEITURA (5 a 10 minutos).
    Transforma 'Resumos' em 'Revistas Digitais Completas'.
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
            tags = ["Indaiatuba", "Notícias Indaiatuba", "Portal da Cidade", "Giro de Notícias", "Aconteceu em Indaiatuba"]
        else:
            tags = ["Indaiatuba", "Imóveis Indaiatuba", "Mercado Imobiliário", "Morar em Indaiatuba"]

        # 2. Injeção de Localização
        if d.get('bairro') and d['bairro']['nome'] != "Indaiatuba":
            tags.append(d['bairro']['nome'])
        
        # 3. Injeção de Ativo/Editoria (Limpo)
        raw_ativo = d.get('ativo_definido', '')
        ativo_limpo = raw_ativo.split('(')[0].strip()
        if ativo_limpo: tags.append(ativo_limpo)
        
        # 4. Injeção de Tópico
        if d.get('topico'): tags.append(d['topico'])
        
        # 5. Deduplicação
        seen = set()
        final_tags = [x for x in tags if not (x in seen or seen.add(x))]
        
        return ", ".join(final_tags[:10])

    def _get_portal_structure(self, formato_key, editoria, tema):
        
        # --- LÓGICA ESPECIAL: GIRO LONGO (5-10 MINUTOS DE LEITURA) ---
        if "Resumo" in editoria or "Notícias" in editoria:
            return f"""
## 5. ESTRUTURA: REVISTA DIGITAL DIÁRIA (LONGFORM)
**OBJETIVO:** Prender o leitor por 10 minutos. NADA DE TEXTO CURTO.
Você deve agir como o Editor-Chefe de um jornal matinal completo.

**ORDEM DE EXECUÇÃO:**
1. **Varredura Completa:** Busque TUDO o que é relevante hoje em Indaiatuba (Segurança, Política, Obras, Eventos, Clima).
2. **Seleção:** Escolha os 4 ou 5 temas mais quentes.

**ESTRUTURA DO TEXTO (OBRIGATÓRIA):**

**MANCHETE DE CAPA:** (Impactante e Local)

**1. A NOTÍCIA PRINCIPAL (O DESTAQUE)**
- Não faça apenas um parágrafo. Escreva uma **MATÉRIA COMPLETA** sobre o assunto principal do dia.
- O que aconteceu? Por que é importante? Quem disse o quê? Qual o histórico?
- *Mínimo de 4 parágrafos robustos neste bloco.*

**2. O GIRO PELA CIDADE (3 a 4 Sub-Manchetes)**
- Para cada notícia secundária, use um H3.
- Escreva pelo menos 2 parágrafos detalhados para cada notícia. 
- *Proibido:* Usar listas simples de bullet points. Desenvolva o texto.

**3. COLUNA SOCIAL & EVENTOS**
- O que vai acontecer hoje/amanhã? (Cinema, Parque Ecológico, Shows).
- Dê detalhes: Horários, Preços, Onde fica.

**4. SERVIÇO DE UTILIDADE PÚBLICA**
- **Previsão do Tempo Detalhada:** (Manhã, Tarde, Noite, Chuva, Vento).
- **Trânsito:** Onde evitar hoje?
- **Plantão:** Farmácias ou Telefones úteis.

**5. A IMAGEM DO DIA**
- Descreva uma cena cotidiana de Indaiatuba que represente o dia de hoje (texto descritivo e poético).

*Tom de Voz:* Jornalístico, Profundo, Analítico e Comunitário.
"""

        # 1. EXPLAINER (Jornalismo Didático)
        if formato_key == "EXPLAINER":
            return f"""
## 5. ESTRUTURA: EXPLAINER (ENTENDA O CASO A FUNDO)
O leitor quer uma aula sobre "{tema}".
- **Intro:** O fato (1 parágrafo).
- **A Linha do Tempo:** Explique a história cronológica do problema.
- **Os Detalhes Técnicos:** Aprofunde-se nos números, leis ou causas.
- **O Impacto Real:** Como isso muda a vida do morador de Indaiatuba hoje.
- **Conclusão:** O que esperar para os próximos meses.
*Meta:* Texto denso e educativo.
"""

        # 2. DOSSIÊ INVESTIGATIVO (Profundidade)
        elif formato_key == "DOSSIE_INVESTIGATIVO":
            return f"""
## 5. ESTRUTURA: DOSSIÊ INVESTIGATIVO (LONGFORM)
Uma análise profunda e extensa sobre {editoria}.
- **Manchete Impactante.**
- **O Problema:** Dados e fatos que mostram a dimensão da questão.
- **As Causas Raiz:** Por que isso acontece? (Análise sociológica/urbana).
- **O Contraponto:** O que dizem as autoridades, especialistas e opositores.
- **Vozes da Cidade:** Histórias reais e citações de quem é afetado.
*Meta:* Texto de referência. O mais completo da internet sobre o assunto.
"""

        # 3. CHECAGEM DE FATOS (Fact-Checking)
        elif formato_key == "CHECAGEM_FATOS":
            return f"""
## 5. ESTRUTURA: CHECAGEM DE FATOS DETALHADA
Vamos investigar a fundo o boato sobre "{tema}".
- **O Contexto:** Onde surgiu? Quem compartilhou? Por que viralizou?
- **A Investigação Passo a Passo:** Detalhe como a checagem foi feita (fomos até lá, ligamos, consultamos a lei).
- **As Evidências:** Transcreva documentos, cite leis, descreva fotos.
- **Veredito:** VERDADE, MENTIRA ou ENGANOSO? (Com justificativa longa).
"""

        # 4. LISTA DE CURADORIA (Serviço/Lazer)
        elif formato_key == "LISTA_CURADORIA":
            return f"""
## 5. ESTRUTURA: GUIA COMPLETO (CURADORIA)
Não apenas uma lista, mas um roteiro comentado sobre {editoria}.
- **Intro:** A cultura desse tema em Indaiatuba.
- **Os Escolhidos (Top 5 a 7):**
  - Para cada item: Nome, Endereço Completo, Faixa de Preço.
  - **A Resenha:** 2 parágrafos descrevendo a experiência, o ambiente e o diferencial.
- **Dica de Insider:** O prato secreto, o melhor horário, onde estacionar.
"""

        # 5. SERVIÇO PASSO A PASSO
        elif formato_key == "SERVICO_PASSO_A_PASSO":
            return f"""
## 5. ESTRUTURA: MANUAL DO CIDADÃO
Guia exaustivo para resolver ({tema}).
- **Introdução:** Quem precisa disso e prazos.
- **Documentação:** Lista detalhada (original e cópia, validade, etc).
- **O Procedimento:** Passo 1, Passo 2... com detalhes de "o que fazer se der errado".
- **Onde Ir:** Endereços, mapas mentais, horários de pico para evitar.
"""

        # 6. HARD NEWS (Notícia Padrão)
        elif formato_key == "NOTICIA_IMPACTO":
            return f"""
## 5. ESTRUTURA: HARD NEWS COMPLETA
Notícia quente, mas com contexto.
- **Lide:** Resumo completo no topo.
- **Desenvolvimento:** Detalhes da ocorrência.
- **Histórico:** Isso é recorrente? Dados de anos anteriores.
- **Repercussão:** O que os vizinhos/comunidade estão dizendo.
- **Serviço:** O que fazer agora?
"""

        # 7. ENTREVISTA PING-PONG
        elif formato_key == "ENTREVISTA_PING_PONG":
            return f"""
## 5. ESTRUTURA: A GRANDE ENTREVISTA
Conversa profunda com uma personalidade local sobre {tema}.
- **Perfil:** Quem é o entrevistado? (Biografia breve).
- **A Entrevista:** Perguntas complexas e respostas completas (mantenha a oralidade, mas expanda o contexto se necessário).
- **Bastidores:** Como foi o encontro? Onde ocorreu?
"""

        else:
            return "## 5. ESTRUTURA LIVRE (LONGFORM)\nDesenvolva uma matéria jornalística extensa, visando 10 minutos de leitura."

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
### 🧠 MENTALIDADE DE ESCRITOR (JORNALISMO PROFUNDO)
- **Extensão:** Escreva MUITO. O leitor quer detalhes.
- **Proibido:** Textos rasos, resumos rápidos ou "notas".
- **Missão:** Informar com profundidade e contexto.
"""
        else:
            return """
### 🧠 MENTALIDADE DE ESCRITOR (COPYWRITING IMERSIVO)
- **Extensão:** Texto longo e envolvente.
- **Conexão:** Use gatilhos mentais e storytelling para prender a atenção.
"""

    def build(self, d, data_pub, data_mod, regras_texto_ajustada):
        if d.get('tipo_pauta') == "PORTAL":
            return self._build_portal_prompt(d, data_pub, data_mod, regras_texto_ajustada)
        else:
            return self._build_real_estate_prompt(d, data_pub, data_mod, regras_texto_ajustada)

    # =========================================================================
    # MODO PORTAL (LONGFORM NEWS)
    # =========================================================================
    def _build_portal_prompt(self, d, data_pub, data_mod, regras_texto_ajustada):
        data_fmt = self._format_date_blogger(data_pub)
        formato_key = d.get('formato', 'NOTICIA_IMPACTO')
        editoria = d.get('ativo_definido', 'Geral')
        tema = d.get('topico', 'Geral')
        
        structure_guide = self._get_portal_structure(formato_key, editoria, tema)
        tone_guide = self._get_tone_guidelines("NEUTRAL_JOURNALISM")
        
        return f"""
## GENESIS MAGNETO V.62 — PORTAL NEWS ENGINE (LONGFORM)
**Objetivo:** JORNALISMO LOCAL DE PROFUNDIDADE (5-10 MINUTOS DE LEITURA).
**Persona:** PORTAL DA CIDADE (Editor-Chefe).

## 1. A PAUTA
- **EDITORIA:** {editoria}
- **TEMA:** {tema}
- **LOCAL:** Indaiatuba (Cidade Inteira)
- **FORMATO:** {formato_key}

## 2. MISSÃO JORNALÍSTICA
Você é um repórter sênior. Seu chefe proibiu "notinhas".
- **Regra de Ouro:** EXPANDA CADA TÓPICO. Se for falar de trânsito, explique as ruas. Se for falar de clima, dê a previsão completa.
- **Dados:** Use dados reais (busque fatos recentes de Indaiatuba). Se for "Resumo do Dia", a busca é OBRIGATÓRIA.
- **Engajamento:** O texto deve ser tão completo que o leitor não precise sair da página para saber mais.

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

## 4. CTA (NEWSLETTER)
{self.CTA_CAPTURE_CODE}

## 5. CHECKLIST FINAL
1. TÍTULO (H1): Manchete forte e clara.
2. LIDE: Resumo de alta densidade informativa.
3. CONTEÚDO: Longo, dividido em H2 e H3, com parágrafos bem desenvolvidos.
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
## GENESIS MAGNETO V.62 — REAL ESTATE (UNCHAINED)
**Objetivo:** Copywriting Imobiliário Persuasivo e Extenso.
**Persona:** IMOBILIÁRIA SABER.

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
3. Foco: Encantamento e Venda Técnica.

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
