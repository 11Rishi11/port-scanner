\# Port Scanner



A simple multi-threaded TCP port scanner written in Python. Scans a target host for open ports, identifies the likely service running on each, and attempts to grab a banner from open ports.



\## Features

\- Multi-threaded scanning using `ThreadPoolExecutor` for speed

\- Identifies common service names for open ports (e.g. 80 → http)

\- Attempts banner grabbing on open ports to reveal more about the running service

\- Simple, dependency-free — uses only Python's standard library



\## Requirements

\- Python 3.x (no external packages needed)



\## Usage

```

python scanner.py

```



(Add any command-line arguments here if your script takes a target/port range as input, e.g.:)

```

python scanner.py <target\_ip> <start\_port> <end\_port>

```



\## Example output

```

Port 22   open   ssh      Banner: SSH-2.0-OpenSSH\_8.2p1

Port 80   open   http     Banner: No banner

Port 443  open   https    Banner: No banner

```



\## How it works

1\. `scan\_port()` attempts a socket connection to each port on the target.

2\. If the connection succeeds, `get\_service\_name()` resolves the common service name via `socket.getservbyport()`.

3\. `grab\_banner()` opens a second connection and tries to read any data the service sends immediately after connecting, which often reveals software name/version.

4\. Results are collected and can be written to `scan\_results.txt`.



\## Disclaimer

Only scan hosts and networks you own or have explicit permission to test. Scanning systems without authorization may be illegal depending on your jurisdiction.



\## License

MIT (or your preferred license).

