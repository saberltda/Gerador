# src/config.py

class GenesisConfig:
    VERSION = "GERADOR V.62 (SYNCED PORTAL EDITION)"

    # Design System & URLs
    COLOR_PRIMARY = "#003366"   # Azul Saber
    COLOR_ACTION  = "#28a745"   # Verde Ação
    GRADIENT_CTA  = "linear-gradient(135deg, #003366 0%, #001a33 100%)"
    BLOG_URL = "https://blog.saber.imb.br"
    FUSO_PADRAO = "-03:00"

    # =====================================================
    # 1. REGRAS GERAIS E BLOQUEIOS
    # =====================================================
    RULES = {
        "FORBIDDEN_WORDS": [
            "oportunidade única", "venha conferir", "show de ofertas", 
            "top", "sensacional", "imperdível", "preço baixo",
            # No modo jornalismo, proibimos adjetivos vazios
            "maravilhoso", "espetacular", "lindo"
        ],
        "JOURNALISM_STOPWORDS": [
            "eu acho", "na minha opinião", "com certeza", "sem dúvida"
        ]
    }

    STRICT_GUIDELINES = [
        "JORNALISMO VERDADE: Nunca invente fatos, datas ou nomes de autoridades.",
        "IMPARCIALIDADE: Ouça (ou simule com dados) os dois lados da história.",
        "LOCALISMO RADICAL: Tudo deve ter conexão direta com Indaiatuba.",
        "SEM OPINIÃO: O jornalista relata, não julga (exceto em editoriais explícitos)."
    ]

    # =====================================================
    # 2. INTEGRAÇÃO IMOBILIÁRIA (MODO CORRETOR)
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

    TOPICS_WEIGHTS = {k: 80 for k in TOPICS_MAP.keys()} # Pesos equalizados

    # Lista Exclusiva para Modo Imobiliária
    REAL_ESTATE_FORMATS_MAP = {
        "GUIA_DEFINITIVO": "📘 Guia Definitivo (Imobiliário)",
        "LISTA_POLEMICA": "🔥 Lista Polêmica (Imobiliário)",
        "COMPARATIVO_TECNICO": "⚖️ Comparativo Técnico (Imobiliário)",
        "INSIGHT_DE_CORRETOR": "💡 Insight de Corretor",
        "PERGUNTAS_RESPOSTAS": "❓ Perguntas & Respostas"
    }

    # =====================================================
    # 3. O NOVO PORTAL: MATRIZ DE SINCRONIZAÇÃO
    # =====================================================
    
    # Esta matriz define a lógica: Editoria -> Tópicos Permitidos -> Formatos Permitidos
    PORTAL_MATRIX = {
        "GIRO_POLICIAL": {
            "label": "🚔 Plantão Policial & Trânsito",
            "topics": [
                "ACIDENTE_GRAVE", "OPERACAO_POLICIAL", "ALERTAS_DEFESA_CIVIL",
                "MOBILIDADE_URBANA", "OBRAS_VIARIAS"
            ],
            "formats": ["NOTICIA_IMPACTO", "CHECAGEM_FATOS", "DATA_DRIVEN"]
        },
        "POLITICA_BASTIDORES": {
            "label": "🏛️ Política & Poder",
            "topics": [
                "CAMARA_MUNICIPAL", "DECISOES_PREFEITURA", "ELEICOES_CENARIOS",
                "POLEMICA_LEGISLATIVA", "ORCAMENTO_PUBLICO"
            ],
            "formats": ["DOSSIE_INVESTIGATIVO", "EXPLAINER", "ENTREVISTA_PING_PONG", "BASTIDORES_ANALISE"]
        },
        "AGENDA_CULTURAL": {
            "label": "🎉 Viver Indaiatuba (Lazer)",
            "topics": [
                "SHOWS_EVENTOS", "GASTRONOMIA_NOVIDADES", "PARQUE_ECOLOGICO_LAZER",
                "ROTEIROS_FIM_DE_SEMANA", "CULTURA_ARTE"
            ],
            "formats": ["LISTA_CURADORIA", "ROTEIRO_EXPERIENCIA", "NOTICIA_SERVICO"]
        },
        "ECONOMIA_LOCAL": {
            "label": "💰 Seu Bolso & Negócios",
            "topics": [
                "VAGAS_EMPREGO", "NOVAS_EMPRESAS", "MERCADO_IMOBILIARIO",
                "CUSTO_DE_VIDA", "INAUGURACOES"
            ],
            "formats": ["SERVICO_PASSO_A_PASSO", "DATA_DRIVEN", "LISTA_CURADORIA"]
        },
        "COTIDIANO_CIDADE": {
            "label": "🏘️ Comunidade & Serviços",
            "topics": [
                "CLIMA_TEMPO", "SAUDE_PUBLICA", "EDUCACAO_ESCOLAS",
                "CAUSA_ANIMAL", "HISTORIAS_DE_VIDA"
            ],
            "formats": ["SERVICO_PASSO_A_PASSO", "EXPLAINER", "VOZ_DA_RUA"]
        },
        "DESTAQUE_DO_DIA": {
            "label": "⚡ Resumo Diário (Manchete)",
            "topics": ["RESUMO_GERAL", "PRINCIPAIS_MANCHETES"],
            "formats": ["REVISTA_DIGITAL_DIARIA"]
        }
    }

    # --- DICIONÁRIO DE VISUALIZAÇÃO (TÓPICOS) ---
    PORTAL_TOPICS_DISPLAY = {
        "ACIDENTE_GRAVE": "🚨 Acidentes e Ocorrências Graves",
        "OPERACAO_POLICIAL": "🚓 Operações e Segurança Pública",
        "ALERTAS_DEFESA_CIVIL": "⛈️ Clima Extremo e Defesa Civil",
        "MOBILIDADE_URBANA": "🚦 Trânsito e Mudanças Viárias",
        "OBRAS_VIARIAS": "🚧 Obras e Interdições",
        "CAMARA_MUNICIPAL": "⚖️ Votações na Câmara",
        "DECISOES_PREFEITURA": "✍️ Decretos e Atos do Executivo",
        "ELEICOES_CENARIOS": "🗳️ Cenário Eleitoral e Pesquisas",
        "POLEMICA_LEGISLATIVA": "🔥 Polêmicas e Debates",
        "ORCAMENTO_PUBLICO": "💸 Dinheiro Público (Para onde vai?)",
        "SHOWS_EVENTOS": "🎵 Agenda de Shows e Eventos",
        "GASTRONOMIA_NOVIDADES": "🍔 Gastronomia e Novos Bares",
        "PARQUE_ECOLOGICO_LAZER": "🌳 Parque Ecológico e Ar Livre",
        "ROTEIROS_FIM_DE_SEMANA": "📅 O que fazer no Fim de Semana",
        "CULTURA_ARTE": "🎨 Exposições e Cultura",
        "VAGAS_EMPREGO": "💼 Balcão de Empregos",
        "NOVAS_EMPRESAS": "🏭 Indústrias e Comércio",
        "MERCADO_IMOBILIARIO": "🏠 Mercado Imobiliário Local",
        "CUSTO_DE_VIDA": "🛒 Preços e Economia Doméstica",
        "INAUGURACOES": "🎀 Inaugurações Recentes",
        "CLIMA_TEMPO": "☀️ Previsão do Tempo Detalhada",
        "SAUDE_PUBLICA": "🏥 SUS, Hospitais e Vacinação",
        "EDUCACAO_ESCOLAS": "🎓 Educação e Escolas",
        "CAUSA_ANIMAL": "🐾 Pets e Causa Animal",
        "HISTORIAS_DE_VIDA": "❤️ Personagens da Cidade",
        "RESUMO_GERAL": "📰 Mix de Notícias do Dia",
        "PRINCIPAIS_MANCHETES": "🗞️ As Capas dos Jornais"
    }

    # --- DICIONÁRIO DE VISUALIZAÇÃO (FORMATOS) ---
    PORTAL_FORMATS_DISPLAY = {
        "NOTICIA_IMPACTO": "📰 Hard News (Fato Seco)",
        "CHECAGEM_FATOS": "✅ Checagem (Verdade ou Mentira?)",
        "DATA_DRIVEN": "📊 Jornalismo de Dados (Raio-X)",
        "DOSSIE_INVESTIGATIVO": "🕵️ Dossiê Investigativo (Profundo)",
        "EXPLAINER": "🧠 Explainer (Entenda o Caso)",
        "ENTREVISTA_PING_PONG": "🎙️ Entrevista (Ping-Pong)",
        "BASTIDORES_ANALISE": "👀 Coluna de Análise/Opinião",
        "LISTA_CURADORIA": "📋 Lista / Roteiro (Top 5)",
        "ROTEIRO_EXPERIENCIA": "⭐ Review / Experiência Real",
        "NOTICIA_SERVICO": "ℹ️ Notícia de Serviço",
        "SERVICO_PASSO_A_PASSO": "👣 Tutorial / Passo a Passo",
        "VOZ_DA_RUA": "🗣️ Reportagem Humanizada",
        "REVISTA_DIGITAL_DIARIA": "🗞️ Giro Completo (Newsletter)"
    }
    
    # (Mantido para compatibilidade reversa com Imobiliária)
    PORTAL_FORMATS_MAP = PORTAL_FORMATS_DISPLAY 
    
    # Unificado (apenas para compatibilidade interna se necessário)
    CONTENT_FORMATS_MAP = {**PORTAL_FORMATS_MAP, **REAL_ESTATE_FORMATS_MAP}
    CONTENT_FORMATS = list(CONTENT_FORMATS_MAP.keys())

    # =====================================================
    # 4. PERSONAS E CATÁLOGOS
    # =====================================================
    
    PERSONAS = {
        "CITIZEN_GENERAL": {
            "cluster_ref": "PORTAL", 
            "nome": "🗞️ REDAÇÃO (Jornalismo Profissional)",
            "dor": "Desinformação e falta de profundidade nas notícias locais.",
            "desejo": "Informação confiável, verificada e útil para o dia a dia."
        },
        "INVESTOR_SHARK_ROI": {"cluster_ref": "INVESTOR", "nome": "🦈 INVESTIDOR TUBARÃO", "dor": "Risco", "desejo": "Retorno"},
        "EXODUS_SP_ELITE_FAMILY": {"cluster_ref": "HIGH_END", "nome": "✈️ FAMÍLIA EXODUS", "dor": "Segurança", "desejo": "Qualidade"},
        "FIRST_HOME_DREAMER": {"cluster_ref": "URBAN", "nome": "🔑 1º IMÓVEL", "dor": "Orçamento", "desejo": "Viabilidade"}
    }

    # --- EDITORIAS (CATÁLOGO LEGADO - MANTIDO P/ BACKUP) ---
    PORTAL_CATALOG = {
        "DESTAQUE_DIARIO": ["Resumo das Principais Notícias do Dia"], 
        "CIDADE_ALERTA": ["Trânsito e Mobilidade", "Segurança Pública", "Clima e Defesa Civil"],
        "PODER_POLITICA": ["Câmara Municipal", "Decisões da Prefeitura"],
        "VIVER_INDAIATUBA": ["Agenda Cultural", "Gastronomia e Bares", "Parque Ecológico"],
        "SEU_DINHEIRO": ["Vagas de Emprego", "Comércio Local"],
        "EDUCACAO_FUTURO": ["Escolas e Creches", "Cursos Gratuitos"],
        "COMUNIDADE": ["Causas Animais (Pets)", "Solidariedade e ONGs"]
    }
    
    # --- CATÁLOGO IMOBILIÁRIO ---
    ASSETS_CATALOG = {
        "HIGH_END": ["MANSÃO EM CONDOMÍNIO", "CASA TÉRREA ALTO PADRÃO"],
        "FAMILY": ["CASA EM CONDOMÍNIO", "SOBRADO COM ÁREA GOURMET"],
        "URBAN": ["APARTAMENTO 3 DORMITÓRIOS", "STUDIO / LOFT MODERNO"],
        "INVESTOR": ["TERRENO EM CONDOMÍNIO", "IMÓVEL PARA REFORMA"],
        "LOGISTICS": ["GALPÃO INDUSTRIAL AAA", "ÁREA PARA CD"],
        "RURAL_LIFESTYLE": ["CHÁCARA EM ITAICI", "SÍTIO OU HARAS"],
        "CORPORATE": ["SALA COMERCIAL", "LAJE CORPORATIVA"]
    }

    # --- PESOS E MAPAS LEGADOS (COMPATIBILIDADE) ---
    PORTAL_TOPICS_MAP = PORTAL_TOPICS_DISPLAY # Alias
    PORTAL_TOPICS_WEIGHTS = {k: 90 for k in PORTAL_TOPICS_DISPLAY.keys()}

    EMOTIONAL_TRIGGERS_MAP = {
        "AUTORIDADE": "👑 Autoridade", "ESCASSEZ": "💎 Escassez",
        "URGENCIA": "🚨 Urgência", "PROVA_SOCIAL": "👥 Prova Social"
    }
