import streamlit as st
import random
import datetime
import json
import urllib.request
import ssl
import re
import os

# ==============================================================================
# GENESIS AGENCY CORE – V10.2 (FIXED JSON-LD + DATA BLOGGER)
# ==============================================================================

class AgencyConfig:
    VERSION = "GENESIS 10.2 (BLOGGER DATA + JSON SAFE)"
    BLOG_URL = "https://blog.saber.imb.br"
    FUSO_PADRAO = "-03:00"

    LEAD_SCRIPT = '<div style="text-align:center; margin: 40px 0;"><script async data-uid="d188d73e78" src="https://sabernovidades.kit.com/d188d73e78/index.js"></script></div>'

    LOGO_URL = "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEixiE1KghKkH0E-I53yyi5zoT7eRX0lxCGLpcWLGAmEE5st8OfHfuzbxfiygwCWRqAdSfpmjAhM8-SogHDU_1gXCX6IHrjW1BaUc87un1lF1o6y2Et7eV0m3gJgvfJs3HsAGyAcPYk8Tl_65rlQmgAp5orRZqtLDvixbCUwscTT8ZJO-7zckc36rNkWHz4/s1600/1000318124.png"

    REGRAS_TECNICAS = """
### ⛔ PROTOCOLO TÉCNICO DE SEGURANÇA (OBRIGATÓRIO)
Você está gerando um FRAGMENTO DE HTML para ser inserido dentro de um post do Blogger.
I. **PROIBIDO** usar: `<!DOCTYPE html>`, `<html>`, `<head>`, `<body>`.
II. **PROIBIDO** incluir tags `<meta>` ou `<title>`.
III. Comece DIRETAMENTE com o conteúdo visível (ex: `<style>`, `<h2>`, `<p>`, `<div>`).
IV. A violação destas regras quebrará o template do site.
"""

    REGRAS_TABELA = """
### 🎨 REGRAS DE DESIGN DE TABELAS (ANTI-QUEBRA)
Para garantir leitura mobile, siga este CSS Inline RIGOROSAMENTE:
1. **Wrapper:** Envolva a tabela em `<div style="overflow-x: auto; width: 100%; margin-bottom: 20px;">`.
2. **Tag Table:** Use `<table style="width: 100%; min-width: 600px; border-collapse: collapse;">`.
3. **Células (TH/TD):** EM TODAS AS CÉLULAS, aplique: 
   `style="padding: 12px; border: 1px solid #cccccc; word-break: keep-all; hyphens: none;"`
"""

    # JSON-LD base (será preenchido com data)
    @staticmethod
    def get_json_ld(iso_date):
        return f'''<script type="application/ld+json">
{{
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    "headline": "INSIRA O TITULO H1 AQUI",
    "datePublished": "{iso_date}",
    "dateModified": "{datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S-03:00')}",
    "author": {{ "@type": "Organization", "name": "Imobiliária Saber" }},
    "publisher": {{
        "@type": "Organization",
        "name": "Imobiliária Saber",
        "logo": {{ "@type": "ImageObject", "url": "{AgencyConfig.LOGO_URL}" }}
    }}
}}
</script>'''

# ==============================================================================
# Função auxiliar – formatação de data para Blogger (DD de mmm. de AAAA)
# ==============================================================================
def formatar_data_blogger(dt):
    meses = ["", "jan.", "fev.", "mar.", "abr.", "mai.", "jun.",
             "jul.", "ago.", "set.", "out.", "nov.", "dez."]
    return f"{dt.day:02d} de {meses[dt.month]} de {dt.year}"

