import logging
import traceback

from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler

# Get the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler = logging.FileHandler("logs/400_errors.log")
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def custom_exception_handler(exc, context):
    # Log the error if it's not a validation error
    if isinstance(exc, ValidationError):
        tb = traceback.format_tb(exc.__traceback__)
        error_msg = f"ValidationError occurred: {exc} \n{''.join(tb)}"
        logger.error(error_msg)

    return exception_handler(exc, context=context)
