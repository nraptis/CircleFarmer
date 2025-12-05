# main.py  (only showing changed / relevant bits)

from __future__ import annotations

import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
)
from PySide6.QtCore import QSize

from top_left_panel import TopLeftPanel
from top_center_panel import TopCenterPanel
from top_right_panel import TopRightPanel
from middle_left_panel import MiddleLeftPanel      # <-- NEW
from home_view import HomeView

from runner_params import RunnerParams
from runner import Runner

from trial import trial
from trial2 import trial2
from trial3 import trial3
from trial4 import trial4


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Data Spoofer")
        self.resize(QSize(1024, 768))

        central = QWidget(self)
        self.setCentralWidget(central)

        root_layout = QVBoxLayout(central)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # --------------------------------------------------
        # TOP ROW + PADDING CONTAINER
        # --------------------------------------------------
        top_container = QWidget(central)
        top_container_layout = QHBoxLayout(top_container)
        top_container_layout.setContentsMargins(16, 32, 16, 0)
        top_container_layout.setSpacing(0)

        top_row = QHBoxLayout()
        top_row.setContentsMargins(0, 0, 0, 0)
        top_row.setSpacing(0)

        self.top_left_panel = TopLeftPanel(top_container)
        self.top_center_panel = TopCenterPanel(top_container)
        self.top_right_panel = TopRightPanel(top_container)

        top_row.addWidget(self.top_left_panel)
        top_row.addStretch(1)
        top_row.addWidget(self.top_center_panel)
        top_row.addStretch(1)
        top_row.addWidget(self.top_right_panel)

        top_container_layout.addLayout(top_row)
        root_layout.addWidget(top_container)

        # --------------------------------------------------
        # MIDDLE ROW (MiddleLeftPanel only for now)
        # --------------------------------------------------
        middle_container = QWidget(central)
        middle_layout = QHBoxLayout(middle_container)
        middle_layout.setContentsMargins(16, 8, 16, 0)
        middle_layout.setSpacing(0)

        self.middle_left_panel = MiddleLeftPanel(middle_container)

        middle_layout.addWidget(self.middle_left_panel)
        middle_layout.addStretch(1)   # rest is empty for now

        root_layout.addWidget(middle_container)

        # --------------------------------------------------
        # BOTTOM CONTENT (HOME VIEW)
        # --------------------------------------------------
        self.home_view = HomeView(central)
        root_layout.addWidget(self.home_view, 1)

        self.home_view.generate_test_requested.connect(self.on_generate_test_requested)
        self.home_view.generate_train_requested.connect(self.on_generate_train_requested)

        trial()
        trial2()
        # trial3()
        # trial4()

    # ------------------------------------------------------
    # Helper: collect all params from the panels
    # ------------------------------------------------------
    def build_runner_params(self) -> RunnerParams:
        left = self.top_left_panel
        center = self.top_center_panel
        right = self.top_right_panel
        middle = self.middle_left_panel

        leading_zeros_text = center.leading_zeros() or "0"
        try:
            leading_zeros = int(leading_zeros_text)
        except ValueError:
            leading_zeros = 0

        return RunnerParams(
            # TopLeftPanel
            alpha_min=left.alpha_min(),
            alpha_max=left.alpha_max(),
            alpha_noise=left.alpha_noise(),
            color_noise=left.color_noise(),

            # TopCenterPanel
            file_name_base=center.file_name_base(),
            training_postfix=center.training_postfix(),
            testing_postfix=center.testing_postfix(),
            leading_zeros=leading_zeros,

            # TopRightPanel
            target_min=right.target_min(),
            target_max=right.target_max(),
            max_overlap=right.max_overlap(),
            max_tries=right.max_tries(),

            # MiddleLeftPanel
            output_width=middle.output_width(),
            output_height=middle.output_height(),
            start_index=middle.start_index(),
            end_index=middle.end_index(),
        )

    
    # ------------------------------------------------------
    # Handlers for HomeView signals
    # ------------------------------------------------------
    def on_generate_test_requested(self) -> None:
        try:
            params = self.build_runner_params()
            params.validate()
        except ValueError as e:
            QMessageBox.warning(self, "Invalid parameters", str(e))
            return
        Runner.run_test(params)

    def on_generate_train_requested(self) -> None:
        try:
            params = self.build_runner_params()
            params.validate()
        except ValueError as e:
            QMessageBox.warning(self, "Invalid parameters", str(e))
            return
        Runner.run_train(params)


def main() -> None:
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
