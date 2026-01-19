import streamlit as st
import random
import datetime
import json
import urllib.request
import ssl
import re
import unicodedata

# ==============================================================================
# 💎 GENESIS APP V.10.1 (SYNTAX SHIELD FIX)
# Correção crítica de aspas e quebra de blockcode
# ==============================================================================

class GenesisConfig:
    VERSION = "GENESIS V.10.1 (SAFE MODE)"
    BLOG_URL = "[https://blog.saber.imb.br](https://blog.saber.imb.br)"
    FEED_URL = "[https://blog.saber.imb.br/feeds/posts/default?alt=json&max-results=50](https://blog.saber.imb.br/feeds/posts/default?alt=json&max-results=50)"
    
    # Script de captura [REGRAS.txt]
    LEAD_SCRIPT = '<div style="text-align:center; margin: 40px 0;"><script async data-uid="d188d73e78" src="[https://sabernovidades.kit.com/d188d73e78/index.js](https://sabernovidades.kit.com/d188d73e78/index.js)"></script></div>'
    
    THEME = {
        "primary": "#003366", 
        "accent": "#28a745",
        "bg": "#f4f6f9"
    }

    PERSONAS = {
        "EXODUS_SP": {
            "nome": "Família em Êxodo Urbano",
            "cluster_ref": "FAMILY",
            "dor": "Medo da violência e trânsito caótico de SP. Infância confinada.",
            "desejo": "Quintal, segurança de condomínio, escolas fortes e 'pé na grama'.",
            "zonas_alvo": ["residencial_fechado", "chacaras_fechado"]
        },
        "INVESTOR_ROI": {
            "nome": "Investidor Analítico (Shark)",
            "cluster_ref": "INVESTOR",
            "dor": "Medo da inflação corroendo patrimônio e vacância de imóveis.",
            "desejo": "Rentabilidade real, liquidez rápida e vetor de crescimento urbano.",
            "zonas_alvo": ["mista", "residencial_fechado", "industrial", "residencial_aberto"]
        },
        "REMOTE_WORKER": {
            "nome": "Profissional Home Office",
            "cluster_ref": "FAMILY",
            "dor": "Apartamento apertado sem isolamento acústico para calls.",
            "desejo": "Cômodo extra (Office), silêncio absoluto e vista livre.",
            "zonas_alvo": ["residencial_fechado", "chacaras_fechado"]
        },
        "HYBRID_COMMUTER": {
            "nome": "O Pendular (SP-Indaiatuba)",
            "cluster_ref": "URBAN",
            "dor": "Cansaço da estrada e tempo perdido no trânsito urbano.",
            "desejo": "Acesso imediato à Rodovia SP-75 e serviços rápidos (padaria/mercado).",
            "zonas_alvo": ["residencial_aberto", "mista"]
        },
        "LUXURY_SEEKER": {
            "nome": "Buscador de Exclusividade",
            "cluster_ref": "HIGH_END",
            "dor": "Falta de privacidade e padronização excessiva das construtoras.",
            "desejo": "Arquitetura autoral, terrenos duplos, lazer privativo e status.",
            "zonas_alvo": ["residencial_fechado", "chacaras_fechado"]
        },
        "LOGISTICS_MANAGER": {
            "nome": "Gestor Logístico/Industrial",
            "cluster_ref": "LOGISTICS",
            "dor": "Custo logístico (Last Mile) e falta de área de manobra.",
            "desejo": "Galpão funcional, pé direito alto, docas e acesso a Viracopos.",
            "zonas_alvo": ["industrial"]
        }
    }

    CONTENT_FORMATS = [
        "GUIA_DEFINITIVO (Técnico e Completo)", 
        "LISTA_POLEMICA (Desafiando Mitos)", 
        "COMPARATIVO_TECNICO (Prós e Contras)", 
        "CENARIO_ANALITICO (Estudo de Caso Hipotético)", 
        "CHECKLIST_TECNICO (Passo a Passo)", 
        "DATA_DRIVEN (Focado em Números/Distâncias)"
    ]

# =========================================================
# 📡 BLOG SCANNER
# =========================================================

