import os
import subprocess
import logging

from core import get_root_path, get_venv_python_path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(os.path.basename(__file__))


def run_black() -> None:
    logging.info("blackを実行します")
    subprocess.run([get_venv_python_path(), "-m", "black", get_root_path()], shell=False)
    logging.info("🍺blackの実行が完了しました")


if __name__ == "__main__":
    run_black()
