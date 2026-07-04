"""SimpleCutPy 入口 — dearpygui 版本。"""

import logging
import sys

from controller.core import CoreController
from ui.app import run

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        encoding="utf-8",
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        filename="SimpleCut.log",
        filemode="w",
    )

    controller = CoreController()
    run(controller)

    sys.exit(0)
