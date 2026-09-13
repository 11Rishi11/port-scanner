import socket
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime


def get_service_name(port):
    """Resolve the common service name for a port (e.g. 80 -> http)."""
    try:
        return socket.getservbyport(port, "tcp")
    except OSError:
        return "Unknown"


def grab_banner(target, port):
    """Try to grab a service banner from an open port."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        sock.connect((target, port))
        banner = sock.recv(1024).decode(errors="ignore").strip()
        sock.close()
        return banner if banner else "No banner"
    except:
        return "No banner"


def scan_port(target, port):
    """Check a single port. Returns (port, service, banner) if open, else None."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    result = sock.connect_ex((target, port))
    sock.close()
    if result == 0:
        service = get_service_name(port)
        banner = grab_banner(target, port)
        return (port, service, banner)
    return None


def scan_range(target, start_port, end_port, max_threads=100):
    """Scan a range of ports using multiple threads for speed."""
    print(f"Scanning {target} from port {start_port} to {end_port}...\n")
    open_ports = []

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        results = executor.map(lambda p: scan_port(target, p), range(start_port, end_port + 1))
        for result in results:
            if result:
                port, service, banner = result
                print(f"Port {port} is OPEN | Service: {service} | Banner: {banner}")
                open_ports.append((port, service, banner))

    return open_ports


def save_results(target, open_ports, filename="scan_results.txt"):
    """Save scan results to a text file."""
    with open(filename, "w") as f:
        f.write(f"Port Scan Report\n")
        f.write(f"Target: {target}\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Open ports found: {len(open_ports)}\n")
        f.write("-" * 40 + "\n")
        for port, service, banner in open_ports:
            f.write(f"Port {port} ({service}): {banner}\n")
    print(f"\nResults saved to {filename}")


if __name__ == "__main__":
    target = input("Enter target IP or hostname (e.g. 127.0.0.1): ")
    start = int(input("Start port: "))
    end = int(input("End port: "))

    results = scan_range(target, start, end)

    print(f"\nScan complete. {len(results)} open port(s) found: {[p for p, s, b in results]}")

    save_results(target, results)