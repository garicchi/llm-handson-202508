import os
import subprocess
import logging

from lib import get_python_path, get_root_path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(os.path.basename(__file__))


def run_black() -> None:
    logging.info("blackを実行します")
    subprocess.run([get_python_path(), "-m", "black", get_root_path()], shell=False)
    logging.info("🍺blackの実行が完了しました")


if __name__ == "__main__":
    run_black()
