import unittest
from src.events.event_system import EventCondition, ConditionType, EventManager
from src.events.event_effects import Effect, EffectType

class TestEventSystem(unittest.TestCase):
    def setUp(self):
        self.game_state = type('GameState', (), {
            'current_round': 1,
            'player_votes': 5,
            'player_influence': {"Zelanti": 2, "Popolari": 1},
            'alliances': [],
            'reputation': {"Zelanti": 0, "Popolari": 0}
        })()

    def test_condition_check(self):
        condition = EventCondition(
            ConditionType.RODADA,
            {"rodada": 1}
        )
        self.assertTrue(condition.check(self.game_state))

    def test_effect_application(self):
        effect = Effect(
            type=EffectType.MODIFICAR_VOTOS,
            magnitude=2,
            duration=2
        )
        initial_votes = self.game_state.player_votes
        effect.apply(self.game_state)
        self.assertEqual(self.game_state.player_votes, initial_votes + 2)
        self.assertEqual(effect.rounds_remaining, 1)

    def test_condition_description(self):
        condition = EventCondition(
            ConditionType.VOTOS,
            {"min_votos": 10}
        )
        self.assertEqual(condition.get_description(), "Requer 10 votos")

    def test_effect_description(self):
        effect = Effect(
            type=EffectType.ALTERAR_REPUTACAO,
            magnitude=-2,
            duration=3,
            target="Zelanti"
        )
        self.assertEqual(
            effect.get_description(),
            "Piora reputação com Zelanti em 2 por 3 rodadas"
        )

if __name__ == '__main__':
    unittest.main()