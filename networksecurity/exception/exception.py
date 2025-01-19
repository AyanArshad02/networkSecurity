import sys
from networksecurity.logging import logger

class NetworkSecurityException(Exception):

    def __init__(self, error_message, error_detail:sys) -> None:
        """
        Custom exception class for handling network security-related errors.

        Parameters:
        error_message (str): The error message to be displayed.
        error_detail (sys): The sys module for accessing exception details.
        """

        self.error_message = error_message
        _,_,exc_tb = error_detail.exc_info()

        self.lineno=exc_tb.tb_lineno
        self.file_name=exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        """
        String representation of the exception.

        Returns:
        str: A formatted error message with details about the exception.
        """

        return "Error occured in python script name [{0}] line number [{1}] error message [{2}]".format(
            self.file_name,self.lineno,str(self.error_message)
        )


## Checking if logging & exception is working fine or not
# if __name__=='__main__':
#     try:
#         logger.logging.info("Entered try block")
#         a = 2/0
#         print("This should not be printed",a)
#     except Exception as e:
#         raise NetworkSecurityException(e,sys)
