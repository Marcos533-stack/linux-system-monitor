import os
import psutil
import platform
import socket
from datetime import datetime
from colorama import Fore, Style, init

# Inicializar colorama
init(autoreset=True)

LOG_DIR = "logs"
LOG_FILE = f"{LOG_DIR}/system_log.txt"


def create_log_directory():
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)


def get_system_info():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    operating_system = platform.system()
    uptime_seconds = datetime.now().timestamp() - psutil.boot_time()

    hours = int(uptime_seconds // 3600)
    minutes = int((uptime_seconds % 3600) // 60)

    return {
        "Hostname": hostname,
        "IP Address": ip_address,
        "Operating System": operating_system,
        "Uptime": f"{hours}h {minutes}m"
    }


def get_resource_usage():
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent

    return {
        "CPU Usage": cpu_usage,
        "RAM Usage": ram_usage,
        "Disk Usage": disk_usage
    }


def get_top_processes():
    processes = []

    for process in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            processes.append(process.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    processes = sorted(
        processes,
        key=lambda proc: proc['cpu_percent'],
        reverse=True
    )

    return processes[:5]


def get_status_color(value):
    if value >= 90:
        return Fore.RED
    elif value >= 70:
        return Fore.YELLOW
    else:
        return Fore.GREEN


def display_system_status():
    system_info = get_system_info()
    resource_usage = get_resource_usage()
    top_processes = get_top_processes()

    print(Fore.CYAN + "\n===== SYSTEM STATUS =====\n")

    for key, value in system_info.items():
        print(f"{key}: {value}")

    print("\n===== RESOURCE USAGE =====\n")

    for key, value in resource_usage.items():
        color = get_status_color(value)
        print(color + f"{key}: {value}%")

    print(Fore.CYAN + "\n===== TOP 5 PROCESSES =====\n")

    for process in top_processes:
        print(
            f"PID: {process['pid']} | "
            f"Name: {process['name']} | "
            f"CPU: {process['cpu_percent']}%"
        )

    log_system_status(system_info, resource_usage, top_processes)


def log_system_status(system_info, resource_usage, top_processes):
    create_log_directory()

    with open(LOG_FILE, "a") as log_file:
        log_file.write("\n==============================\n")
        log_file.write(f"Timestamp: {datetime.now()}\n\n")

        for key, value in system_info.items():
            log_file.write(f"{key}: {value}\n")

        log_file.write("\n")

        for key, value in resource_usage.items():
            log_file.write(f"{key}: {value}%\n")

        log_file.write("\nTop Processes:\n")

        for process in top_processes:
            log_file.write(
                f"PID: {process['pid']} | "
                f"Name: {process['name']} | "
                f"CPU: {process['cpu_percent']}%\n"
            )


if __name__ == "__main__":
    display_system_status()