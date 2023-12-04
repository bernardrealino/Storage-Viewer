import psutil
from texttable import Texttable

def bytes_to_gb(bytes_value):
    return bytes_value / (1024 ** 3)  # 1 gigabyte = 1024^3 bytes

def set_text_color(text, color_code):
    colored_text = f"\033[{color_code}m{text}\033[0m"
    return colored_text

def draw_bar(percentage):    
    bar_length = 30
    filled_length = int(bar_length * percentage)
    bar = '█' * filled_length + '░' * (bar_length - filled_length)
    percentage = percentage*100
    return f"[{bar}] {percentage:.2f}%"

def get_storage_info():
    storage_info = []

    try:
        partitions = psutil.disk_partitions(all=True)

        for partition in partitions:
            partition_info = {}
            partition_path = partition.mountpoint

            disk_usage = psutil.disk_usage(partition_path)

            partition_info['device'] = partition.device
            partition_info['mountpoint'] = partition_path
            partition_info['total_size'] = bytes_to_gb(disk_usage.total)
            partition_info['used_size'] = bytes_to_gb(disk_usage.used)
            partition_info['free_size'] = bytes_to_gb(disk_usage.free)
            partition_info['usage_percentage'] = disk_usage.percent / 100.0

            storage_info.append(partition_info)

        return storage_info

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    storage_info = get_storage_info()

    if isinstance(storage_info, list):
        t = Texttable()
        t.add_row(['Device', 'Mountpoint', 'Total Size (GB)', 'Used Size (GB)', 'Free Size (GB)', 'Usage'])
        t.set_cols_width([7,5,10,10,10,41])
        for partition in storage_info:
            usage_bar = draw_bar(partition['usage_percentage'])
            t.add_row([
                partition['device'],
                partition['mountpoint'],
                f"{partition['total_size']:.2f}",
                f"{partition['used_size']:.2f}",
                f"{partition['free_size']:.2f}",
                usage_bar
            ])

        print(t.draw())
    else:
        print(storage_info)
