import argparse
import importlib
import os
from core.utils import setup_project_structure
from core.logger import setup_logger

def main():
    # Setup project structure
    setup_project_structure()
    
    # Setup main logger
    logger = setup_logger('main')
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='RPA Bots Manager')
    parser.add_argument('--bot', type=str, required=True, help='Name of the bot to run')
    parser.add_argument('--config', type=str, help='Path to configuration file')
    args = parser.parse_args()
    
    try:
        # Import the bot module
        bot_module = importlib.import_module(f'bots.{args.bot}.bot')
        
        # Create bot instance
        bot_class = getattr(bot_module, f'{args.bot.capitalize()}Bot')
        bot = bot_class()
        
        # Run the bot
        logger.info(f"Starting bot: {args.bot}")
        bot.run()
        logger.info(f"Bot {args.bot} completed successfully")
        
    except ImportError as e:
        logger.error(f"Error importing bot module: {str(e)}")
    except AttributeError as e:
        logger.error(f"Error creating bot instance: {str(e)}")
    except Exception as e:
        logger.error(f"Error running bot: {str(e)}")

if __name__ == '__main__':
    main() 