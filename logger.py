import logging

def get_logger():
    formatter_info = logging.Formatter("%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s")

    logger_info = logging.getLogger("main")
    handler_info = logging.FileHandler("info.log", mode="a",encoding="utf-8")
    handler_info.setFormatter(formatter_info)
    logger_info.setLevel(logging.INFO)
    logger_info.addHandler(handler_info)

    return logger_info