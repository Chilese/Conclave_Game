def normalize_support(support_dict, min_value=2.0):
    """Normaliza os valores de suporte garantindo total 100% e valor mínimo por facção."""
    if not support_dict:
        return
        
    # Primeiro aplica o valor mínimo
    for candidate in support_dict:
        if support_dict[candidate] < min_value:
            support_dict[candidate] = min_value
    
    # Calcula o total atual
    total = sum(support_dict.values())
    
    # Se o total for zero, distribui igualmente
    if total <= 0:
        equal_share = 100.0 / len(support_dict)
        for candidate in support_dict:
            support_dict[candidate] = equal_share
        return
    
    # Normaliza para 100%
    factor = 100.0 / total
    remaining = 100.0
    
    # Aplica o fator mantendo o valor mínimo
    for candidate in list(support_dict.keys())[:-1]:  # Processa todos menos o último
        value = max(min_value, support_dict[candidate] * factor)
        support_dict[candidate] = round(value, 2)
        remaining -= support_dict[candidate]
    
    # O último candidato recebe o restante para garantir soma 100%
    last_candidate = list(support_dict.keys())[-1]
    support_dict[last_candidate] = round(remaining, 2)
    
    # Garante que o último valor também respeita o mínimo
    if support_dict[last_candidate] < min_value:
        support_dict[last_candidate] = min_value
        # Renormaliza os outros valores proporcionalmente
        total_others = sum(support_dict[k] for k in support_dict if k != last_candidate)
        if total_others > 0:
            factor = (100 - min_value) / total_others
            for candidate in support_dict:
                if candidate != last_candidate:
                    support_dict[candidate] = round(support_dict[candidate] * factor, 2)

def distribute_members_among_factions(total_members, num_factions):
    """Distribui membros entre facções de forma equilibrada."""
    base_members = total_members // num_factions
    remainder = total_members % num_factions
    distribution = [base_members] * num_factions
    for i in range(remainder):
        distribution[i] += 1
    return distribution

def calculate_votes(factions, round_number):
    """Calcula os votos com peso progressivo por rodada."""
    total_electors = sum(faction.num_members for faction in factions)
    candidate_votes = {}
    
    # O peso da rodada agora tem um impacto mais significativo
    round_weight = 1.0 + (round_number - 1) * 0.5  # 50% de aumento por rodada
    
    # Primeiro passo: calcula os votos considerando o suporte e o peso da rodada
    for faction in factions:
        for candidate, support in faction.candidate_support.items():
            if candidate not in candidate_votes:
                candidate_votes[candidate] = 0
            
            # Aplica peso da rodada de forma quadrática para maiores suportes
            weighted_support = support * (1 + (support / 100) * (round_weight - 1))
            votes = (weighted_support / 100.0) * faction.num_members
            candidate_votes[candidate] += votes
    
    # Normalização para manter o total de eleitores
    total_votes = sum(candidate_votes.values())
    if total_votes > 0:
        scaling_factor = total_electors / total_votes
        for candidate in candidate_votes:
            candidate_votes[candidate] = round(candidate_votes[candidate] * scaling_factor)
    
    # Ajuste final para garantir o total exato
    return correct_final_discrepancy(candidate_votes, total_electors)

def adjust_votes_to_total(candidate_votes, total_electors):
    """Ajusta os votos para totalizar exatamente o número de eleitores."""
    current_total = sum(candidate_votes.values())
    if current_total > 0:
        adjustment_factor = total_electors / current_total
        for candidate in candidate_votes:
            candidate_votes[candidate] = int(candidate_votes[candidate] * adjustment_factor)
    return correct_final_discrepancy(candidate_votes, total_electors)

def correct_final_discrepancy(candidate_votes, total_electors):
    """Corrige qualquer discrepância final nos votos."""
    final_total = sum(candidate_votes.values())
    if final_total != total_electors:
        difference = total_electors - final_total
        top_candidate = max(candidate_votes, key=candidate_votes.get)
        candidate_votes[top_candidate] += difference
    return candidate_votes

def check_majority(candidate_votes, total_voters):
    """Verifica se há um vencedor com 2/3 dos votos."""
    if not candidate_votes:
        return None, 0, None
        
    required_majority = int(total_voters * 2 / 3) + 1
    current_leader = max(candidate_votes.items(), key=lambda x: x[1])[0]
    
    for candidate, votes in candidate_votes.items():
        if votes >= required_majority:
            return candidate, required_majority, current_leader
            
    return None, required_majority, current_leader