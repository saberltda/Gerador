# src/config.py
import datetime

class GenesisConfig:
    VERSION = "GERADOR V.70 (ALL PERSONAS UNLOCKED - HUMANIZED)"

    # =====================================================
    # ⛔ CONFIGURAÇÃO CRÍTICA DE FUSO HORÁRIO
    # =====================================================
    TZ_BRASILIA = datetime.timezone(datetime.timedelta(hours=-3))
    FUSO_PADRAO = "-03:00"

    # Cores e URLs
    COLOR_PRIMARY = "#003366"   # Azul Saber
    COLOR_ACTION  = "#28a745"   # Verde Ação
    BLOG_URL = "https://blog.saber.imb.br"

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

    REAL_ESTATE_TOPICS_DISPLAY = TOPICS_MAP 

    REAL_ESTATE_FORMATS_MAP = {
        "GUIA_DEFINITIVO": "📘 Guia Definitivo (Imobiliário)",
        "LISTA_POLEMICA": "🔥 Lista Polêmica (Imobiliário)",
        "COMPARATIVO_TECNICO": "⚖️ Comparativo Técnico (Imobiliário)",
        "INSIGHT_DE_CORRETOR": "💡 Insight de Corretor",
        "PERGUNTAS_RESPOSTAS": "❓ Perguntas & Respostas",
        "CENARIO_ANALITICO": "📊 Cenário Analítico (Previsão)",
        "CHECKLIST_TECNICO": "📝 Checklist Técnico (Vistoria)"
    }

    ASSETS_CATALOG = {
        "HIGH_END": ["MANSÃO EM CONDOMÍNIO", "CASA TÉRREA ALTO PADRÃO", "TERRENO EM CONDOMÍNIO DE LUXO"],
        "FAMILY": ["CASA EM CONDOMÍNIO FECHADO", "SOBRADO COM ÁREA GOURMET", "CASA TÉRREA COM QUINTAL"],
        "URBAN": ["APARTAMENTO 3 DORMITÓRIOS", "STUDIO / LOFT MODERNO", "COBERTURA DUPLEX"],
        "INVESTOR": ["TERRENO EM CONDOMÍNIO (LOTE)", "IMÓVEL PARA REFORMA (FLIP)", "KITNET PARA RENDA"],
        "LOGISTICS": ["GALPÃO INDUSTRIAL AAA", "ÁREA PARA CD LOGÍSTICO", "TERRENO INDUSTRIAL"],
        "RURAL_LIFESTYLE": ["CHÁCARA", "SÍTIO DE LAZER", "HARAS OU ESTÂNCIA"],
        "CORPORATE": ["SALA COMERCIAL", "LAJE CORPORATIVA", "PRÉDIO MONOUSUÁRIO"]
    }

    EMOTIONAL_TRIGGERS_MAP = {
        "AUTORIDADE": "👑 Autoridade (Especialista)", 
        "ESCASSEZ": "💎 Escassez (Últimas Unidades)",
        "URGENCIA": "🚨 Urgência (Agora)", 
        "PROVA_SOCIAL": "👥 Prova Social (Outros compraram)",
        "SEGURANCA": "🛡️ Segurança (Risco Zero)",
        "GANANCIA": "💰 Ganância (Lucro)",
        "EXCLUSIVIDADE": "✨ Exclusividade (Só para você)"
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
    # 3. PERSONAS & FILTROS (LISTA COMPLETA)
    # =====================================================
    PERSONAS = {
        "CITIZEN_GENERAL": {
            "cluster_ref": "PORTAL", 
            "nome": "🗞️ Redação (Jornalismo)", 
            "dor": "Desinformação e Fake News", 
            "desejo": "Informação confiável e Verdade"
        },
        "INVESTOR_SHARK_ROI": {
            "cluster_ref": "INVESTOR", 
            "nome": "🦈 Investidor Tubarão (Agressivo)", 
            "dor": "Baixo retorno e Custo de Oportunidade", 
            "desejo": "ROI máximo e Valorização rápida"
        },
        "INVESTOR_SAFE": {
            "cluster_ref": "INVESTOR", 
            "nome": "🛡️ Investidor Conservador (Renda)", 
            "dor": "Medo da vacância e Depredação", 
            "desejo": "Renda passiva segura e Liquidez"
        },
        "EXODUS_SP_ELITE_FAMILY": {
            "cluster_ref": "HIGH_END", 
            "nome": "✈️ Família Exodus (Elite SP)", 
            "dor": "Violência urbana e Trânsito", 
            "desejo": "Segurança armada e Qualidade de vida"
        },
        "FAMILY_FIRST_TIME": {
            "cluster_ref": "FAMILY", 
            "nome": "👨‍👩‍👧‍👦 Família em Crescimento", 
            "dor": "Falta de espaço e Quintal pequeno", 
            "desejo": "Espaço gourmet e Quarto extra"
        },
        "REMOTE_WORKER": {
            "cluster_ref": "FAMILY", 
            "nome": "💻 Profissional Home Office", 
            "dor": "Barulho e Falta de escritório", 
            "desejo": "Silêncio e Cômodo dedicado"
        },
        "HYBRID_COMMUTER": {
            "cluster_ref": "URBAN", 
            "nome": "🚗 O Pendular (Trabalha em SP)", 
            "dor": "Cansaço da estrada", 
            "desejo": "Acesso rápido à Rodovia e Praticidade"
        },
        "RETIREE_ACTIVE": {
            "cluster_ref": "FAMILY", 
            "nome": "🍷 Melhor Idade Ativa", 
            "dor": "Escadas e Solidão", 
            "desejo": "Casa térrea e Proximidade de serviços"
        },
        "PET_LOVER": {
            "cluster_ref": "FAMILY", 
            "nome": "🐾 Tutor de Grandes Animais", 
            "dor": "Condomínio restritivo", 
            "desejo": "Quintal gramado e Espaço pet"
        },
        "MEDICAL_PRO": {
            "cluster_ref": "HIGH_END", 
            "nome": "⚕️ Profissional de Saúde (Médico)", 
            "dor": "Rotina estressante e Plantões", 
            "desejo": "Oásis de descanso e Proximidade HAOC"
        },
        "FIRST_HOME_DREAMER": {
            "cluster_ref": "URBAN", 
            "nome": "🔑 1º Imóvel (Jovem)", 
            "dor": "Orçamento apertado e Aprovação", 
            "desejo": "Sair do aluguel e Viabilidade"
        },
        "LUXURY_SEEKER": {
            "cluster_ref": "HIGH_END", 
            "nome": "💎 Buscador de Exclusividade", 
            "dor": "Padronização e Falta de privacidade", 
            "desejo": "Arquitetura autoral e Status"
        },
        "LOGISTICS_MANAGER": {
            "cluster_ref": "LOGISTICS", 
            "nome": "🚚 Gestor Logístico / Empresário", 
            "dor": "Custo logístico (Last Mile)", 
            "desejo": "Proximidade Viracopos e Pé direito alto"
        }
    }
    
    # =====================================================
    # ⚖️ REGRAS DE VOCABULÁRIO (HUMANIZAÇÃO ATIVA)
    # =====================================================
    RULES = {
        # Lista flexibilizada: Adjetivos como "tranquilo", "lindo" e "maravilhoso" são PERMITIDOS.
        # Proibidos apenas clichês de baixo valor que reduzem a autoridade do texto.
        "FORBIDDEN_WORDS": [
            "oportunidade única", 
            "venha conferir", 
            "top", 
            "sensacional", 
            "imperdível"
        ],
        "JOURNALISM_STOPWORDS": ["eu acho", "na minha opinião"]
    }
