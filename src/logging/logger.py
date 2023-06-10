import logging
import ntpath
import os

import fiona
import matplotlib
import open3d

from ..config import Config

matplotlib.set_loglevel("Error")
open3d.utility.set_verbosity_level(open3d.utility.VerbosityLevel.Error)
fiona.log.setLevel('CRITICAL')

filename = ntpath.basename(__name__).replace(".py", "")  # Get filename from filepath, and removes .py from the end
log_save_path = os.path.join(Config.LOG_DIR.value, f"{filename}.log")

# Logger configuration
logging.basicConfig(
    level=Config.LOGGING_LEVEL.value,
)

logger = logging.getLogger(filename)
handler = logging.FileHandler(filename=log_save_path, mode="a")
formatter = logging.Formatter(
    fmt='{:<15}{:<15}{:<15}{:<15}'.format('%(asctime)s', '%(levelname)s', '%(filename)s', '%(message)s'),
    datefmt='%Y-%m-%d %H:%M:%S'
)

handler.setFormatter(formatter)
logger.addHandler(handler)