class BlogScanner:
    def __init__(self):
        self.feed_url = GenesisConfig.FEED_URL
        self.bairros_publicados = set()
        self.status = "Inativo"

    def slugify(self, texto):
        if not texto: return ""
        texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
        texto = texto.lower()
        texto = re.sub(r'[^a-z0-9]', '', texto)
        return texto

    def run_scan(self):
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            
            with urllib.request.urlopen(self.feed_url, context=ctx, timeout=4) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode())
                    count = 0
                    if "feed" in data and "entry" in data["feed"]:
                        for entry in data["feed"]["entry"]:
                            titulo = entry["title"]["$t"]
                            self.bairros_publicados.add(self.slugify(titulo))
                            count += 1
                    self.status = f"Online ({count} posts indexados)"
                    return True
        except Exception:
            self.status = "Offline (Seguindo sem histórico)"
            return False
        return False

    def is_fresh(self, nome_bairro):
        return self.slugify(nome_bairro) not in self.bairros_publicados

# =========================================================
# 🧠 BRAIN LOGIC
# =========================================================

class GenesisBrain:
    def __init__(self):
        self.bairros = self._load_bairros()
        self.scanner = BlogScanner()

    def _load_bairros(self):
        try:
            with open("bairros.json", "r", encoding="utf-8") as f:
                raw = json.load(f)
            processed = []
            for b in raw:
                z = b.get('zona', '').lower()
                if "industrial" in z or "empresarial" in z: zn = "industrial"
                elif "chácara" in z and "fechado" in z: zn = "chacaras_fechado"
                elif "chácara" in z: zn = "chacaras_aberto"
                elif "fechado" in z: zn = "residencial_fechado"
                elif "mista" in z: zn = "mista"
                else: zn = "residencial_aberto"
                b['zona_norm'] = zn
                processed.append(b)
            return processed
        except:
            return [{"nome": "Jardim Pau Preto", "zona": "Residencial", "zona_norm": "residencial_aberto"}]

    def generate_strategy(self, use_scanner=True):
        if use_scanner: self.scanner.run_scan()

        p_key = random.choice(list(GenesisConfig.PERSONAS.keys()))
        persona = GenesisConfig.PERSONAS[p_key]

        candidatos = [b for b in self.bairros if b['zona_norm'] in persona['zonas_alvo']]
        
        if use_scanner:
            ineditos = [b for b in candidatos if self.scanner.is_fresh(b['nome'])]
            if ineditos:
                candidatos = ineditos
                scan_result = "✅ Bairro Inédito"
            else:
                scan_result = "⚠️ Repetindo (Sem opções inéditas)"
        else:
            scan_result = "⚪ Scanner Off"

        if not candidatos: candidatos = self.bairros
        
        bairro = random.choice(candidatos)
        ativo = self._definir_ativo(persona['cluster_ref'], bairro['zona_norm'])
        formato = random.choice(GenesisConfig.CONTENT_FORMATS)

        return {
            "persona": persona,
            "bairro": bairro,
            "ativo": ativo,
            "formato": formato,
            "scan_status": self.scanner.status,
            "scan_log": scan_result
        }

    def _definir_ativo(self, cluster, zona):
        if zona == "industrial": return "Galpão Logístico"
        if cluster == "HIGH_END": return "Casa Alto Padrão"
        if cluster == "INVESTOR" and zona == "residencial_aberto": return "Lote (Flip)"
        if zona == "residencial_fechado": return "Sobrado em Condomínio"
        if zona == "chacaras_fechado": return "Chácara em Condomínio"
        return "Imóvel Residencial"

# =========================================================
# ✍️ PROMPT ARCHITECT (FIXED STRINGS)
# =========================================================

