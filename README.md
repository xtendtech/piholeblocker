Pihole is installed on system 
But since its on public ip there are lot of bots or scripts
scanning and using dns.Its running on docker.So normal Ufw 
firewall will not work
So this script will block all access except for allowed ips
for dns
Assumption : Pihole running on port 53 for dns using docker is installed

PORT = 8080 #The webserver port of pihole 

SECRET_PATH = "/secret-open-sesame"  # Change this to your secret token # This is the url to change ip when its dynamic ip. SSH should work for all ips  but port 53 is blocked except for the allowed ips
use  sudo ss -lptn 'sport = :8080' to check port if its 8081
INTERFACE = "ens3"

To get public ip use
curl ifconfig.me

The script modifies iptables in mangle section which is the first section to get loaded before docker rules.To see change 
 sudo iptables -t mangle -L PREROUTING -v -n

 Logs for webservice 
 sudo journalctl -u dns-knock.service -n 50 -f


Use to create
sudo systemctl edit --full dns-knock.service
to start 
To  start service
sudo systemctl daemon-reload
sudo systemctl start dns-knock.service

To check status
sudo systemctl status dns-knock.service

To stop service
sudo systemctl stop dns-knock.service