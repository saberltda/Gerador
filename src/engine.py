# src/engine.py
import random
import copy
from .database import GenesisData
from .logic import PlanoDiretor, SEOHeatmap, RiscoJuridico
from .scanner import BlogScanner
from .config import GenesisConfig

class GenesisEngine:
    def __init__(self, data_instance):
        self.data = data_instance 
        self.plano = PlanoDiretor()
        self.heatmap = SEOHeatmap()
        self.risco_juridico = RiscoJuridico()
        self.scanner = BlogScanner()

    def _selecionar_persona_compativel(self, cluster_key):
        """
        Encontra uma persona que tenha interesse no cluster sorteado.
        """
        candidatos = []
        for chave, persona in GenesisConfig.PERSONAS.items():
            refs = persona['cluster_ref']
            if not isinstance(refs, list): refs = [refs]
            
            if cluster_key in refs:
                candidatos.append(persona)
        
        if candidatos:
            return random.choice(candidatos)
        # Fallback inteligente: Se falhar, usa o Pet Parent (alta conversão) ou Cidadão
        return GenesisConfig.PERSONAS.get("PET_PARENT_PREMIUM", GenesisConfig.PERSONAS["CITIZEN_GENERAL"])

    def _filtrar_bairros_por_cluster(self, cluster_key):
        todos_bairros = self.data.bairros
        candidatos = []

        for b in todos_bairros:
            z = b.get("zona_normalizada", "indefinido")
            match = False
            
            if cluster_key == "HIGH_END":
                if z in ["residencial_fechado", "chacaras_fechado"]: match = True
            elif cluster_key == "FAMILY":
                if z in ["residencial_fechado", "residencial_aberto", "chacaras_fechado"]: match = True
            elif cluster_key == "URBAN":
                if z in ["residencial_aberto", "mista"]: match = True
            elif cluster_key == "INVESTOR":
                if z in ["industrial", "residencial_fechado", "mista", "residencial_aberto"]: match = True
            elif cluster_key == "LOGISTICS":
                if z in ["industrial", "mista"]: match = True
            elif cluster_key == "CORPORATE":
                if z in ["mista", "industrial", "residencial_aberto"]: match = True
            elif cluster_key == "RURAL_LIFESTYLE":
                if "chacara" in z: match = True

            if match:
                candidatos.append(b)

        return candidatos if candidatos else todos_bairros

    def _escolher_topico_ponderado(self):
        """
        Usa os pesos definidos em TOPICS_WEIGHTS para priorizar pautas de alta conversão.
        """
        opcoes = []
        pesos = []
        
        for key, nome_display in GenesisConfig.TOPICS_MAP.items():
            opcoes.append(nome_display)
            # Pega o peso do config, default 50 se não existir
            pesos.append(GenesisConfig.TOPICS_WEIGHTS.get(key, 50))
            
        return random.choices(opcoes, weights=pesos, k=1)[0]

    def run(self, user_selection: dict):
        # 1. Scanner
        self.scanner.mapear()
        historico_recente = self.scanner.get_ultimos_titulos(20)

        tipo_pauta_code = user_selection.get("tipo_pauta", "IMOBILIARIA")
        eh_portal = (tipo_pauta_code == "PORTAL")

        # --- PASSO 1: CLUSTER & PERSONA ---
        persona_data = None
        cluster_ref = "FAMILY" 

        if user_selection['persona_key'] != "ALEATÓRIO":
            key = user_selection['persona_key']
            persona_data = GenesisConfig.PERSONAS[key]
            cluster_ref = persona_data['cluster_ref']
        else:
            # Sorteio do Cluster com leve viés para High Ticket
            clusters_disponiveis = list(self.data.ativos_por_cluster.keys())
            pesos_cluster = []
            for c in clusters_disponiveis:
                if c in ["HIGH_END", "INVESTOR", "LOGISTICS"]: pesos_cluster.append(2.0) # Dobro de chance
                else: pesos_cluster.append(1.0)
            
            cluster_ref = random.choices(clusters_disponiveis, weights=pesos_cluster, k=1)[0]
            persona_data = self._selecionar_persona_compativel(cluster_ref)

        # --- PASSO 2: BAIRRO ---
        bairro_selecionado = None
        modo = "CIDADE"
        obs_tecnica = f"Cluster: {cluster_ref}"

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
                    obs_tecnica += " | Bairro Manual"
        else:
            candidatos = self._filtrar_bairros_por_cluster(cluster_ref)
            ineditos = [b for b in candidatos if not self.scanner.ja_publicado(b["nome"])]
            
            if ineditos and random.random() < 0.75:
                 bairro_selecionado = random.choice(ineditos)
                 obs_tecnica += " | Bairro Inédito (Smart SEO)"
            elif candidatos:
                 bairro_selecionado = random.choice(candidatos)
                 obs_tecnica += " | Bairro Recorrente"
            
            if bairro_selecionado:
                modo = "BAIRRO"

        # --- PASSO 3: ATIVO ---
        if user_selection['ativo'] != "ALEATÓRIO":
            ativo_final = user_selection['ativo']
            obs_ref = "Ativo Manual"
            if modo == "BAIRRO" and bairro_selecionado:
                 ativo_final, obs_ajuste = self.plano.refinar_ativo(cluster_ref, bairro_selecionado, [ativo_final])
                 obs_ref += f" ({obs_ajuste})"
        else:
            if eh_portal:
                lista_portal = []
                for l in self.data.ativos_portal.values(): lista_portal.extend(l)
                ativo_final = random.choice(lista_portal)
                obs_ref = "Notícia Portal"
            else:
                lista_ativos = self.data.ativos_por_cluster.get(cluster_ref, ["IMÓVEL PADRÃO"])
                ativo_base = random.choice(lista_ativos)
                
                if modo == "BAIRRO" and bairro_selecionado:
                    ativo_final, obs_ajuste = self.plano.refinar_ativo(cluster_ref, bairro_selecionado, [ativo_base])
                    obs_ref = obs_ajuste
                else:
                    ativo_final = ativo_base
                    obs_ref = "Sorteio Simples"

        obs_tecnica += f" | {obs_ref}"

        # --- PASSO 4: FLAVOR TEXT (COM INTELIGÊNCIA PONDERADA) ---
        
        # 4.1 Ângulo Editorial (Topico)
        if user_selection['topico'] != "ALEATÓRIO": 
            topico = user_selection['topico']
        else: 
            # AGORA USA OS PESOS DE SEO (Mais "ROI", menos "Genérico")
            topico = self._escolher_topico_ponderado()

        # 4.2 Formato
        if user_selection['formato'] != "ALEATÓRIO": formato = user_selection['formato']
        else: formato = random.choice(GenesisConfig.CONTENT_FORMATS)
            
        # 4.3 Gatilho
        if user_selection['gatilho'] != "ALEATÓRIO": gatilho = user_selection['gatilho']
        else: gatilho = random.choice(GenesisConfig.EMOTIONAL_TRIGGERS)

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
