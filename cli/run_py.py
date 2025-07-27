
import os
import subprocess
import logging
import argparse

from lib import get_python_path, get_root_path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(os.path.basename(__file__))


def run_py() -> None:
    parser = argparse.ArgumentParser(description="venv上のpythonで指定ファイルを実行")
    parser.add_argument("script", help="実行するPythonファイルのパス")
    parser.add_argument("args", nargs=argparse.REMAINDER, help="スクリプトに渡す追加引数")
    args = parser.parse_args()

    if not args.script:
        logger.error("実行するPythonファイルを指定してください")
        exit(1)

    cmd = [get_python_path(), args.script] + args.args
    subprocess.run(cmd, shell=False)


if __name__ == "__main__":
    run_py()
