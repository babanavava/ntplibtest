import ntplib
from time import strftime, gmtime, time, sleep

program_start_time = time()

def get_ntp_time():
    ntp_server = 'ntp.nict.jp'
    client = ntplib.NTPClient()    
    try:
        response = client.request(ntp_server, version=3, timeout=1)
        return response.tx_time
    except ntplib.NTPException as e:
        return None

def format_time(timestamp):
    formatted_time = strftime("%Y/%m/%d %H:%M:%S", gmtime(timestamp))
    return f"{formatted_time}.{str(timestamp % 1)[2:8]}"

def format_elapsed_time(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return f"{int(h):02d}:{int(m):02d}:{s:.2f}"

def elapsed_time():
    return time() - program_start_time

def write_to_cache_file(file_path, log_entry):
    with open(file_path, 'a') as file:
        file.write(log_entry + '\n')

def main():
    cache_file_path = 'ntp_cache.txt'

    while True:
        ntp_time = get_ntp_time()
        current_time = time()
        elapsed = elapsed_time()
        if ntp_time is not None:
            log_entry = f"NTP: {format_time(ntp_time)}, Local: {format_time(current_time)}, Elapsed: {format_elapsed_time(elapsed)}"
        else:
            log_entry = f"NTP: No response received, Local: {format_time(current_time)}, Elapsed: {format_elapsed_time(elapsed)}"
        write_to_cache_file(cache_file_path, log_entry)
        print(log_entry)        
        sleep(60)

if __name__ == "__main__":
    main()
