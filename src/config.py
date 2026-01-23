# src/config.py

class GenesisConfig:
    VERSION = "GERADOR V.63 (SYNCED REAL ESTATE)"

    # Design System & URLs
    COLOR_PRIMARY = "#003366"   # Azul Saber
    COLOR_ACTION  = "#28a745"   # Verde Ação
    GRADIENT_CTA  = "linear-gradient(135deg, #003366 0%, #001a33 100%)"
    BLOG_URL = "https://blog.saber.imb.br"
    FUSO_PADRAO = "-03:00"

    # =====================================================
    # 1. REGRAS GERAIS
    # =====================================================
    RULES = {
        "FORBIDDEN_WORDS": [
            "oportunidade única", "venha conferir", "show de ofertas", 
            "top", "sensacional", "imperdível", "preço baixo",
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
    # 2. MATRIZ DE SINCRONIZAÇÃO (IMOBILIÁRIA)
    # =====================================================
    
    # Esta matriz define a lógica: Cluster -> Tópicos Permitidos -> Formatos Permitidos
    REAL_ESTATE_MATRIX = {
        "HIGH_END": {
            "label": "💎 Alto Padrão & Luxo",
            "topics": ["PRIVACIDADE_TOTAL", "ARQUITETURA_ASSINADA", "SEGURANCA_ARMADA", "LAZER_PRIVATIVO", "LOCALIZACAO_NOBRE"],
            "formats": ["INSIGHT_DE_CORRETOR", "COMPARATIVO_TECNICO", "GUIA_DEFINITIVO"]
        },
        "FAMILY": {
            "label": "👨‍👩‍👧‍👦 Família & Moradia",
            "topics": ["EDUCACAO_FILHOS", "SEGURANCA_CONDOMINIO", "LAZER_CLUBE", "PETS_GARDEN", "COMUNIDADE_VIZINHANCA"],
            "formats": ["GUIA_DEFINITIVO", "PERGUNTAS_RESPOSTAS", "LISTA_POLEMICA"]
        },
        "INVESTOR": {
            "label": "💰 Investidor & Rentabilidade",
            "topics": ["INVESTIMENTO_ROI", "LIQUIDEZ_ALUGUEL", "MERCADO_DADOS", "OPORTUNIDADE_FLIP", "VALORIZACAO_FUTURA"],
            "formats": ["DATA_DRIVEN", "COMPARATIVO_TECNICO", "CENARIO_ANALITICO"]
        },
        "URBAN": {
            "label": "🏙️ Urbano & Praticidade",
            "topics": ["MOBILIDADE_RAPIDA", "SERVICOS_APE", "PRIMEIRO_IMOVEL", "SMART_LIVING", "VARANDA_GOURMET"],
            "formats": ["LISTA_POLEMICA", "CHECKLIST_TECNICO", "GUIA_DEFINITIVO"]
        },
        "RURAL_LIFESTYLE": {
            "label": "🌿 Chácaras & Lazer Rural",
            "topics": ["DESCOMPRESSAO", "PRODUCAO_PROPRIA", "ESPACO_EVENTOS", "INTERNET_RURAL", "SEGURANCA_RURAL"],
            "formats": ["INSIGHT_DE_CORRETOR", "ROTINA_SUGERIDA", "GUIA_DEFINITIVO"]
        },
        "LOGISTICS": {
            "label": "🚚 Logística & Industrial",
            "topics": ["LOGISTICA_HUB", "ENERGIA_POTENCIA", "ACESSO_RODOVIA", "PE_DIREITO", "AREA_MANOBRA"],
            "formats": ["CHECKLIST_TECNICO", "DATA_DRIVEN", "COMPARATIVO_TECNICO"]
        },
        "CORPORATE": {
            "label": "💼 Corporativo & Escritórios",
            "topics": ["IMAGEM_CORPORATIVA", "NETWORKING_LOCAL", "FACILIDADE_CLIENTE", "CONECTIVIDADE", "SEGURANCA_TECH"],
            "formats": ["CHECKLIST_TECNICO", "LISTA_POLEMICA", "PERGUNTAS_RESPOSTAS"]
        }
    }

    # VISUALIZAÇÃO DE TÓPICOS IMOBILIÁRIOS
    REAL_ESTATE_TOPICS_DISPLAY = {
        "PRIVACIDADE_TOTAL": "🔒 Privacidade Absoluta e Sossego",
        "ARQUITETURA_ASSINADA": "🎨 Arquitetura Autoral e Design",
        "SEGURANCA_ARMADA": "🛡️ Segurança Patrimonial de Elite",
        "LAZER_PRIVATIVO": "🏊 Lazer Privativo (Piscina/Gourmet)",
        "LOCALIZACAO_NOBRE": "📍 Localização Premium e Valorizada",
        "EDUCACAO_FILHOS": "🎓 Proximidade de Escolas Bilíngues",
        "SEGURANCA_CONDOMINIO": "👮 Segurança e Portaria 24h",
        "LAZER_CLUBE": "club Lazer Completo (Estilo Resort)",
        "PETS_GARDEN": "🐾 Espaço Pet e Quintal",
        "COMUNIDADE_VIZINHANCA": "🤝 Vizinhança e Perfil Familiar",
        "INVESTIMENTO_ROI": "📈 ROI e Potencial de Valorização",
        "LIQUIDEZ_ALUGUEL": "💸 Liquidez para Locação",
        "MERCADO_DADOS": "📊 Dados de Mercado e Metro Quadrado",
        "OPORTUNIDADE_FLIP": "🔨 Oportunidade de Reforma (Flip)",
        "VALORIZACAO_FUTURA": "🚀 Vetor de Crescimento Urbano",
        "MOBILIDADE_RAPIDA": "🚦 Mobilidade e Acesso ao Centro",
        "SERVICOS_APE": "🛍️ Conveniência e Serviços a Pé",
        "PRIMEIRO_IMOVEL": "🔑 Estratégia do 1º Imóvel",
        "SMART_LIVING": "📱 Automação e Modernidade",
        "VARANDA_GOURMET": "🍖 Varanda Gourmet e Receber Bem",
        "DESCOMPRESSAO": "🧘 Refúgio e Descompressão Mental",
        "PRODUCAO_PROPRIA": "🍎 Pomar e Horta Orgânica",
        "ESPACO_EVENTOS": "🎉 Espaço para Grandes Famílias",
        "INTERNET_RURAL": "📡 Conectividade no Campo",
        "SEGURANCA_RURAL": "🚧 Monitoramento Rural e Segurança",
        "LOGISTICA_HUB": "✈️ Proximidade Viracopos/SP-75",
        "ENERGIA_POTENCIA": "⚡ Capacidade Elétrica Industrial",
        "ACESSO_RODOVIA": "🚛 Logística Last Mile",
        "PE_DIREITO": "🏭 Pé Direito e Capacidade de Piso",
        "AREA_MANOBRA": "🚛 Pátio e Docas",
        "IMAGEM_CORPORATIVA": "👔 Status e Imagem da Empresa",
        "NETWORKING_LOCAL": "🤝 Networking no Condomínio",
        "FACILIDADE_CLIENTE": "🅿️ Estacionamento e Acesso Cliente",
        "CONECTIVIDADE": "💻 Fibra Óptica e Redundância",
        "SEGURANCA_TECH": "📷 Controle de Acesso Facial"
    }

    # VISUALIZAÇÃO DE FORMATOS IMOBILIÁRIOS
    REAL_ESTATE_FORMATS_DISPLAY = {
        "GUIA_DEFINITIVO": "📘 Guia Definitivo de Compra",
        "LISTA_POLEMICA": "🔥 Mitos vs Verdades (Polêmico)",
        "COMPARATIVO_TECNICO": "⚖️ Comparativo Técnico (Tabela)",
        "INSIGHT_DE_CORRETOR": "💡 Insight de Bastidores (Expert)",
        "PERGUNTAS_RESPOSTAS": "❓ FAQ (Perguntas Frequentes)",
        "DATA_DRIVEN": "📊 Análise Baseada em Dados",
        "CENARIO_ANALITICO": "🔮 Previsão de Cenário Futuro",
        "CHECKLIST_TECNICO": "✅ Checklist de Vistoria/Avaliação",
        "ROTINA_SUGERIDA": "📅 Rotina de Vida (Storytelling)"
    }
    
    # =====================================================
    # 3. MATRIZ DE SINCRONIZAÇÃO (PORTAL)
    # =====================================================
    
    PORTAL_MATRIX = {
        "GIRO_POLICIAL": {
            "label": "🚔 Plantão Policial & Trânsito",
            "topics": ["ACIDENTE_GRAVE", "OPERACAO_POLICIAL", "ALERTAS_DEFESA_CIVIL", "MOBILIDADE_URBANA", "OBRAS_VIARIAS"],
            "formats": ["NOTICIA_IMPACTO", "CHECAGEM_FATOS", "DATA_DRIVEN"]
        },
        "POLITICA_BASTIDORES": {
            "label": "🏛️ Política & Poder",
            "topics": ["CAMARA_MUNICIPAL", "DECISOES_PREFEITURA", "ELEICOES_CENARIOS", "POLEMICA_LEGISLATIVA", "ORCAMENTO_PUBLICO"],
            "formats": ["DOSSIE_INVESTIGATIVO", "EXPLAINER", "ENTREVISTA_PING_PONG", "BASTIDORES_ANALISE"]
        },
        "AGENDA_CULTURAL": {
            "label": "🎉 Viver Indaiatuba (Lazer)",
            "topics": ["SHOWS_EVENTOS", "GASTRONOMIA_NOVIDADES", "PARQUE_ECOLOGICO_LAZER", "ROTEIROS_FIM_DE_SEMANA", "CULTURA_ARTE"],
            "formats": ["LISTA_CURADORIA", "ROTEIRO_EXPERIENCIA", "NOTICIA_SERVICO"]
        },
        "ECONOMIA_LOCAL": {
            "label": "💰 Seu Bolso & Negócios",
            "topics": ["VAGAS_EMPREGO", "NOVAS_EMPRESAS", "MERCADO_IMOBILIARIO", "CUSTO_DE_VIDA", "INAUGURACOES"],
            "formats": ["SERVICO_PASSO_A_PASSO", "DATA_DRIVEN", "LISTA_CURADORIA"]
        },
        "COTIDIANO_CIDADE": {
            "label": "🏘️ Comunidade & Serviços",
            "topics": ["CLIMA_TEMPO", "SAUDE_PUBLICA", "EDUCACAO_ESCOLAS", "CAUSA_ANIMAL", "HISTORIAS_DE_VIDA"],
            "formats": ["SERVICO_PASSO_A_PASSO", "EXPLAINER", "VOZ_DA_RUA"]
        },
        "DESTAQUE_DO_DIA": {
            "label": "⚡ Resumo Diário (Manchete)",
            "topics": ["RESUMO_GERAL", "PRINCIPAIS_MANCHETES"],
            "formats": ["REVISTA_DIGITAL_DIARIA"]
        }
    }

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
    
    # UNIFICAÇÃO PARA FALLBACK
    CONTENT_FORMATS_MAP = {**PORTAL_FORMATS_DISPLAY, **REAL_ESTATE_FORMATS_DISPLAY}
    CONTENT_FORMATS = list(CONTENT_FORMATS_MAP.keys())

    # =====================================================
    # 4. PERSONAS E CATÁLOGOS (ASSETS)
    # =====================================================
    
    PERSONAS = {
        "CITIZEN_GENERAL": {
            "cluster_ref": "PORTAL", 
            "nome": "🗞️ REDAÇÃO (Jornalismo Profissional)",
            "dor": "Desinformação e falta de profundidade.",
            "desejo": "Informação confiável e útil."
        },
        "INVESTOR_SHARK_ROI": {"cluster_ref": "INVESTOR", "nome": "🦈 INVESTIDOR TUBARÃO", "dor": "Risco de Vacância", "desejo": "ROI acima da SELIC"},
        "EXODUS_SP_ELITE_FAMILY": {"cluster_ref": "HIGH_END", "nome": "✈️ FAMÍLIA EXODUS (SP)", "dor": "Segurança e Violência", "desejo": "Qualidade de Vida e Espaço"},
        "FIRST_HOME_DREAMER": {"cluster_ref": "URBAN", "nome": "🔑 1º IMÓVEL (CASAL)", "dor": "Orçamento Apertado", "desejo": "Viabilidade Financeira"},
        "LOGISTICS_MANAGER": {"cluster_ref": "LOGISTICS", "nome": "🚚 GESTOR LOGÍSTICO", "dor": "Custo Last Mile", "desejo": "Eficiência e Acesso"},
        "RURAL_RETIREE": {"cluster_ref": "RURAL_LIFESTYLE", "nome": "🌿 APOSENTADORIA VERDE", "dor": "Barulho e Estresse", "desejo": "Paz e Terra"},
        "CORPORATE_CEO": {"cluster_ref": "CORPORATE", "nome": "👔 CEO / EMPRESÁRIO", "dor": "Imagem da Empresa", "desejo": "Status e Networking"}
    }

    # CATÁLOGO DE ATIVOS IMOBILIÁRIOS (AGRUPADOS PELA CHAVE DO CLUSTER)
    ASSETS_CATALOG = {
        "HIGH_END": ["MANSÃO EM CONDOMÍNIO DE LUXO", "CASA TÉRREA ALTO PADRÃO", "TERRENO DE ALTO PADRÃO", "SOBRADO DE LUXO"],
        "FAMILY": ["CASA EM CONDOMÍNIO (FAMÍLIA)", "SOBRADO COM ÁREA GOURMET", "CASA DE RUA EM BAIRRO PLANEJADO"],
        "URBAN": ["APARTAMENTO 3 DORMITÓRIOS", "STUDIO / LOFT MODERNO", "APARTAMENTO GARDEN", "COBERTURA DUPLEX"],
        "INVESTOR": ["TERRENO EM CONDOMÍNIO (INVESTIMENTO)", "IMÓVEL PARA REFORMA (FLIP)", "LOTE COMERCIAL", "KITNET PARA RENDA"],
        "LOGISTICS": ["GALPÃO INDUSTRIAL AAA", "ÁREA PARA CD LOGÍSTICO", "TERRENO INDUSTRIAL"],
        "RURAL_LIFESTYLE": ["CHÁCARA EM ITAICI", "SÍTIO DE LAZER", "HARAS OU CHÁCARA DE PRODUÇÃO"],
        "CORPORATE": ["SALA COMERCIAL PREMIUM", "LAJE CORPORATIVA", "PRÉDIO MONOUSUÁRIO", "CONSULTÓRIO MÉDICO"]
    }
    
    # CATÁLOGO DO PORTAL
    PORTAL_CATALOG = {
        "DESTAQUE_DIARIO": ["Resumo das Principais Notícias do Dia"], 
        "CIDADE_ALERTA": ["Trânsito e Mobilidade", "Segurança Pública"],
        # ... (simplificado pois usamos a Matrix agora)
    }

    EMOTIONAL_TRIGGERS_MAP = {
        "AUTORIDADE": "👑 Autoridade", "ESCASSEZ": "💎 Escassez",
        "URGENCIA": "🚨 Urgência", "PROVA_SOCIAL": "👥 Prova Social"
    }
