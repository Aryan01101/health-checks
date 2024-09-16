import psutil
import os
import platform
from collections import defaultdict

def get_size(bytes):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}B"
        bytes /= factor

def get_system_info():
    print("="*40, "System Information", "="*40)
    uname = platform.uname()
    print(f"System: {uname.system}")
    print(f"Node Name: {uname.node}")
    print(f"Release: {uname.release}")
    print(f"Version: {uname.version}")
    print(f"Machine: {uname.machine}")
    print(f"Processor: {uname.processor}")

def get_cpu_info():
    print("="*40, "CPU Info", "="*40)
    print("Physical cores:", psutil.cpu_count(logical=False))
    print("Total cores:", psutil.cpu_count(logical=True))
    print(f"CPU Usage: {psutil.cpu_percent()}%")

def get_memory_info():
    print("="*40, "Memory Information", "="*40)
    svmem = psutil.virtual_memory()
    print(f"Total: {get_size(svmem.total)}")
    print(f"Available: {get_size(svmem.available)}")
    print(f"Used: {get_size(svmem.used)}")
    print(f"Percentage: {svmem.percent}%")

def get_disk_info():
    print("="*40, "Disk Information", "="*40)
    partitions = psutil.disk_partitions()
    for partition in partitions:
        print(f"=== Device: {partition.device} ===")
        print(f"  Mountpoint: {partition.mountpoint}")
        print(f"  File system type: {partition.fstype}")
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            continue
        print(f"  Total Size: {get_size(partition_usage.total)}")
        print(f"  Used: {get_size(partition_usage.used)}")
        print(f"  Free: {get_size(partition_usage.free)}")
        print(f"  Percentage: {partition_usage.percent}%")

def get_file_categories(path):
    categories = defaultdict(int)
    for root, _, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                file_size = os.path.getsize(file_path)
                _, extension = os.path.splitext(file)
                categories[extension.lower()] += file_size
            except (FileNotFoundError, PermissionError):
                continue
    return categories

def print_file_categories(categories):
    print("="*40, "File Categories", "="*40)
    total_size = sum(categories.values())
    for ext, size in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        if ext:
            print(f"{ext}: {get_size(size)} ({size/total_size:.2%})")
        else:
            print(f"No extension: {get_size(size)} ({size/total_size:.2%})")

if __name__ == "__main__":
    get_system_info()
    get_cpu_info()
    get_memory_info()
    get_disk_info()
    
    # Specify the path you want to analyze
    path_to_analyze = "/path/to/analyze"  # Change this to the desired path
    file_categories = get_file_categories(path_to_analyze)
    print_file_categories(file_categories)
