import logging
def setup_logger(name,log_file="my_app.log",level=logging):
    # Create a custom logger
    logger = logging.getLogger(name)

    # Configure the custom logger
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler('my_app.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger