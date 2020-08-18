import logging
logging.basicConfig(filename='app.log', filemode='w', format='%(process)d-%(levelname)s-%(message)s')
logger = logging.getLogger()
logger.warning('Cedears Start')

def log(str):
    print(str)
    logger.warning(str)