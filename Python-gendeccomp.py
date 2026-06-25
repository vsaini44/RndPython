import time
import re

SAMPLE_LOGS = """2024-01-01 10:00:00 INFO Server started on 192.168.1.10
2024-01-01 10:01:23 ERROR Connection failed from 10.0.0.5
2024-01-01 10:02:45 WARN High memory usage
2024-01-01 10:03:12 ERROR Timeout from 10.0.0.5"""


# DECORATOR
def timer(func):
    def wrapper(*args, **kwargs):
        start  = time.time()
        result = func(*args, **kwargs)
        end    = time.time()
        print(f"\n[TIMER] {func.__name__} took {end - start:.6f} seconds")
        return result
    return wrapper


# GENERATOR
def parse_log_file(log_data):
    for line in log_data.strip().split("\n"):
        parts = line.split(" ", 3)
        yield {
            "timestamp": parts[0] + " " + parts[1],
            "level":     parts[2],
            "message":   parts[3]
        }


# MAIN FUNCTION
@timer
def analyze_logs(log_data):

    logs = list(parse_log_file(log_data))    # generator → list

    # list comprehension — only errors
    errors = [log for log in logs if log["level"] == "ERROR"]
    print("--- ERRORS ---")
    for e in errors:
        print(e["message"])

    # dict comprehension — count per level
    level_count = {
        "INFO":  len([log for log in logs if log["level"] == "INFO"]),
        "ERROR": len([log for log in logs if log["level"] == "ERROR"]),
        "WARN":  len([log for log in logs if log["level"] == "WARN"])
    }
    print("\n--- COUNT PER LEVEL ---")
    print(level_count)

    # set comprehension — unique IPs
    ip_pattern  = r"\d+\.\d+\.\d+\.\d+"
    unique_ips  = {ip for log in logs for ip in re.findall(ip_pattern, log["message"])}
    print("\n--- UNIQUE IPs ---")
    print(unique_ips)


analyze_logs(SAMPLE_LOGS)
