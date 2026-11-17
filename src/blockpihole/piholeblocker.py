#!/usr/bin/env python3
import http.server
import subprocess
import os

PORT = 8081
SECRET_PATH = "/secret-open-sesame"  # Change this to your secret token
INTERFACE = "ens3"

class KnockHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # Only trigger if the secret URL is hit exactly
        if self.path == SECRET_PATH:
            # Extract the client's real public IP address
            client_ip = self.client_address[0]

            # If your VPS is behind a proxy/NAT layer, uncomment the line below:
            # client_ip = self.headers.get('X-Forwarded-For', self.client_address[0])

            print(f"Knock received from {client_ip}. Updating firewall...")

            try:
                # 1. Flush the existing mangle PREROUTING table
                subprocess.run(["sudo", "iptables", "-t", "mangle", "-F", "PREROUTING"], check=True)

                # 2. Inject the new strict allow rules
                subprocess.run(["sudo", "iptables", "-t", "mangle", "-I", "PREROUTING", "-i", INTERFACE, "-p", "udp", "--dport", "53", "!", "-s", client_ip, "-j", "DROP"], check=True)
                subprocess.run(["sudo", "iptables", "-t", "mangle", "-I", "PREROUTING", "-i", INTERFACE, "-p", "tcp", "--dport", "53", "!", "-s", client_ip, "-j", "DROP"], check=True)
                         # 3. Save the rules permanently
                subprocess.run(["sudo", "netfilter-persistent", "save"], stdout=subprocess.DEVNULL)

                # Send a successful HTML response back to your Windows browser
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                response_html = f"<html><body><h2>Access Granted!</h2><p>Your IP <b>{client_ip}</b> is now authorized on Port 53.</p></body></html>"
                self.wfile.write(bytes(response_html, "utf-8"))

            except subprocess.CalledProcessError as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"Internal Server Error: Failed to update firewall.")
        else:
            # Stealth mode: Send a 444 or 404 to any scanner poking around your ports
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

if __name__ == "__main__":
    # Ensure the script runs as root so it can modify iptables
    if os.geteuid() != 0:
        print("Error: This script must be run as root/sudo.")
        exit(1)

    server = http.server.HTTPServer(('0.0.0.0', PORT), KnockHandler)
    print(f"Knock listener active on port {PORT}...")
    server.serve_forever()
    
