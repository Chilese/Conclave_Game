# rules.py
def calculate_votes(factions):
    candidate_votes = {}
    total_electors = sum(faction.num_members for faction in factions)  # Deve ser 206
    for faction in factions:
        members = faction.num_members
        total_support = sum(faction.candidate_support.values())
        if total_support > 0:
            for candidate, support in faction.candidate_support.items():
                votes = (support / 100) * members
                candidate_votes[candidate] = candidate_votes.get(candidate, 0) + votes

    # Ajustar para garantir que o total seja exatamente total_electors (206)
    current_total = sum(candidate_votes.values())
    if current_total > 0:
        adjustment_factor = total_electors / current_total
        for candidate in candidate_votes:
            candidate_votes[candidate] = round(candidate_votes[candidate] * adjustment_factor)
    
    return candidate_votes

def check_majority(candidate_votes, total_voters):
    required_majority = int(total_voters * 2 / 3) + 1
    for candidate, votes in candidate_votes.items():
        if votes >= required_majority:
            return candidate
    return None