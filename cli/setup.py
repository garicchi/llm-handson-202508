import os
import subprocess
import logging

from core import get_pip_path, get_root_path, get_venv_path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(os.path.basename(__file__))


def create_venv() -> None:
    venv_dir = get_venv_path()

    if os.path.exists(venv_dir):
        logger.info("すでにvenvが存在します")
        return

    logger.info("venvを作成します")
    subprocess.run(["python", "-m", "venv", venv_dir], shell=False)
    logger.info("🍺venvが作成されました")


def install_dependencies() -> None:
    requirements = os.path.join(get_root_path(), "requirements.txt")

    if not os.path.exists(get_venv_path()):
        logger.error("venvが存在しません。先にcreate_venv()を実行してください")
        exit(1)

    pip_path = get_pip_path()
    if not os.path.exists(pip_path):
        logger.error("pipが見つかりません")
        exit(1)

    if not os.path.exists(requirements):
        logger.error("requirements.txtが見つかりません")
        exit(1)

    logger.info("依存パッケージをインストールします")
    subprocess.run([pip_path, "install", "-r", requirements], shell=False)
    logger.info("🍺依存パッケージのインストールが完了しました")


if __name__ == "__main__":
    create_venv()
    install_dependencies()
