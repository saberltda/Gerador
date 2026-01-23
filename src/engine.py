# src/engine.py
import random
import datetime
# Importa as classes de lógica do arquivo logic.py (onde elas foram definidas corretamente)
from .logic import PlanoDiretor, SEOHeatmap, RiscoJuridico, PortalSynchronizer, RealEstateSynchronizer
from .config import GenesisConfig

class GenesisEngine:
    """
    O 'Cérebro' (Versão 67 - Config Sync).
    Coordena a escolha inteligente dos parâmetros da pauta.
    Agora compatível com a nova estrutura do config.py (PORTAL_CATALOG).
    """
    
    def __init__(self, data_manager):
        self.data = data_manager
        # Instancia as lógicas
        self.plano_diretor = PlanoDiretor()
        self.seo_bot = SEOHeatmap()
        self.juridico = RiscoJuridico()
        # Instancia os sincronizadores para ajudar na seleção
        self.portal_sync = PortalSynchronizer()
        self.imob_sync = RealEstateSynchronizer()

    def run(self, user_inputs):
        """
        Executa o pipeline de decisão:
        1. Identifica o Modo (Portal ou Imobiliária)
        2. Seleciona/Valida Persona
        3. Seleciona/Valida Bairro
        4. Define Ativo, Tópico e Formato (Cruzamento Inteligente)
        """
        
        # 1. MODO DE OPERAÇÃO
        modo = user_inputs.get('tipo_pauta', 'IMOBILIARIA')
        eh_portal = (modo == "PORTAL")

        # 2. SELEÇÃO DE PERSONA
        persona_key = user_inputs.get('persona_key', 'ALEATÓRIO')
        if persona_key == "ALEATÓRIO" or not persona_key:
            if eh_portal:
                persona_key = "CITIZEN_GENERAL" # Persona padrão do Portal
            else:
                # Escolhe uma persona de imobiliária aleatória (excluindo a do portal)
                opcoes = [k for k in GenesisConfig.PERSONAS.keys() if k != "CITIZEN_GENERAL"]
                persona_key = random.choice(opcoes)
        
        persona_obj = GenesisConfig.PERSONAS.get(persona_key, GenesisConfig.PERSONAS["CITIZEN_GENERAL" if eh_portal else "FIRST_HOME_DREAMER"])

        # 3. SELEÇÃO DE BAIRRO
        bairro_nome = user_inputs.get('bairro_nome', 'ALEATÓRIO')
        
        if bairro_nome == "ALEATÓRIO":
            # Escolhe um bairro aleatório da lista carregada
            bairro_obj = random.choice(self.data.bairros)
        elif bairro_nome == "FORCE_CITY_MODE":
            # Modo cidade inteira (comum no Portal)
            bairro_obj = {"nome": "Indaiatuba", "zona_normalizada": "urbana", "slug": "indaiatuba"}
        else:
            # Busca o objeto do bairro selecionado pelo nome
            bairro_obj = next((b for b in self.data.bairros if b['nome'] == bairro_nome), None)
            if not bairro_obj:
                # Fallback se não encontrar
                bairro_obj = {"nome": "Indaiatuba", "zona_normalizada": "urbana", "slug": "indaiatuba"}

        # 4. DEFINIÇÃO DE CONTEÚDO (ATIVO/TÓPICO/FORMATO)
        if eh_portal:
            result_content = self._decide_portal_content(user_inputs)
        else:
            result_content = self._decide_real_estate_content(user_inputs, persona_obj, bairro_obj)

        # 5. MONTAGEM DO PACOTE FINAL
        final_package = {
            "tipo_pauta": modo,
            "persona": persona_obj,
            "bairro": bairro_obj,
            "ativo_definido": result_content['ativo'], # No portal, isso é a Editoria
            "topico": result_content['topico'],
            "formato": result_content['formato'],
            "gatilho": user_inputs.get('gatilho', 'ALEATÓRIO'),
            # Preserva os inputs originais para debug
            "inputs_originais": user_inputs 
        }

        # Refinamento final de gatilho se for aleatório
        if final_package['gatilho'] == 'ALEATÓRIO':
            if eh_portal:
                 final_package['gatilho'] = "NEUTRAL_JOURNALISM"
            else:
                 final_package['gatilho'] = random.choice(list(GenesisConfig.EMOTIONAL_TRIGGERS_MAP.keys()))

        return final_package

    def _decide_portal_content(self, inputs):
        """
        Lógica de decisão para o PORTAL DA CIDADE.
        Substitui a antiga PORTAL_MATRIX pela nova PORTAL_CATALOG.
        """
        
        # A. EDITORIA (Ativo)
        editoria_input = inputs.get('ativo', 'ALEATÓRIO')
        
        if editoria_input != 'ALEATÓRIO' and editoria_input in GenesisConfig.PORTAL_CATALOG:
            editoria_key = editoria_input
        else:
            editoria_key = random.choice(list(GenesisConfig.PORTAL_CATALOG.keys()))
            
        # O "ativo_definido" será o nome legível da editoria (ex: "Polícia") ou um sub-item dela
        # Para simplificar, vamos usar o nome da chave ou um item da lista
        lista_itens = GenesisConfig.PORTAL_CATALOG[editoria_key]
        if lista_itens:
            ativo_final = random.choice(lista_itens) # Ex: "Trânsito e Mobilidade"
        else:
            ativo_final = editoria_key

        # B. TÓPICO (Ângulo)
        topico_input = inputs.get('topico', 'ALEATÓRIO')
        if topico_input != 'ALEATÓRIO' and topico_input in GenesisConfig.PORTAL_TOPICS_MAP:
            topico_final = topico_input
        else:
            topico_final = random.choice(list(GenesisConfig.PORTAL_TOPICS_MAP.keys()))

        # C. FORMATO
        formato_input = inputs.get('formato', 'ALEATÓRIO')
        if formato_input != 'ALEATÓRIO' and formato_input in GenesisConfig.PORTAL_FORMATS_MAP:
            formato_final = formato_input
        else:
            # Tenta combinar formato com tópico (lógica simples)
            if topico_final == "GIRO_NOTICIAS":
                formato_final = "NOTICIA_IMPACTO" # Giro pede notícia rápida ou lista
            elif topico_final == "SERVICO_ESSENCIAL":
                formato_final = "SERVICO_PASSO_A_PASSO"
            else:
                formato_final = random.choice(list(GenesisConfig.PORTAL_FORMATS_MAP.keys()))

        return {
            "ativo": ativo_final,
            "topico": topico_final,
            "formato": formato_final
        }

    def _decide_real_estate_content(self, inputs, persona, bairro):
        """
        Lógica de decisão para IMOBILIÁRIA.
        """
        
        # A. CLUSTER / ATIVO
        cluster_input = inputs.get('ativo', 'ALEATÓRIO') # Aqui vem a chave do cluster (ex: FAMILY)
        sub_ativo_input = inputs.get('sub_ativo', 'ALEATÓRIO')

        # Se o usuário escolheu um cluster específico
        if cluster_input != 'ALEATÓRIO' and cluster_input in GenesisConfig.ASSETS_CATALOG:
            cluster_escolhido = cluster_input
        else:
            # Escolhe cluster baseado na persona (preferência) ou aleatório
            pref = persona.get('cluster_ref')
            if pref and pref in GenesisConfig.ASSETS_CATALOG and random.random() > 0.3:
                cluster_escolhido = pref
            else:
                cluster_escolhido = random.choice(list(GenesisConfig.ASSETS_CATALOG.keys()))

        # Define o ativo final (imóvel específico)
        ativos_disponiveis = GenesisConfig.ASSETS_CATALOG.get(cluster_escolhido, ["Imóvel Padrão"])
        
        if sub_ativo_input != 'ALEATÓRIO' and sub_ativo_input in ativos_disponiveis:
            ativo_base = sub_ativo_input
        else:
            ativo_base = random.choice(ativos_disponiveis)

        # Refinamento Físico (Plano Diretor)
        # Verifica se o imóvel cabe no bairro (ex: não por galpão em bairro residencial)
        ativo_final, _ = self.plano_diretor.refinar_ativo(cluster_escolhido, bairro, [ativo_base])

        # B. TÓPICO
        topico_input = inputs.get('topico', 'ALEATÓRIO')
        if topico_input != 'ALEATÓRIO' and topico_input in GenesisConfig.TOPICS_MAP:
            topico_final = topico_input
        else:
            topico_final = random.choice(list(GenesisConfig.TOPICS_MAP.keys()))

        # C. FORMATO
        formato_input = inputs.get('formato', 'ALEATÓRIO')
        if formato_input != 'ALEATÓRIO' and formato_input in GenesisConfig.REAL_ESTATE_FORMATS_MAP:
            formato_final = formato_input
        else:
            formato_final = random.choice(list(GenesisConfig.REAL_ESTATE_FORMATS_MAP.keys()))

        return {
            "ativo": ativo_final,
            "topico": topico_final,
            "formato": formato_final,
            "cluster_tecnico": cluster_escolhido # Extra info for debug
        }
