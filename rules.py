def calculate_votes(factions, num_members_per_faction=60):
    candidate_votes = {}
    for faction in factions:
        for candidate, support in faction.candidate_support.items():
            votes = int(support / 100 * num_members_per_faction)
            if candidate in candidate_votes:
                candidate_votes[candidate] += votes
            else:
                candidate_votes[candidate] = votes
    return candidate_votes

def check_majority(candidate_votes, total_voters, majority_rule="simple"):
    required_majority = total_voters // 2 + 1 if majority_rule == "simple" else int(total_voters * 2 / 3) + 1
    for candidate, votes in candidate_votes.items():
        if votes >= required_majority:
            return candidate
    return None