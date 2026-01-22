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
        Ex: Se cluster='LOGISTICS', retorna 'COMMERCIAL_LOGISTICS_BOSS'.
        """
        candidatos = []
        for chave, persona in GenesisConfig.PERSONAS.items():
            refs = persona['cluster_ref']
            if not isinstance(refs, list): refs = [refs]
            
            if cluster_key in refs:
                candidatos.append(persona)
        
        if candidatos:
            return random.choice(candidatos)
        return GenesisConfig.PERSONAS["CITIZEN_GENERAL"] # Fallback

    def _filtrar_bairros_por_cluster(self, cluster_key):
        """
        Retorna apenas bairros cujo zoneamento faz sentido para o cluster.
        Evita alucinações (ex: Mansão em Distrito Industrial).
        """
        todos_bairros = self.data.bairros
        candidatos = []

        # Regras de Compatibilidade (Zoneamento Inteligente)
        for b in todos_bairros:
            z = b.get("zona_normalizada", "indefinido")
            match = False
            
            if cluster_key == "HIGH_END":
                if z in ["residencial_fechado", "chacaras_fechado"]: match = True
            
            elif cluster_key == "FAMILY":
                # Família aceita aberto ou fechado, mas evita industrial
                if z in ["residencial_fechado", "residencial_aberto", "chacaras_fechado"]: match = True
            
            elif cluster_key == "URBAN":
                # Foco em apartamentos/casas de rua
                if z in ["residencial_aberto", "mista"]: match = True
            
            elif cluster_key == "INVESTOR":
                # Investidor olha tudo (terreno em aberto, fechado ou industrial)
                if z in ["industrial", "residencial_fechado", "mista", "residencial_aberto"]: match = True
            
            elif cluster_key == "LOGISTICS":
                if z in ["industrial", "mista"]: match = True
            
            elif cluster_key == "CORPORATE":
                if z in ["mista", "industrial", "residencial_aberto"]: match = True
                
            elif cluster_key == "RURAL_LIFESTYLE":
                if "chacara" in z: match = True

            if match:
                candidatos.append(b)

        # Se o filtro for muito restritivo e não achar nada, retorna tudo (fallback seguro)
        return candidatos if candidatos else todos_bairros

    def run(self, user_selection: dict):
        """
        Execução Otimizada: Cluster -> Persona -> Bairro -> Ativo
        """
        # 1. Scanner (Anti-Repetição)
        self.scanner.mapear()
        historico_recente = self.scanner.get_ultimos_titulos(20)

        tipo_pauta_code = user_selection.get("tipo_pauta", "IMOBILIARIA")
        eh_portal = (tipo_pauta_code == "PORTAL")

        # --- PASSO 1: DEFINIR O CLUSTER (A INTENÇÃO) ---
        # O Cluster guia tudo. Se a persona for manual, o cluster vem dela.
        # Se for aleatória, sorteamos o cluster PRIMEIRO.
        
        persona_data = None
        cluster_ref = "FAMILY" # Default

        if user_selection['persona_key'] != "ALEATÓRIO":
            # Persona Manual
            key = user_selection['persona_key']
            persona_data = GenesisConfig.PERSONAS[key]
            cluster_ref = persona_data['cluster_ref']
        else:
            # Persona Aleatória -> Sorteamos o Cluster primeiro
            clusters_disponiveis = list(self.data.ativos_por_cluster.keys())
            
            # Peso SEO: Dá uma leve preferência para clusters de alto valor (High End/Investor)
            # 2x chance para HIGH_END e INVESTOR
            pesos = []
            for c in clusters_disponiveis:
                if c in ["HIGH_END", "INVESTOR"]: pesos.append(c); pesos.append(c)
                else: pesos.append(c)
            
            cluster_ref = random.choice(pesos)
            
            # Agora define a persona baseada no cluster
            persona_data = self._selecionar_persona_compativel(cluster_ref)

        # --- PASSO 2: DEFINIR O BAIRRO (FILTRADO PELO CLUSTER) ---
        bairro_selecionado = None
        modo = "CIDADE"
        obs_tecnica = f"Cluster: {cluster_ref}"

        if user_selection['bairro_nome'] != "ALEATÓRIO":
            # Bairro Manual
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
            # Bairro Aleatório (AGORA FILTRADO)
            candidatos = self._filtrar_bairros_por_cluster(cluster_ref)
            
            # Tenta pegar um bairro inédito no blog
            ineditos = [b for b in candidatos if not self.scanner.ja_publicado(b["nome"])]
            
            if ineditos and random.random() < 0.75: # 75% de chance de priorizar inédito
                 bairro_selecionado = random.choice(ineditos)
                 obs_tecnica += " | Bairro Inédito (Smart SEO)"
            else:
                 bairro_selecionado = random.choice(candidatos)
                 obs_tecnica += " | Bairro Recorrente (Smart SEO)"
            
            if bairro_selecionado:
                modo = "BAIRRO"

        # --- PASSO 3: DEFINIR O ATIVO (COM ATENÇÃO AO MAIÚSCULO) ---
        if user_selection['ativo'] != "ALEATÓRIO":
            ativo_final = user_selection['ativo']
            obs_ref = "Ativo Manual"
            # Validação cruzada rápida
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
                
                # Sorteio do ativo base
                ativo_base = random.choice(lista_ativos)
                
                # Refinamento Lógico (Plano Diretor)
                if modo == "BAIRRO" and bairro_selecionado:
                    ativo_final, obs_ajuste = self.plano.refinar_ativo(cluster_ref, bairro_selecionado, [ativo_base])
                    obs_ref = obs_ajuste
                else:
                    ativo_final = ativo_base
                    obs_ref = "Sorteio Simples"

        obs_tecnica += f" | {obs_ref}"

        # --- PASSO 4: FLAVOR TEXT (TÓPICO, FORMATO, GATILHO) ---
        if user_selection['topico'] != "ALEATÓRIO": topico = user_selection['topico']
        else: topico = random.choice(list(GenesisConfig.TOPICS_MAP.values()))

        if user_selection['formato'] != "ALEATÓRIO": formato = user_selection['formato']
        else: formato = random.choice(GenesisConfig.CONTENT_FORMATS)
            
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
