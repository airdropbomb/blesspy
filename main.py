import asyncio
import json
import os

from src.main.bless import BlessAutoRun
from src.main.proxy import ProxyManager
from src.utils.logger import Logger


def load_accounts(filename="accounts.json"):
    if not os.path.exists(filename):
        Logger.log_message(0, 0, "accounts.json not found", "error")
        return []

    try:
        with open(filename, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        Logger.log_message(0, 0, "Error accounts.json", "error")
        return []


proxy_manager = ProxyManager()


async def run_ping(account_data, index, total_accounts):
    token = account_data["Token"]
    nodes = account_data["Nodes"]

    proxy = proxy_manager.get_random_proxy(
        index + 1, total_accounts)

    tasks = []
    for node in nodes:
        node_obj = type("Node", (object,), node)
        bless = BlessAutoRun(
            proxy=proxy, current_num=index + 1, total=total_accounts)

        tasks.append(asyncio.create_task(bless.ping_node(node_obj, token)))

    await asyncio.gather(*tasks)


async def main():
    os.system("cls" if os.name == "nt" else "clear")
    print("""
       █████╗ ██████╗ ██████╗     ███╗   ██╗ ██████╗ ██████╗ ███████╗
      ██╔══██╗██╔══██╗██╔══██╗    ████╗  ██║██╔═══██╗██╔══██╗██╔════╝
      ███████║██║  ██║██████╔╝    ██╔██╗ ██║██║   ██║██║  ██║█████╗  
      ██╔══██║██║  ██║██╔══██╗    ██║╚██╗██║██║   ██║██║  ██║██╔══╝  
      ██║  ██║██████╔╝██████╔╝    ██║ ╚████║╚██████╔╝██████╔╝███████╗
      ╚═╝  ╚═╝╚═════╝ ╚═════╝     ╚═╝  ╚═══╝ ╚═════╝ ╚═════╝ ╚══════╝  
        By : ADB NODE

    accounts = load_accounts()
    if not accounts:
        return

    tasks = []
    for i, account in enumerate(accounts):
        tasks.append(asyncio.create_task(run_ping(account, i, len(accounts))))

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
