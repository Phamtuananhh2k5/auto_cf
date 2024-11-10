import time
import requests
import os

# Cấu hình
ip_can_ping = "36.50.135.207"
so_loi_toi_da = 3
cloudflare_api_key = "3b411374ee6b120fbfc87be4b80e930922034"
cloudflare_email = "dcmnmmmchkh@gmail.com"
zone_id = "97ba8fa7677ba6c439840ba679d698b0"
domain = "dualeovpn.net"

# Hàm ping IP
def ping_ip(ip):
    response = os.system(f"ping -c 1 {ip}")
    return response == 0

# Bật tất cả các rule WAF trong Cloudflare
def bat_tat_ca_rule_waf(api_key, email, zone_id):
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/firewall/waf/packages"
    headers = {
        "X-Auth-Key": api_key,
        "X-Auth-Email": email,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        packages = response.json().get("result", [])
        for package in packages:
            package_id = package.get("id")
            rules_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/firewall/waf/packages/{package_id}/rules"
            rules_response = requests.get(rules_url, headers=headers)
            if rules_response.status_code == 200:
                rules = rules_response.json().get("result", [])
                for rule in rules:
                    rule_id = rule.get("id")
                    update_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/firewall/waf/packages/{package_id}/rules/{rule_id}"
                    data = {
                        "mode": "on"
                    }
                    update_response = requests.patch(update_url, json=data, headers=headers)
                    if update_response.status_code == 200:
                        print(f"Đã bật rule {rule_id} trong package {package_id}.")
                    else:
                        print(f"Không thể bật rule {rule_id} trong package {package_id}: {update_response.text}")
            else:
                print(f"Không thể lấy rule cho package {package_id}: {rules_response.text}")
    else:
        print(f"Không thể lấy package: {response.text}")

# Logic chính
so_loi = 0

while True:
    if ping_ip(ip_can_ping):
        so_loi = 0
        print(f"Ping tới {ip_can_ping} thành công.")
    else:
        so_loi += 1
        print(f"Ping tới {ip_can_ping} thất bại ({so_loi}/{so_loi_toi_da}).")
    
    if so_loi >= so_loi_toi_da:
        print(f"Đạt tới số lỗi tối đa. Bật tất cả các rule WAF cho domain {domain} trong Cloudflare.")
        bat_tat_ca_rule_waf(cloudflare_api_key, cloudflare_email, zone_id)
        break
    
    time.sleep(1)
