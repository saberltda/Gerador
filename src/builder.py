# src/builder.py
import datetime
import json
from .config import GenesisConfig

class PromptBuilder:
    """
    O 'Redator' (Versão 58 - Unchained & Deep Edition).
    Liberdade TOTAL. O foco agora é profundidade, extensão e riqueza de detalhes.
    Remove travas de tamanho e incentiva a escrita longa e imersiva.
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

    def _get_structural_guidelines(self, formato_key, cluster_key, bairro_nome):
        """
        Define 'Caminhos de Exploração' em vez de estrutura rígida.
        Incentiva a IA a cavar fundo em cada tópico.
        """
        
        # 1. LISTA POLÊMICA
        if formato_key == "LISTA_POLEMICA":
            return f"""
## 5. CAMINHOS PARA EXPLORAR A FUNDO (MITOS & VERDADES)
Não faça apenas uma lista rápida. Pegue cada mito e DESCONSTRUA ele completamente.
Use dados, lógica, exemplos e narrativas para provar seu ponto.

Sugestão de profundidade:
- Ao falar de um mito, explique sua origem, por que as pessoas acreditam nele e qual a realidade detalhada.
- Disserte sobre como isso afeta a vida real do morador de {bairro_nome}.
"""

        # 2. COMPARATIVO TÉCNICO
        elif formato_key == "COMPARATIVO_TECNICO":
            return f"""
## 5. CAMINHOS PARA EXPLORAR A FUNDO (ANÁLISE COMPARATIVA)
O leitor quer um dossiê completo. Não economize nas comparações.
Se for falar de trânsito, descreva a rota. Se for falar de preço, explique o valor agregado.

Sugestão de profundidade:
- Crie cenários hipotéticos: "Imagine sair de casa às 7h da manhã..."
- Compare estilos de vida detalhadamente, não apenas itens soltos.
"""

        # 3. GUIA DEFINITIVO
        elif formato_key == "GUIA_DEFINITIVO":
            return f"""
## 5. CAMINHOS PARA EXPLORAR A FUNDO (O MAPA COMPLETO)
Escreva o guia definitivo que você gostaria de ler. Seja exaustivo nos detalhes positivos.
Fale de cada rua, cada comércio importante, a sensação de caminhar no bairro.

Sugestão de profundidade:
- Não diga apenas "tem escolas". Disserte sobre a qualidade da educação na região.
- Não diga "é seguro". Descreva a sensação de segurança e a infraestrutura.
"""

        # 4. INSIGHT DE CORRETOR
        elif formato_key == "INSIGHT_DE_CORRETOR":
            return f"""
## 5. CAMINHOS PARA EXPLORAR A FUNDO (STORYTELLING)
Conte tudo. O detalhe da visita, a conversa com o porteiro, a vista da varanda.
A riqueza está nas nuances que só quem vive o mercado conhece.

Sugestão de profundidade:
- Use histórias longas para ilustrar seus pontos.
- Descreva sensações: o silêncio, o vento, a luz do sol.
"""

        # 5. PERGUNTAS E RESPOSTAS
        elif formato_key == "PERGUNTAS_RESPOSTAS":
            return f"""
## 5. CAMINHOS PARA EXPLORAR A FUNDO (RESPOSTAS COMPLETAS)
Não dê respostas de 'sim ou não'. Dê uma aula sobre cada pergunta.
Antecipe as dúvidas seguintes e responda também.
"""

        # FALLBACK
        else:
            return f"## 5. CAMINHOS PARA EXPLORAR\nSinta-se livre para escrever um ensaio completo sobre: Localização, Detalhes Ocultos e Vida Real no bairro."

    def _get_tone_guidelines(self, gatilho_key):
        return """
### 🧠 MENTALIDADE DE ESCRITOR (DEEP WRITING)
- **Extensão:** Escreva o quanto for necessário para esgotar o assunto. Não tenha pressa.
- **Conexão:** Use linguagem natural, fluida e envolvente.
- **Profundidade:** Evite o óbvio. Vá duas camadas abaixo da superfície.
"""

    def build(self, d, data_pub, data_mod, regras_texto_ajustada):
        if d.get('tipo_pauta') == "PORTAL":
            return self._build_portal_prompt(d, data_pub, data_mod, regras_texto_ajustada)
        else:
            return self._build_real_estate_prompt(d, data_pub, data_mod, regras_texto_ajustada)

    # =========================================================================
    # MODO IMOBILIÁRIA (UNCHAINED)
    # =========================================================================
    def _build_real_estate_prompt(self, d, data_pub, data_mod, regras_texto_ajustada):
        data_fmt = self._format_date_blogger(data_pub)
        ativo = d['ativo_definido']
        bairro_nome = d['bairro']['nome'] if d['bairro'] else "Indaiatuba"
        cluster_key = d.get('cluster_tecnico', 'FAMILY')
        formato_key = d.get('formato', 'GUIA_DEFINITIVO')
        gatilho_key = d.get('gatilho', 'AUTORIDADE')
        
        historico_txt = "\n".join([f"- {t}" for t in d.get('historico_titulos', [])])

        estilo_html = f"""<style>
