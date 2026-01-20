# src/engine.py
import random
from .config import GenesisConfig
from .logic import PlanoDiretor
from .scanner import BlogScanner

class GenesisEngine:
    """
    O 'Maestro'.
    Coordena todos os subsistemas:
    1. Pede dados para o GenesisData (recebido no init)
    2. Consulta o BlogScanner para ver histórico
    3. Aplica a inteligência de SEO (Pesos)
    4. Valida coerência com PlanoDiretor
    """

    def __init__(self, data_instance):
        # O Engine precisa dos dados (bairros), que vêm injetados de fora
        self.data = data_instance
        self.config = GenesisConfig()
        self.plano = PlanoDiretor()
        self.scanner = BlogScanner()

    def run(self, user_selection: dict):
        """
        Executa a geração da pauta com base nas escolhas do usuário (ou aleatórias).
        user_selection espera: {
            "persona_key", "bairro_nome", "topico", "ativo", "formato", "gatilho"
        }
        """
        # 1. Atualiza o Scanner (Espião)
        self.scanner.mapear()
        historico_recente = self.scanner.get_ultimos_titulos(20)

        # =====================================================
        # 1. DEFINIÇÃO DA PERSONA
        # =====================================================
        if user_selection['persona_key'] != "ALEATÓRIO":
            persona_key = user_selection['persona_key']
        else:
            persona_key = random.choice(list(self.config.PERSONAS.keys()))
            
        persona_data = self.config.PERSONAS[persona_key]
        cluster_ref = persona_data.get("cluster_ref", "FAMILY")

        # =====================================================
        # 2. DEFINIÇÃO DO BAIRRO (COM INTEGRIDADE)
        # =====================================================
        bairro_selecionado = None
        modo = "CIDADE"
        obs_tecnica = "Foco Macro (Cidade)"

        # Caso A: Usuário escolheu um bairro manual
        if user_selection['bairro_nome'] != "ALEATÓRIO":
            for b in self.data.bairros:
                if b['nome'] == user_selection['bairro_nome']:
                    bairro_selecionado = b
                    break
            if bairro_selecionado:
                modo = "BAIRRO"
                obs_tecnica = "Bairro Definido pelo Usuário"
        
        # Caso B: Sorteio Inteligente da IA
        else:
            # Filtra bairros que fazem sentido para a Persona (Ex: Rico -> Condomínio)
            candidatos_validos = []
            for b in self.data.bairros:
                z = b.get("zona_normalizada")
                match = False
                # Lógica de Match Persona <-> Zona
                if cluster_ref == "HIGH_END" and z in ["residencial_fechado", "chacaras_fechado"]: match = True
                elif cluster_ref == "FAMILY" and z in ["residencial_fechado", "residencial_aberto", "chacaras_fechado"]: match = True
                elif cluster_ref == "URBAN" and z in ["residencial_aberto", "mista"]: match = True
                elif cluster_ref == "INVESTOR" and z in ["industrial", "residencial_fechado", "mista", "residencial_aberto"]: match = True
                elif cluster_ref == "LOGISTICS" and z in ["industrial"]: match = True
                elif cluster_ref == "CORPORATE" and z in ["mista", "industrial", "residencial_aberto"]: match = True
                
                if match:
                    candidatos_validos.append(b)

            # Sorteio (65% de chance de focar num bairro específico)
            if candidatos_validos:
                if random.random() < 0.65:
                    # Tenta pegar um bairro inédito (não publicado no blog)
                    ineditos = [b for b in candidatos_validos if not self.scanner.ja_publicado(b["nome"])]
                    if ineditos:
                        bairro_selecionado = random.choice(ineditos)
                        obs_tecnica = "Bairro Inédito Compatível (IA)"
                    else:
                        bairro_selecionado = random.choice(candidatos_validos)
                        obs_tecnica = "Bairro Compatível (IA - Já publicado)"
                    modo = "BAIRRO"

        # =====================================================
        # 3. DEFINIÇÃO DO TÓPICO (AQUI ENTRA O SEO INTELIGENTE)
        # =====================================================
        if user_selection['topico'] != "ALEATÓRIO":
            # Se o usuário escolheu manual, respeita
            # (Precisamos achar o nome bonito baseado na chave ou valor)
            topico_nome = user_selection['topico'] 
        else:
            # --- IMPLEMENTAÇÃO DA PROBABILIDADE PONDERADA ---
            keys = list(self.config.TOPICS_MAP.keys())
            
            # Cria a lista de pesos na mesma ordem das chaves
            pesos = [self.config.TOPICS_WEIGHTS[k] for k in keys]
            
            # Sorteia 1 item usando os pesos
            chave_sorteada = random.choices(keys, weights=pesos, k=1)[0]
            topico_nome = self.config.TOPICS_MAP[chave_sorteada]

        # =====================================================
        # 4. DEFINIÇÃO DO ATIVO E REFINAMENTO
        # =====================================================
        if user_selection['ativo'] != "ALEATÓRIO":
            ativo_final = user_selection['ativo']
            obs_ref = "Ativo Definido pelo Usuário"
            # Passa pelo Plano Diretor para validar incoerências físicas
            if bairro_selecionado:
                 ativo_final, obs_ajuste = self.plano.refinar_ativo(cluster_ref, bairro_selecionado, [ativo_final])
                 obs_ref += f" | {obs_ajuste}"
        else:
            # Pega lista de ativos sugeridos para o cluster da persona
            ativo_base_list = self.data.ativos_por_cluster.get(cluster_ref, ["Imóvel Padrão"])
            
            # Se tiver bairro, usa o Plano Diretor para escolher o melhor ativo para aquele local
            if modo == "BAIRRO" and bairro_selecionado:
                ativo_final, obs_ajuste = self.plano.refinar_ativo(cluster_ref, bairro_selecionado, ativo_base_list)
                obs_ref = obs_ajuste
            else:
                ativo_final = random.choice(ativo_base_list)
                obs_ref = "Ativo Aleatório (Sem restrição de bairro)"

        obs_tecnica += f" | {obs_ref}"

        # =====================================================
        # 5. OUTROS SORTEIOS SIMPLES
        # =====================================================
        if user_selection['formato'] != "ALEATÓRIO":
            formato = user_selection['formato']
        else:
            formato = random.choice(self.config.CONTENT_FORMATS)

        if user_selection['gatilho'] != "ALEATÓRIO":
            gatilho = user_selection['gatilho']
        else:
            gatilho = random.choice(self.config.EMOTIONAL_TRIGGERS)

        # Retorna o Pacote de Decisão completo
        return {
            "modo": modo,
            "bairro": bairro_selecionado,
            "cluster_tecnico": cluster_ref,
            "ativo_definido": ativo_final,
            "topico": topico_nome,
            "persona": persona_data,
            "formato": formato,
            "gatilho": gatilho,
            "obs_tecnica": obs_tecnica,
            "historico_titulos": historico_recente
        }