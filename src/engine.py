# src/engine.py
import random
import copy
from .database import GenesisData
from .logic import PlanoDiretor, SEOHeatmap, RiscoJuridico
from .scanner import BlogScanner
from .config import GenesisConfig

class GenesisEngine:
    def __init__(self, data_instance):
        self.data = data_instance # Recebe instância de GenesisData (database.py)
        self.plano = PlanoDiretor()
        self.heatmap = SEOHeatmap()
        self.risco_juridico = RiscoJuridico()
        self.scanner = BlogScanner()
        self.log_file = "historico_geracao.csv"

    def _selecionar_persona(self, cluster_key):
        """
        Inteligência de Match: Seleciona uma persona que faça sentido 
        para o Cluster Técnico (Tipo de Imóvel) sorteado.
        """
        candidatos = []
        for chave, persona in GenesisConfig.PERSONAS.items():
            refs = persona['cluster_ref']
            # Normaliza para lista se for string única
            if not isinstance(refs, list):
                refs = [refs]
            
            if cluster_key in refs:
                candidatos.append(persona)
        
        if candidatos:
            # Sorteio entre os candidatos compatíveis (ex: para High End, pode ser Old Money ou Exodus)
            return random.choice(candidatos)
        
        # Fallback de segurança
        return GenesisConfig.PERSONAS["CITIZEN_GENERAL"]

    def run(self, user_selection: dict):
        """
        Executa a geração com base na seleção do usuário (Streamlit).
        """
        # 1. Atualiza Scanner (Anti-Canibalismo)
        self.scanner.mapear()
        historico_recente = self.scanner.get_ultimos_titulos(20)

        tipo_pauta_code = user_selection.get("tipo_pauta", "IMOBILIARIA")
        eh_portal = (tipo_pauta_code == "PORTAL")

        # 2. Definição da Persona (Manual ou Automática)
        if user_selection['persona_key'] != "ALEATÓRIO":
            # Usuário escolheu manualmente no menu
            key = user_selection['persona_key']
            persona_data = GenesisConfig.PERSONAS[key]
            
            # Se a persona tem múltiplos clusters, escolhe um principal para guiar o ativo
            cluster_ref = persona_data['cluster_ref'][0] if isinstance(persona_data['cluster_ref'], list) else persona_data['cluster_ref']
        else:
            # Modo Aleatório: A persona será definida DEPOIS de escolher o Cluster do imóvel (passo 4)
            # para garantir coerência. Definimos um placeholder aqui.
            persona_data = None 
            cluster_ref = "FAMILY" # Default temp

        # 3. Definição do Bairro
        bairro_selecionado = None
        modo = "CIDADE"
        obs_tecnica = "Foco Macro"

        if user_selection['bairro_nome'] != "ALEATÓRIO":
            if user_selection['bairro_nome'] == "FORCE_CITY_MODE":
                modo = "CIDADE"
            else:
                for b in self.data.bairros:
                    if b['nome'] == user_selection['bairro_nome']:
                        bairro_selecionado = b
                        break
                if bairro_selecionado:
                    modo = "BAIRRO"
                    obs_tecnica = "Bairro Definido Usuário"
        else:
            # Sorteio inteligente de bairro
            # (Aqui poderíamos filtrar bairros por cluster se a Persona já estivesse definida)
            pool = [b for b in self.data.bairros]
            
            # Tenta pegar um bairro inédito (Scanner)
            ineditos = [b for b in pool if not self.scanner.ja_publicado(b["nome"])]
            
            if ineditos and random.random() < 0.7:
                 bairro_selecionado = random.choice(ineditos)
                 obs_tecnica = "Bairro Inédito (IA)"
            else:
                 bairro_selecionado = random.choice(pool)
                 obs_tecnica = "Bairro Recorrente (IA)"
            
            if bairro_selecionado:
                modo = "BAIRRO"

        # 4. Definição de Cluster e Ativo
        # Se a persona já foi escolhida manualmente, respeitamos o cluster dela.
        # Se for ALEATORIO, sorteamos um cluster do banco de dados primeiro.
        
        if not persona_data:
            # Sorteio do Cluster Imobiliário (ex: HIGH_END, LOGISTICS)
            clusters_db = list(self.data.ativos_por_cluster.keys())
            cluster_ref = random.choice(clusters_db)
            
            # AGORA escolhemos a persona compatível com esse cluster
            persona_data = self._selecionar_persona(cluster_ref)
        
        # Agora sorteamos o ativo dentro desse cluster
        if user_selection['ativo'] != "ALEATÓRIO":
            ativo_final = user_selection['ativo']
            obs_ref = "Ativo Manual"
        else:
            if eh_portal:
                lista_portal = []
                for l in self.data.ativos_portal.values(): lista_portal.extend(l)
                ativo_final = random.choice(lista_portal)
                obs_ref = "Notícia Portal"
            else:
                lista_ativos = self.data.ativos_por_cluster.get(cluster_ref, ["Imóvel Padrão"])
                # Refinamento Lógico (Plano Diretor)
                if modo == "BAIRRO" and bairro_selecionado:
                    ativo_final, obs_ajuste = self.plano.refinar_ativo(cluster_ref, bairro_selecionado, lista_ativos)
                    obs_ref = obs_ajuste
                else:
                    ativo_final = random.choice(lista_ativos)
                    obs_ref = "Sorteio Simples"

        obs_tecnica += f" | {obs_ref}"

        # 5. Tópico, Formato e Gatilho
        if user_selection['topico'] != "ALEATÓRIO":
            topico = user_selection['topico']
        else:
            topico = random.choice(list(GenesisConfig.TOPICS_MAP.values()))

        if user_selection['formato'] != "ALEATÓRIO":
            formato = user_selection['formato']
        else:
            formato = random.choice(GenesisConfig.CONTENT_FORMATS)
            
        if user_selection['gatilho'] != "ALEATÓRIO":
            gatilho = user_selection['gatilho']
        else:
            gatilho = random.choice(GenesisConfig.EMOTIONAL_TRIGGERS)

        return {
            "modo": modo,
            "bairro": bairro_selecionado,
            "cluster_tecnico": cluster_ref,
            "ativo_definido": ativo_final,
            "topico": topico,
            "persona": persona_data,
            "formato": formato,
            "gatilho": gatilho,
            "obs_tecnica": obs_tecnica,
            "historico_titulos": historico_recente,
            "tipo_pauta": tipo_pauta_code
        }
