# port-scanner by ryderbr

import socket
import argparse
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

def port(val):
    port = int(val)
    if not (1 <= port <= 65535):
        raise argparse.ArgumentTypeError(f"{val} is not a valid port (1-65535)")
    return port

def check(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        if s.connect_ex((ip, port)) == 0:
            return port
    return None

parser = argparse.ArgumentParser()
parser.add_argument('input', type=str, nargs='?', help="Target host address (default is self)", default=socket.gethostname())
parser.add_argument('-s', '--start', type=port, help='Start of port range (default = 1)', default=1)
parser.add_argument('-e', '--end', type=port, help="End of port range (default = 65535)", default=65535)
args = parser.parse_args()

if args.start > args.end:
    parser.error("Start port must be less than or equal to end port.")

try:
    targetIP = socket.gethostbyname(args.input)
except socket.gaierror:
    print("\nHostname could not be resolved. :( Exiting program.")
    exit()
ports = range(args.start, args.end + 1)
print("-" * 30)
print(f"Scanning {targetIP} for open ports from {args.start} to {args.end}")
print("-" * 30)

socket.setdefaulttimeout(1)
startdate = datetime.now()
try:
    with ThreadPoolExecutor(max_workers=500) as executor:
        results = executor.map(lambda p: check(targetIP, p), ports)
    for port in results:
        if port is not None:
            print(f"Port {port} is open")
except KeyboardInterrupt:
    print("\nExiting program.")
    exit()
except socket.error:
    print("\nCouldn't connect to server. :( Exiting program.")
    exit()

print(f"\nScanning completed in: {datetime.now() - startdate}")