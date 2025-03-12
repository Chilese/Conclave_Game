# rules.py
def calculate_votes(factions, round_number):
    """Calcula os votos dos NPCs com total fixo de 205."""
    candidate_votes = {}
    total_electors = sum(faction.num_members for faction in factions)  # 205 NPCs
    
    # Calcula votos iniciais proporcionalmente ao suporte
    for faction in factions:
        members = faction.num_members
        total_support = sum(faction.candidate_support.values())
        if total_support > 0:
            for candidate, support in faction.candidate_support.items():
                votes = (support / 100) * members
                candidate_votes[candidate] = candidate_votes.get(candidate, 0) + votes

    # Ajusta para totalizar exatamente 205 votos
    current_total = sum(candidate_votes.values())
    if current_total > 0:
        adjustment_factor = total_electors / current_total
        for candidate in candidate_votes:
            candidate_votes[candidate] = int(candidate_votes[candidate] * adjustment_factor)
    
    # Corrige qualquer discrepância final
    final_total = sum(candidate_votes.values())
    if final_total != total_electors:
        difference = total_electors - final_total
        top_candidate = max(candidate_votes, key=candidate_votes.get)
        candidate_votes[top_candidate] += difference
    
    return candidate_votes

def check_majority(candidate_votes, total_voters):
    """Verifica se há um vencedor com 2/3 dos votos."""
    required_majority = int(total_voters * 2 / 3) + 1  # 138 para 206
    for candidate, votes in candidate_votes.items():
        if votes >= required_majority:
            return candidate
    return None