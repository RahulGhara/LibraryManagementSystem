import logging

LOG_FORMAT = '%(levelname)s %(asctime)s - %(message)s'
logging.basicConfig(filename= 'LibraryManagementSysytem_logger.log', level= logging.DEBUG , format= LOG_FORMAT, filemode='w')
logger = logging.getLogger()