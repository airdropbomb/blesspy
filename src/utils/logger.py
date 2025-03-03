from datetime import datetime


class Logger:
    @staticmethod
    def log_message(current_num=None, total=None, message="", message_type="info"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        account_status = f"[{current_num}/{total}] " if current_num and total else ""

        colors = {
            "info": "\033[97m",
            "success": "\033[92m",
            "error": "\033[91m",
            "warning": "\033[93m",
            "process": "\033[96m",
            "debug": "\033[94m",
        }

        color = colors.get(message_type, "\033[97m")
        print(f"\033[97m[{timestamp}] {account_status}{color}{message}\033[0m")
