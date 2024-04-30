import os

from dotenv import load_dotenv
import fire
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from loguru import logger
from sqlalchemy.orm import Session


class BootStrap:
    def prepare_training_data(self, bot_name: str):
        Base = automap_base()

        logger.info('连接数据库......')
        engine = create_engine(os.getenv('CORUPS_DATABASE_URL'))

        logger.info('准备数据......')
        Base.prepare(autoload_with=engine)
        session = Session(engine)
        OpsPilotBot = Base.classes.ops_pilot_bot
        # filter bot via bot_name
        bot = session.query(OpsPilotBot).filter(OpsPilotBot.name == bot_name).first()
        logger.info(f'Bot: {bot.name}')


if __name__ == "__main__":
    load_dotenv()
    fire.Fire(BootStrap)
