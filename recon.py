import socket
import dns.resolver
import requests
import json
from colorama import Fore, Style

def banner():
    print(Fore.CYAN + """
    ===============================
       Automated Recon Tool
       Author: Munavar
    ===============================
    """ + Style.RESET_ALL)

def resolve_domain(domain):
    try:
        ip = socket.gethostbyname(domain)
        print(f"[+] Domain IP: {ip}")
        return ip
    except:
        print("[-] Could not resolve domain")
        return None

def check_subdomains(domain):
    alive = []
    with open("subdomains.txt") as file:
        for sub in file:
            sub = sub.strip()
            url = f"http://{sub}.{domain}"
            try:
                r = requests.get(url, timeout=3)
                print(f"[+] {url} -> {r.status_code}")
                alive.append({
                    "subdomain": url,
                    "status": r.status_code
                })
            except:
                pass
    return alive

def save_report(domain, ip, results):
    data = {
        "domain": domain,
        "ip": ip,
        "alive_subdomains": results
    }
    with open("report.json", "w") as f:
        json.dump(data, f, indent=4)
    print("[+] Report saved as report.json")

def main():
    banner()
    domain = input("Enter target domain (example.com): ")
    ip = resolve_domain(domain)
    results = check_subdomains(domain)
    save_report(domain, ip, results)

if __name__ == "__main__":
    main()
