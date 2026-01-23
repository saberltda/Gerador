# src/config.py

class GenesisConfig:
    VERSION = "GERADOR V.63 (FULL STACK)"

    # Cores e URLs
    COLOR_PRIMARY = "#003366"   # Azul Saber
    COLOR_ACTION  = "#28a745"   # Verde Ação
    BLOG_URL = "https://blog.saber.imb.br"
    FUSO_PADRAO = "-03:00"

    # =====================================================
    # 1. IMOBILIÁRIA (MODO CORRETOR)
    # =====================================================
    TOPICS_MAP = {
        "MERCADO_DADOS": "📈 Dados de Mercado e Rentabilidade",
        "INVESTIMENTO_ROI": "💰 Lucro e Valorização de Patrimônio",
        "FINANCAS_TOKEN": "💳 Potencial de Financiamento e Crédito",
        "SUSTENTABILIDADE_ESG": "🌱 Sustentabilidade e Economia Verde",
        "LOCALIZACAO_PREMIUM": "📍 Localização e Facilidade de Acesso",
        "LUXO_COMPACTO": "💎 Luxo e Design Exclusivo",
        "CIDADES_INTELIGENTES": "🏙️ Infraestrutura Urbana e Modernidade",
        "HOME_OFFICE_FLEX": "💻 Espaço para Trabalho e Flexibilidade",
        "LOGISTICA_HUB": "🚚 Logística e Proximidade com Aeroporto",
        "BEM_ESTAR_BIOFILIA": "🌿 Saúde, Bem-Estar e Natureza",
        "SENIOR_LIVING": "🍷 Qualidade de Vida na Melhor Idade",
        "SEGURANCA_TECH": "🛡️ Segurança e Monitoramento Inteligente",
        "SHORT_STAY": "🧳 Aluguel por Temporada e Renda Extra",
        "PETS_GARDEN": "🐾 Espaço para Animais e Quintal",
        "SMART_HOME": "📱 Casa Inteligente e Tecnologia",
        "JURIDICO_SEGURANCA": "⚖️ Segurança Jurídica e Documentação",
        "ARQUITETURA_FACHADA": "🎨 Arquitetura e Estilo da Fachada",
        "COMUNIDADE_VIZINHANCA": "🤝 Vizinhança e Vida em Comunidade"
    }

    REAL_ESTATE_FORMATS_MAP = {
        "GUIA_DEFINITIVO": "📘 Guia Definitivo (Imobiliário)",
        "LISTA_POLEMICA": "🔥 Lista Polêmica (Imobiliário)",
        "COMPARATIVO_TECNICO": "⚖️ Comparativo Técnico (Imobiliário)",
        "INSIGHT_DE_CORRETOR": "💡 Insight de Corretor",
        "PERGUNTAS_RESPOSTAS": "❓ Perguntas & Respostas"
    }

    ASSETS_CATALOG = {
        "HIGH_END": ["MANSÃO EM CONDOMÍNIO", "CASA TÉRREA ALTO PADRÃO"],
        "FAMILY": ["CASA EM CONDOMÍNIO", "SOBRADO COM ÁREA GOURMET"],
        "URBAN": ["APARTAMENTO 3 DORMITÓRIOS", "STUDIO / LOFT MODERNO"],
        "INVESTOR": ["TERRENO EM CONDOMÍNIO", "IMÓVEL PARA REFORMA"],
        "LOGISTICS": ["GALPÃO INDUSTRIAL AAA", "ÁREA PARA CD"],
        "RURAL_LIFESTYLE": ["CHÁCARA EM ITAICI", "SÍTIO OU HARAS"],
        "CORPORATE": ["SALA COMERCIAL", "LAJE CORPORATIVA"]
    }

    EMOTIONAL_TRIGGERS_MAP = {
        "AUTORIDADE": "👑 Autoridade", "ESCASSEZ": "💎 Escassez",
        "URGENCIA": "🚨 Urgência", "PROVA_SOCIAL": "👥 Prova Social"
    }

    # =====================================================
    # 2. PORTAL (MODO JORNALISMO)
    # =====================================================
    PORTAL_TOPICS_MAP = {
        "GIRO_NOTICIAS": "⚡ Giro de Notícias (Tempo Real)",
        "JORNALISMO_SOLUCOES": "💡 Jornalismo de Soluções (Como resolver?)",
        "FISCAL_DO_POVO": "🔍 Fiscal do Povo (Transparência/Denúncia)",
        "DATA_JOURNALISM": "📊 Raio-X de Dados (O que os números dizem)",
        "SERVICO_ESSENCIAL": "🛠️ Serviço e Utilidade (Guia Prático)",
        "RESGATE_MEMORIA": "🏛️ Memória Viva (História e Identidade)",
        "BASTIDORES_PODER": "⚖️ Bastidores do Poder (Política/Decisões)",
        "ECONOMIA_REAL": "💰 Economia Real (Bolso do Cidadão)",
        "VOZ_DA_RUA": "🗣️ Voz da Rua (Histórias Humanas/Comunidade)",
        "FUTURO_INOVACAO": "🚀 Futuro e Inovação (Obras/Projetos)"
    }

    PORTAL_FORMATS_MAP = {
        "NOTICIA_IMPACTO": "📰 Hard News (Notícia de Impacto)",
        "EXPLAINER": "🧠 Explainer (Entenda o Caso)",
        "DOSSIE_INVESTIGATIVO": "🕵️ Dossiê Investigativo (Longform)",
        "CHECAGEM_FATOS": "✅ Checagem de Fatos (Verdade ou Mentira)",
        "LISTA_CURADORIA": "📋 Curadoria (Top 5 / Roteiros)",
        "ENTREVISTA_PING_PONG": "🎙️ Entrevista Ping-Pong (Direto)",
        "SERVICO_PASSO_A_PASSO": "👣 Serviço Passo-a-Passo (Tutorial)"
    }

    PORTAL_CATALOG = {
        "DESTAQUE_DIARIO": ["Resumo das Principais Notícias do Dia"],
        "CIDADE_ALERTA": ["Trânsito e Mobilidade", "Segurança Pública", "Clima e Defesa Civil", "Saúde Pública (SUS/Hospitais)"],
        "PODER_POLITICA": ["Câmara Municipal", "Decisões da Prefeitura", "Diário Oficial", "Eleições e Votos"],
        "VIVER_INDAIATUBA": ["Agenda Cultural", "Gastronomia e Bares", "Parque Ecológico", "Eventos e Shows"],
        "SEU_DINHEIRO": ["Vagas de Emprego", "Comércio Local", "Preço da Cesta Básica", "Novas Empresas"],
        "EDUCACAO_FUTURO": ["Escolas e Creches", "Cursos Gratuitos", "Tecnologia e Inovação", "Obras de Infraestrutura"],
        "COMUNIDADE": ["Causas Animais (Pets)", "Solidariedade e ONGs", "Histórias de Moradores", "Esportes Locais"]
    }

    CONTENT_FORMATS_MAP = {**PORTAL_FORMATS_MAP, **REAL_ESTATE_FORMATS_MAP}

    # =====================================================
    # 3. PERSONAS
    # =====================================================
    PERSONAS = {
        "CITIZEN_GENERAL": {
            "cluster_ref": "PORTAL", 
            "nome": "🗞️ REDAÇÃO (Jornalismo Profissional)",
            "dor": "Desinformação.", "desejo": "Verdade."
        },
        "INVESTOR_SHARK_ROI": {"cluster_ref": "INVESTOR", "nome": "🦈 INVESTIDOR TUBARÃO", "dor": "Risco", "desejo": "Retorno"},
        "EXODUS_SP_ELITE_FAMILY": {"cluster_ref": "HIGH_END", "nome": "✈️ FAMÍLIA EXODUS", "dor": "Segurança", "desejo": "Qualidade"},
        "FIRST_HOME_DREAMER": {"cluster_ref": "URBAN", "nome": "🔑 1º IMÓVEL", "dor": "Orçamento", "desejo": "Viabilidade"}
    }