class PromptArchitect:
    def format_date_pt(self, date_obj):
        meses = {1:"jan.", 2:"fev.", 3:"mar.", 4:"abr.", 5:"mai.", 6:"jun.", 
                 7:"jul.", 8:"ago.", 9:"set.", 10:"out.", 11:"nov.", 12:"dez."}
        return f"{date_obj.day} de {meses[date_obj.month]} de {date_obj.year}"

    def build(self, strategy, pub_date):
        s = strategy
        p = s['persona']
        b = s['bairro']
        
        data_extenso = self.format_date_pt(pub_date)
        data_iso = pub_date.strftime("%Y-%m-%dT09:00:00-03:00")
        data_mod = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S-03:00")

        # 1. JSON-LD Construído Separadamente (Evita conflito de chaves {})
        # Note o uso de {{ }} para escapar as chaves que não são variáveis Python
        json_ld_template = """
<script type="application/ld+json">
{{
    "@context": "[https://schema.org](https://schema.org)",
    "@type": "BlogPosting",
    "headline": "INSIRA O TÍTULO H1 AQUI",
    "datePublished": "{0}",
    "dateModified": "{1}",
    "author": {{ "@type": "Organization", "name": "Imobiliária Saber" }},
    "publisher": {{
        "@type": "Organization", 
        "name": "Imobiliária Saber", 
        "logo": {{ "@type": "ImageObject", "url": "[https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEixiE1KghKkH0E-I53yyi5zoT7eRX0lxCGLpcWLGAmEE5st8OfHfuzbxfiygwCWRqAdSfpmjAhM8-SogHDU_1gXCX6IHrjW1BaUc87un1lF1o6y2Et7eV0m3gJgvfJs3HsAGyAcPYk8Tl_65rlQmgAp5orRZqtLDvixbCUwscTT8ZJO-7zckc36rNkWHz4/s1600/1000318124.png](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEixiE1KghKkH0E-I53yyi5zoT7eRX0lxCGLpcWLGAmEE5st8OfHfuzbxfiygwCWRqAdSfpmjAhM8-SogHDU_1gXCX6IHrjW1BaUc87un1lF1o6y2Et7eV0m3gJgvfJs3HsAGyAcPYk8Tl_65rlQmgAp5orRZqtLDvixbCUwscTT8ZJO-7zckc36rNkWHz4/s1600/1000318124.png)" }}
    }}
}}
</script>
""".format(data_iso, data_mod)

        # 2. Definição das Regras CSS (Source 9, 10 do REGRAS.txt)
        css_table_wrapper = '<div style="overflow-x: auto; width: 100%; margin-bottom: 20px;">'
        css_table_tag = '<table style="width: 100%; min-width: 600px; border-collapse: collapse;">'
        css_td = 'style="padding: 12px; border: 1px solid #cccccc; word-break: keep-all; hyphens: none;"'

        # 3. Construção do Prompt Seguro (Sem f-string gigante)
        prompt_parts = []
        
        prompt_parts.append("# ZONA DE SEGURANÇA MÁXIMA (REGRAS.txt COMPLIANT)")
        prompt_parts.append(f"CONTEXTO: Você é o GENESIS MAGNETO. Escreva para a persona: {p['nome']}.")
        prompt_parts.append(f"DOR: {p['dor']} | LOCAL: {b['nome']} | ATIVO: {s['ativo']}")
        prompt_parts.append(f"FORMATO: {s['formato']}")
        
        prompt_parts.append("\n## PROTOCOLO DE PESQUISA (SEARCH MODE)")
        prompt_parts.append(f"1. A IA DEVE pesquisar no Google Maps o entorno de: {b['nome']}, Indaiatuba.")
        prompt_parts.append("2. Cite 3 locais REAIS (Escolas, Mercados) a menos de 10 min.")
        prompt_parts.append("3. NÃO INVENTE nomes de estabelecimentos. Se não achar, use referências genéricas reais.")

        prompt_parts.append("\n## REGRAS TÉCNICAS (HTML FRAGMENT)")
        prompt_parts.append("1. PROIBIDO: <!DOCTYPE>, <html>, <head>, <body>, <meta>, <title>.")
        prompt_parts.append("2. Comece direto com o conteúdo visual (h2, p).")
        prompt_parts.append("3. TABELAS (ANTI-QUEBRA): Use EXATAMENTE este CSS:")
        prompt_parts.append(f"   - Wrapper: {css_table_wrapper}")
        prompt_parts.append(f"   - Table: {css_table_tag}")
        prompt_parts.append(f"   - Células (TD/TH): {css_td}")

        prompt_parts.append("\n## CHECKLIST DE ENTREGA (ORDEM 1-8)")
        prompt_parts.append("1. LOG DE PESQUISA (Locais encontrados)")
        prompt_parts.append("2. BLOCKCODE (HTML + JSON-LD + Script de Captura)")
        prompt_parts.append("3. TÍTULO (H1)")
        prompt_parts.append("4. MARCADORES (Tags SEO)")
        prompt_parts.append(f"5. DATA: {data_extenso}")
        prompt_parts.append("6. LOCAL: Indaiatuba")
        prompt_parts.append(f"7. DESCRIÇÃO: (Focada na dor: {p['dor']})")
        prompt_parts.append("8. IMAGEM: (Prompt IA)")

        prompt_parts.append("\n## ESTRUTURA MODELO DO HTML (Copie esta estrutura):")
        prompt_parts.append("```html")
        prompt_parts.append("<style>h2 { color: #003366; } p { font-size: 19px; line-height: 1.6; }</style>")
        prompt_parts.append("")
        prompt_parts.append(json_ld_template.strip())
        prompt_parts.append("")
        prompt_parts.append("<h2>Título Impactante</h2>")
        prompt_parts.append("<p>Texto persuasivo...</p>")
        prompt_parts.append("")
        prompt_parts.append(css_table_wrapper)
        prompt_parts.append("  " + css_table_tag)
        prompt_parts.append(f"    <tr><th {css_td}>Local</th><th {css_td}>Tempo</th></tr>")
        prompt_parts.append("    ")
        prompt_parts.append("  </table>")
        prompt_parts.append("</div>")
        prompt_parts.append("")
        prompt_parts.append(GenesisConfig.LEAD_SCRIPT)
        prompt_parts.append("```")

        return "\n".join(prompt_parts)

