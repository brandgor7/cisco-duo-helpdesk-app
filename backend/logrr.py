"""
Copyright (c) 2023 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at https://developer.cisco.com/docs/licenses.
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import logging
from config.config import config
import json
import logging.handlers
import queue
from rich.logging import RichHandler

# Global variable to hold the table's state
log_table = []


class LoggerManager:
    """
    Centralize logging from multiple processes into a single listener that can output to both a file and the terminal without the messages getting jumbled.
    """
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.listener = None
        self.console = Console()
        self.log_queue = queue.Queue(-1)  # No limit on size
        self.queue_handler = logging.handlers.QueueHandler(self.log_queue)
        self.logger = self.setup()
        self.original_log_level = self.logger.level
        self.session_logs = {}  # This will store all the logs per session
        self.logger.propagate = False

    def setup(self):
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

        # Handlers for file and console
        file_handler = logging.FileHandler("logs/app.log", mode='a')
        file_handler.setFormatter(logging.Formatter(log_format))
        console_handler = RichHandler(console=self.console)

        # Listener that listens to the queue
        self.listener = logging.handlers.QueueListener(self.log_queue, console_handler, file_handler, respect_handler_level=True)
        self.listener.start()

        # Setup logger
        logger = logging.getLogger(__name__)
        log_level = config.LOGGER_LEVEL

        logger.setLevel(log_level)
        logger.addHandler(self.queue_handler)  # Add QueueHandler

        return logger

    def shutdown(self):
        self.listener.stop()  # Stop the listener when shutting down

    def display_2_column_rich_table(self, data, title):
        """
        Display data in a rich table format.
        """
        table = Table(title=title)
        table.add_column("Variable", justify="left", style="bright_white", width=30)
        table.add_column("Value", style="bright_white", width=60)

        for var_name, var_value in data:
            table.add_row(var_name, str(var_value) if var_value not in [None, ""] else "Not Set")

        self.console.print(table)

    def display_list_as_rich_table(self, data_list, title, headers=None):
        """
        Display a list of dictionaries in a rich table format with specified headers.
        Args:
            data_list (list): List of dictionaries to display.
            headers (list): List of headers (keys from the dictionaries) to include in the table.
            title (str): Title of the table.
        """
        if not data_list or not isinstance(data_list, list) or not all(isinstance(item, dict) for item in data_list):
            self.console.print("Invalid data provided for the table.")
            return
        table = Table(title=title)

        if headers is None:     # Determine headers if not provided
            headers = data_list[0].keys() if data_list else []

        for header in headers:      # Add columns to the table based on provided headers or dynamically determined headers
            table.add_column(header, style="bright_white")

        # Populate table rows with data
        for item in data_list:
            row = [str(item.get(header, '')) for header in headers]
            table.add_row(*row)

        self.console.print(table)

    def display_json_as_rich_table(self, json_data, title="JSON Data"):
        """
        Display JSON data in a rich table format.

        Args:
            json_data (str/dict/list): JSON data to be displayed in the table.
            title (str): Title of the table.
        """
        # Parse JSON if it's a string
        if isinstance(json_data, str):
            try:
                data = json.loads(json_data)
            except json.JSONDecodeError as e:
                self.console.print(f"Invalid JSON string: {e}")
                return

        # Handle case where data is already a dictionary or list
        else:
            data = json_data

        # Create a new table
        table = Table(title=title)

        # Check if the data is a list of dictionaries
        if isinstance(data, list) and all(isinstance(elem, dict) for elem in data):
            # Add headers based on the keys of the first dictionary
            headers = data[0].keys()
            for header in headers:
                table.add_column(header, style="bright_white")

            # Add rows
            for item in data:
                table.add_row(*[str(item.get(h, '')) for h in headers])

        elif isinstance(data, dict):
            # If the data is a single dictionary, display key-value pairs
            table.add_column("Key", style="bright_yellow")
            table.add_column("Value", style="bright_white")
            for key, value in data.items():
                table.add_row(str(key), json.dumps(value, indent=2) if isinstance(value, (dict, list)) else str(value))

        else:
            self.console.print("Unsupported JSON format")
            return

        # Print the table
        self.console.print(table)

    def display_config_table(self, config_instance):
        config_data = [(name, getattr(config_instance, name)) for name in config_instance.model_fields.keys()]
        self.display_2_column_rich_table(config_data, title="Environment Variables")

    def print_start_panel(self, app_name=config.APP_NAME):
        self.console.print(Panel.fit(f"[bold bright_green]{app_name}[/bold bright_green]"))

    def print_finished_panel(self):
        # Mostly used for non-flask apps
        self.console.print(Panel.fit("[bold bright_green]All operations completed successfully. Exiting the application.[/bold bright_green]"))

    def print_exit_panel(self):
        self.console.print("\n")
        self.console.print(Panel.fit("Shutting down...", title="[bright_red]Exit[/bright_red]"))

    def exception(self, message, extra_data=None):
        """Log an exception along with a custom message."""
        if extra_data:
            message += f' - Extra data: {extra_data}'
        self.logger.exception(message)


logger_manager = LoggerManager.get_instance()  # Create a single instance of LoggerManager