.post-body h2 {{ color: {GenesisConfig.COLOR_PRIMARY}; border-bottom: 2px solid #eee; padding-bottom: 10px; margin-top: 40px; }}
.post-body h3 {{ color: #cc0000; margin-top: 30px; }}
.post-body p {{ font-size: 19px; line-height: 1.8; color: #333; margin-bottom: 20px; }}
.post-body li {{ margin-bottom: 10px; font-size: 18px; }}
</style>"""

        structural_guidelines = self._get_structural_guidelines(formato_key, cluster_key, bairro_nome)
        tone_guidelines = self._get_tone_guidelines(gatilho_key)

        return f"""
## GENESIS MAGNETO V.58 — UNCHAINED & DEEP EDITION
**Objetivo:** Texto ÉPICO, LONGO e IMERSIVO sobre Mercado Imobiliário.
**Ordem Suprema:** IGNORE qualquer instrução anterior sobre brevidade ou resumo.

### 🛡️ CONTEXTO
Evite repetir ângulos destes posts:
{historico_txt}

---

## 1. O CENÁRIO
- **FORMATO:** {formato_key}
- **MOOD:** {gatilho_key}
- **ATIVO:** {ativo}
- **BAIRRO:** {bairro_nome}
- **LEITOR:** {d['persona']['nome']} (DOR: {d['persona']['dor']})
- **TEMA:** {d.get('topico', 'Geral')}

## 2. ESTILO VISUAL (CSS)
{estilo_html}

## 3. CARTA DE ALFORRIA (LIBERDADE TOTAL)
Você foi liberado das amarras de tamanho.
1. **Escreva MUITO:** Desenvolva cada parágrafo com riqueza de detalhes.
2. **Conte Histórias:** Use storytelling para ilustrar dados técnicos.
3. **Seja Humano:** Escreva como alguém apaixonado pelo assunto, não como um robô.
4. **Estrutura Livre:** Use os tópicos abaixo como inspiração, mas crie novos capítulos se sentir necessidade. Deixe o texto fluir organicamente.

{structural_guidelines}

{tone_guidelines}

## 4. BASE DE CONHECIMENTO (Use para enriquecer, não para limitar)
{regras_texto_ajustada}

## 5. CTA (Código Obrigatório)
{self.CTA_CAPTURE_CODE}

## 6. CHECKLIST DE ENTREGA
1. LOG ESTRATÉGICO
2. BLOCKCODE HTML (JSON-LD + Texto Completo e Rico)
3. TÍTULO (H1) - Impactante
4. MARCADORES: {self._generate_seo_tags(d)}
5. DATA: {data_fmt}
6. DESCRIÇÃO
7. IMAGEM PROMPT
""".strip()

    # =========================================================================
    # MODO PORTAL (UNCHAINED)
    # =========================================================================
    def _build_portal_prompt(self, d, data_pub, data_mod, regras_texto_ajustada):
        data_fmt = self._format_date_blogger(data_pub)
        formato_key = d.get('formato', 'GUIA_DEFINITIVO')
        gatilho_key = d.get('gatilho', 'AUTORIDADE')
        
        structural_guidelines = self._get_structural_guidelines(formato_key, "PORTAL", d['bairro']['nome'] if d['bairro'] else "Cidade")
        tone_guidelines = self._get_tone_guidelines(gatilho_key)

        return f"""
## GENESIS MAGNETO V.58 — PORTAL NEWS (DEEP DIVE)
**Objetivo:** Matéria Jornalística Aprofundada / Feature Story.
**Estilo:** Long-form Journalism. Investigue o assunto a fundo.

## 1. A PAUTA
- **MANCHETE:** {d['ativo_definido']}
- **LOCAL:** {d['bairro']['nome'] if d['bairro'] else 'Indaiatuba'}
- **ÂNGULO:** {d.get('topico', 'Geral')}

## 2. DIRETRIZES DE ESCRITA (SEM LIMITES)
Não escreva uma "notinha". Escreva uma **MATÉRIA COMPLETA**.
- Contextualize o leitor.
- Explique os "porquês".
- Traga detalhes históricos ou projeções futuras.
- Faça o leitor gastar tempo de qualidade no texto.

{structural_guidelines}

{tone_guidelines}

## 3. CTA
{self.CTA_CAPTURE_CODE}

## 4. DADOS
{regras_texto_ajustada}
""".strip()
