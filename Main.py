from src.core.game import Game
from src.utils.game_logging import GameLogger

def main():
    """Função principal que inicia o jogo."""
    logger = GameLogger()
    logger.info("Iniciando Conclave Game")
    
    try:
        game = Game()
        game.run()
    except KeyboardInterrupt:
        logger.info("Jogo interrompido pelo usuário")
    except Exception as e:
        logger.error(f"Erro não esperado: {str(e)}")
    finally:
        logger.info("Encerrando Conclave Game")

if __name__ == "__main__":
    main()