# ==============================================================================
# GERAÇÃO DO PROMPT (usando .format para evitar erro de f-string)
# ==============================================================================
def gerar_prompt(persona, bairro, estrategia, data_pub):
    date_fmt = formatar_data_blogger(data_pub)
    iso_date = data_pub.strftime(f"%Y-%m-%dT09:00:00{AgencyConfig.FUSO_PADRAO}")

    json_ld_block = AgencyConfig.get_json_ld(iso_date)

    template = """
# 🛑 ZONA DE SEGURANÇA MÁXIMA – NÃO ALTERAR NADA ABAIXO

{regras_tecnicas}

{regras_tabela}

## INSTRUÇÃO CRÍTICA SOBRE JSON-LD
NÃO modifique, reescreva, altere indentação ou qualquer caractere do bloco JSON-LD abaixo.
Copie e cole EXATAMENTE como está, no INÍCIO do BLOCKCODE HTML.

**BLOCO JSON-LD OBRIGATÓRIO (não mexa):**
{json_ld}

## CHECKLIST DE ENTREGA – ORDEM IMUTÁVEL (não mude a sequência)
Sua resposta final deve conter EXATAMENTE:

1. LOG DE BASTIDORES: (estratégia usada, locais reais simulando Google Maps)
2. BLOCKCODE: (HTML puro + JSON-LD acima + conteúdo do artigo)
   - Comece diretamente com <style>, <h1>, <h2>, <p>, <div>...
   - NUNCA inclua <!DOCTYPE html>, <html>, <head>, <body>, <meta>, <title>
   - No FINAL do artigo, inclua obrigatoriamente:
     {lead_script}
3. TÍTULO: (apenas o texto do H1, sem aspas)
4. MARCADORES: (separados por vírgula)
5. DATA: {data_fmt}
6. LOCAL: Indaiatuba
7. DESCRIÇÃO: (meta description curta, focada na dor)
8. IMAGEM: (prompt para geração de imagem)

## Briefing Estratégico
Persona: {persona_nome}
Dor principal: {dor}
Local: {bairro_nome} ({zona})
Ativo foco: {ativo}
Gatilho: {gatilho_nome} – {gatilho_desc}
Entidades semânticas: {semantica}

## Regras obrigatórias
- Use APENAS locais REAIS de Indaiatuba (simule busca no Google Maps)
- Distâncias em minutos realistas
- NUNCA invente depoimentos com nomes de pessoas
- Evite palavras proibidas: sonho, sonhos, oportunidade única, excelente localização, ótimo investimento, preço imperdível, lindo, maravilhoso, tranquilo, localização privilegiada

Gere o conteúdo seguindo rigorosamente a ordem acima.
"""

    return template.format(
        regras_tecnicas=AgencyConfig.REGRAS_TECNICAS.strip(),
        regras_tabela=AgencyConfig.REGRAS_TABELA.strip(),
        json_ld=json_ld_block,
        lead_script=AgencyConfig.LEAD_SCRIPT,
        data_fmt=date_fmt,
        persona_nome=persona.get("nome", "Persona não definida"),
        dor=persona.get("dor", "")[:100],
        bairro_nome=bairro.get("nome", "Bairro não definido"),
        zona=bairro.get("zona", ""),
        ativo=estrategia.get("ativo", "Ativo não definido"),
        gatilho_nome=estrategia.get("gatilho_nome", ""),
        gatilho_desc=estrategia.get("gatilho_desc", ""),
        semantica=", ".join(estrategia.get("cluster_semantic", []))
    )

# ==============================================================================
# INTERFACE STREAMLIT (mínima – expanda conforme necessário)
# ==============================================================================
def main():
    st.set_page_config(page_title="Genesis 10.2 – Blogger Ready", layout="wide")

    st.title("Genesis Agency v10.2")
    st.caption("Formato de data corrigido para Blogger + JSON-LD seguro")

    # Exemplo de valores (substitua pela sua lógica real de seleção)
    persona_exemplo = {"nome": "Família Êxodo Urbano", "dor": "Medo da violência e trânsito caótico em São Paulo"}
    bairro_exemplo = {"nome": "Jardim Monte Belo", "zona": "residencial_fechado"}
    estrategia_exemplo = {
        "ativo": "Casa em Condomínio Fechado",
        "gatilho_nome": "CONTRASTE_DOR",
        "gatilho_desc": "Comparar o caos de SP com a tranquilidade do interior",
        "cluster_semantic": ["Segurança Monitorada", "Parque Ecológico", "Escolas de ponta"]
    }

    data_pub = st.date_input("Data de publicação", datetime.date.today())

    if st.button("Gerar Prompt"):
        with st.spinner("Gerando prompt..."):
            prompt = gerar_prompt(persona_exemplo, bairro_exemplo, estrategia_exemplo, data_pub)

        st.subheader("Prompt para IA (copie e cole)")
        st.code(prompt, language="markdown")

        st.download_button(
            label="Baixar .txt",
            data=prompt,
            file_name=f"prompt_{data_pub.strftime('%Y%m%d')}_{bairro_exemplo['nome'].replace(' ', '_')}.txt",
            mime="text/plain"
        )

if __name__ == "__main__":
    main()