# =========================================================
# 🖥️ UI STREAMLIT
# =========================================================

def main():
    st.set_page_config(page_title="Genesis v10.1 Safe", page_icon="🛡️", layout="wide")

    st.markdown(f"""
    <style>
        .stApp {{ background-color: {GenesisConfig.THEME['bg']}; }}
        .header-box {{ 
            padding: 15px; background: white; border-radius: 10px; 
            border-left: 5px solid {GenesisConfig.THEME['primary']}; margin-bottom: 20px;
        }}
        .stButton button {{
            background-color: {GenesisConfig.THEME['primary']}; color: white; 
            font-weight: bold; padding: 12px; border-radius: 6px; width: 100%;
        }}
        /* Força a área de texto a ter fonte monoespaçada e fundo claro */
        textarea {{ font-family: monospace !important; }}
    </style>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns([3, 1])
    with c1:
        st.title("🛡️ GENESIS APP V.10.1")
        st.markdown("**Safe Mode:** Correção de Strings e Blockcode")
    with c2:
        st.image("[https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEixiE1KghKkH0E-I53yyi5zoT7eRX0lxCGLpcWLGAmEE5st8OfHfuzbxfiygwCWRqAdSfpmjAhM8-SogHDU_1gXCX6IHrjW1BaUc87un1lF1o6y2Et7eV0m3gJgvfJs3HsAGyAcPYk8Tl_65rlQmgAp5orRZqtLDvixbCUwscTT8ZJO-7zckc36rNkWHz4/s1600/1000318124.png](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEixiE1KghKkH0E-I53yyi5zoT7eRX0lxCGLpcWLGAmEE5st8OfHfuzbxfiygwCWRqAdSfpmjAhM8-SogHDU_1gXCX6IHrjW1BaUc87un1lF1o6y2Et7eV0m3gJgvfJs3HsAGyAcPYk8Tl_65rlQmgAp5orRZqtLDvixbCUwscTT8ZJO-7zckc36rNkWHz4/s1600/1000318124.png)", width=80)

    # Sidebar
    with st.sidebar:
        data_pub = st.date_input("Data Publicação", datetime.date.today())
        use_scanner = st.checkbox("Usar Blog Scanner", value=True)
        st.caption(f"Status: {GenesisConfig.VERSION}")

    # Geração
    if st.button("GERAR PAUTA BLINDADA"):
        brain = GenesisBrain()
        architect = PromptArchitect()
        
        with st.spinner("Compilando prompt seguro..."):
            strategy = brain.generate_strategy(use_scanner)
            # Constrói o prompt string linha a linha para segurança
            prompt_final = architect.build(strategy, data_pub)
            
            st.session_state['strategy'] = strategy
            st.session_state['prompt'] = prompt_final

    # Exibição
    if 'prompt' in st.session_state:
        s = st.session_state['strategy']
        
        # Resumo
        st.markdown(f"""
        <div class="header-box">
            <b>Persona:</b> {s['persona']['nome']} | <b>Bairro:</b> {s['bairro']['nome']} | 
            <b>Scanner:</b> {s['scan_log']}
        </div>
        """, unsafe_allow_html=True)

        st.subheader("📋 Copie o Prompt Abaixo:")
        
        # USANDO TEXT_AREA AO INVÉS DE CODE PARA EVITAR QUEBRA VISUAL
        st.text_area(
            label="Prompt Final",
            value=st.session_state['prompt'],
            height=600,
            help="Clique dentro, Ctrl+A e Ctrl+C para copiar tudo."
        )
        
        # Botão Download (Backup)
        filename = f"PAUTA_{s['bairro']['nome'].replace(' ','_')}.txt"
        st.download_button("💾 Baixar Arquivo .txt", st.session_state['prompt'], filename)

if __name__ == "__main__":
    main()