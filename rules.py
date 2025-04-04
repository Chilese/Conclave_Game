# rules.py
def calculate_initial_votes(factions):
    """Calcula os votos iniciais proporcionalmente ao suporte."""
    candidate_votes = {}
    for faction in factions:
        members = faction.num_members
        total_support = sum(faction.candidate_support.values())
        if total_support > 0:
            for candidate, support in faction.candidate_support.items():
                votes = (support / 100) * members
                candidate_votes[candidate] = candidate_votes.get(candidate, 0) + votes
    return candidate_votes

def adjust_votes_to_total(candidate_votes, total_electors):
    """Ajusta os votos para totalizar exatamente o número de eleitores."""
    current_total = sum(candidate_votes.values())
    if current_total > 0:
        adjustment_factor = total_electors / current_total
        for candidate in candidate_votes:
            candidate_votes[candidate] = int(candidate_votes[candidate] * adjustment_factor)
    return candidate_votes

def correct_final_discrepancy(candidate_votes, total_electors):
    """Corrige qualquer discrepância final nos votos."""
    final_total = sum(candidate_votes.values())
    if final_total != total_electors:
        difference = total_electors - final_total
        top_candidate = max(candidate_votes, key=candidate_votes.get)
        candidate_votes[top_candidate] += difference
    return candidate_votes

def redistribute_support_after_voting(factions, candidate_votes, total_voters, favorite_candidate):
    """Redistribui o suporte com base nos resultados da votação."""
    for faction in factions:
        new_support = {}
        total_votes = sum(candidate_votes.values())
        
        for candidate in faction.candidate_support:
            votes = candidate_votes.get(candidate, 0)
            support_percentage = max(2.0, (votes / total_voters) * 100)
            new_support[candidate] = support_percentage
        
        # Normaliza o suporte
        total_support = sum(new_support.values())
        if total_support > 100:
            factor = 100 / total_support
            for candidate in new_support:
                new_support[candidate] *= factor
        
        # Protege o suporte ao candidato favorito
        if favorite_candidate in new_support:
            new_support[favorite_candidate] = max(20.0, new_support[favorite_candidate] + 10.0)
        
        faction.candidate_support = new_support

def calculate_votes(factions, round_number):
    """Calcula os votos com peso progressivo por rodada."""
    total_electors = sum(faction.num_members for faction in factions)
    candidate_votes = {}
    
    # Aumenta o peso do suporte com o número da rodada
    weight = 1.0 + (round_number * 0.15)  # Aumentado para 0.15
    
    for faction in factions:
        faction_weight = faction.num_members * weight
        for candidate, support in faction.candidate_support.items():
            votes = (support / 100) * faction_weight
            candidate_votes[candidate] = candidate_votes.get(candidate, 0) + votes
    
    # Arredonda os votos para números inteiros
    for candidate in candidate_votes:
        candidate_votes[candidate] = round(candidate_votes[candidate])
    
    candidate_votes = adjust_votes_to_total(candidate_votes, total_electors)
    return correct_final_discrepancy(candidate_votes, total_electors)

def check_majority(candidate_votes, total_voters):
    """
    Verifica se há um vencedor com 2/3 dos votos.
    
    Returns:
        tuple: (vencedor, votos_necessarios, lider_atual)
        - vencedor: Cardinal ou None se não houver vencedor
        - votos_necessarios: número de votos necessários para vitória
        - lider_atual: Cardinal com mais votos atualmente
    """
    if not candidate_votes:
        return None, 0, None
        
    required_majority = int(total_voters * 2 / 3) + 1
    current_leader = max(candidate_votes.items(), key=lambda x: x[1])[0]  # Pega apenas o Cardinal, não os votos
    
    for candidate, votes in candidate_votes.items():
        if votes >= required_majority:
            return candidate, required_majority, current_leader
            
    return None, required_majority, current_leader