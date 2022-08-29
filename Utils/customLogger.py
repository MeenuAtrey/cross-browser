import logging


class LogGen:

    @staticmethod
    def log_gen():
        logger = logging.getLogger(r"./Logs/Edit_cross_browser_regression.log")
        logger.setLevel(logging.INFO)
        fh = logging.FileHandler(r"./Logs/Edit_cross_browser_regression.log", 'w+')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        # add the handlers to logger
        if not logger.handlers:
            logger.addHandler(fh)
        return logger
