import sys
import subprocess

# sys.argv[1] == "--status"
if "--status" in sys.argv:
 try:
        print("inside status")
        public_ip = subprocess.check_output(
            ["curl", "-s", "--max-time", "5", "ifconfig.me"],
            text=True
        ).strip()
    
    
 except Exception:
        public_ip = "Unavailable"
print(f"http://{public_ip}:8080/secret-open-sesame")
print(f"Currently allowed DNS IP:  {', '.join(ips) if ips else 'None'}")
sys.exit(0)
