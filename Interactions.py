from ui import display_info
import random

class Interactions:
    @staticmethod
    def persuade(player, target, favorite_candidate, factions):
        result = (player.charisma + player.scholarship) - (target.charisma + target.scholarship + target.modifiers["persuasion"])
        if result > 5:
            player.influence = min(100, player.influence + random.randint(3, 7))
            target_faction = next(f for f in factions if f.ideology == target.ideology)
            target_faction.candidate_support[favorite_candidate] = min(100, target_faction.candidate_support.get(favorite_candidate, 0) + 10)
            display_info("Sucesso! Influência aumentada.")
        else:
            player.influence = max(0, player.influence - random.randint(2, 5))
            display_info("Falha! Influência reduzida.")

    @staticmethod
    def propose_alliance(player, target, favorite_candidate, factions):
        result = (player.influence + player.discretion) - (target.influence + target.discretion + target.modifiers["alliance"])
        if result > 5:
            player.influence = min(100, player.influence + random.randint(5, 10))
            target_faction = next(f for f in factions if f.ideology == target.ideology)
            target_faction.candidate_support[favorite_candidate] = min(100, target_faction.candidate_support.get(favorite_candidate, 0) + 15)
            display_info("Sucesso! Aliança formada.")
        else:
            player.discretion = max(0, player.discretion - random.randint(3, 8))
            display_info("Falha! Discrição reduzida.")

    @staticmethod
    def manipulate_rumors(player, target, favorite_candidate, factions, candidates):
        result = (player.discretion + player.scholarship) - (target.discretion + target.scholarship + target.modifiers["rumors"])
        if result > 5:
            player.discretion = min(100, player.discretion + random.randint(4, 8))
            target_faction = next(f for f in factions if f.ideology == target.ideology)
            rival = random.choice([c for c in candidates if c != favorite_candidate])
            target_faction.candidate_support[rival] = max(0, target_faction.candidate_support.get(rival, 0) - 10)
            display_info("Sucesso! Rumores espalhados.")
        else:
            player.influence = max(0, player.influence - random.randint(2, 6))
            display_info("Falha! Influência reduzida.")