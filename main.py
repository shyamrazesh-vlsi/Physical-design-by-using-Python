#!/usr/bin/env python3
"""
Universal RPT Analyzer - Main Entry Point
For all Innovus report types (Timing, Power, Area, etc.)
"""

import sys
import logging
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from gui.main_window import MainWindow
from core.universal_parser import UniversalParser
from core.report_detector import ReportDetector
from utils.file_utils import setup_logging


class RPTAnalyzer:
    """Main application class"""

    def __init__(self):
        self.logger = None
        self.parser = None
        self.detector = None
        self.app = None
        self.window = None

    def initialize(self):
        """Initialize all components"""
        # Setup logging
        self.logger = setup_logging()
        self.logger.info("=" * 60)
        self.logger.info("PathPal RPT Analyzer Starting")
        self.logger.info("=" * 60)

        # Initialize core components
        self.detector = ReportDetector()
        self.parser = UniversalParser(self.detector)

        # Create application
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("PathPal RPT Analyzer")
        self.app.setOrganizationName("PathPal Tools")
        self.app.setApplicationVersion("1.0.0")

        # -------- LOAD APPLICATION ICON --------
        icon_path = Path(__file__).parent / "core" / "PathPal.ico"

        if icon_path.exists():
            self.app.setWindowIcon(QIcon(str(icon_path)))
            self.logger.info(f"Loaded application icon: {icon_path}")
        else:
            self.logger.warning(f"Icon not found: {icon_path}")

        # Apply dark theme
        self._apply_dark_theme()

    def _apply_dark_theme(self):
        """Apply professional dark theme"""
        dark_style = """
        QMainWindow, QDialog {
            background-color: #2b2b2b;
            color: #ffffff;
        }
        QMenuBar {
            background-color: #333333;
            color: #ffffff;
            border-bottom: 1px solid #555555;
        }
        QMenuBar::item:selected {
            background-color: #404040;
        }
        QMenu {
            background-color: #333333;
            color: #ffffff;
            border: 1px solid #555555;
        }
        QMenu::item:selected {
            background-color: #404040;
        }
        QToolBar {
            background-color: #333333;
            border: none;
            border-bottom: 1px solid #555555;
            spacing: 3px;
            padding: 2px;
        }
        QStatusBar {
            background-color: #333333;
            color: #cccccc;
            border-top: 1px solid #555555;
        }
        QTabWidget::pane {
            background-color: #2b2b2b;
            border: 1px solid #555555;
        }
        QTabBar::tab {
            background-color: #333333;
            color: #cccccc;
            padding: 6px 12px;
            margin-right: 2px;
            border: 1px solid #555555;
            border-bottom: none;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
        }
        QTabBar::tab:selected {
            background-color: #404040;
            color: #ffffff;
        }
        QTableWidget {
            background-color: #2b2b2b;
            color: #ffffff;
            gridline-color: #555555;
            border: 1px solid #555555;
        }
        QTableWidget::item:selected {
            background-color: #404040;
        }
        QHeaderView::section {
            background-color: #333333;
            color: #ffffff;
            padding: 4px;
            border: 1px solid #555555;
        }
        QPushButton {
            background-color: #404040;
            color: #ffffff;
            border: 1px solid #555555;
            padding: 6px 12px;
            border-radius: 4px;
            min-width: 80px;
        }
        QPushButton:hover {
            background-color: #4a4a4a;
        }
        QPushButton:pressed {
            background-color: #333333;
        }
        QLineEdit, QTextEdit, QPlainTextEdit {
            background-color: #333333;
            color: #ffffff;
            border: 1px solid #555555;
            padding: 4px;
            border-radius: 4px;
        }
        QComboBox {
            background-color: #333333;
            color: #ffffff;
            border: 1px solid #555555;
            padding: 4px;
            border-radius: 4px;
        }
        QComboBox::drop-down {
            border: none;
        }
        QComboBox::down-arrow {
            image: none;
            border-left: 4px solid transparent;
            border-right: 4px solid transparent;
            border-top: 4px solid #ffffff;
            margin-right: 4px;
        }
        QComboBox QAbstractItemView {
            background-color: #333333;
            color: #ffffff;
            border: 1px solid #555555;
            selection-background-color: #404040;
        }
        QCheckBox {
            color: #ffffff;
        }
        QCheckBox::indicator {
            width: 16px;
            height: 16px;
            border: 1px solid #555555;
            background-color: #333333;
        }
        QCheckBox::indicator:checked {
            background-color: #404040;
        }
        QScrollBar:vertical {
            background-color: #333333;
            width: 12px;
            border: 1px solid #555555;
        }
        QScrollBar::handle:vertical {
            background-color: #555555;
            min-height: 20px;
        }
        QScrollBar::handle:vertical:hover {
            background-color: #666666;
        }
        QScrollBar:horizontal {
            background-color: #333333;
            height: 12px;
            border: 1px solid #555555;
        }
        QScrollBar::handle:horizontal {
            background-color: #555555;
            min-width: 20px;
        }
        QScrollBar::handle:horizontal:hover {
            background-color: #666666;
        }
        QGroupBox {
            color: #ffffff;
            border: 1px solid #555555;
            margin-top: 10px;
            padding-top: 10px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
        }
        QProgressBar {
            border: 1px solid #555555;
            background-color: #333333;
            color: #ffffff;
            text-align: center;
        }
        QProgressBar::chunk {
            background-color: #404040;
            width: 10px;
        }
        """
        self.app.setStyleSheet(dark_style)

    def run(self):
        """Run the application"""
        self.window = MainWindow(self.parser, self.detector)
        self.window.show()
        self.logger.info("Main window displayed")
        return self.app.exec()

    def cleanup(self):
        """Cleanup before exit"""
        self.logger.info("Shutting down...")
        logging.shutdown()


def main():
    """Main entry point"""
    app = RPTAnalyzer()

    try:
        app.initialize()
        exit_code = app.run()
        app.cleanup()
        sys.exit(exit_code)
    except Exception as e:
        logging.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
