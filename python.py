import urllib.request
import json

def test_dns_json(domain, doh_base_url):
    print(f"--- 正在查询域名: {domain} ---")
    
    # NextDNS 支持 JSON 接口，我们可以直接通过 GET 请求获取结果
    # 格式：https://你的域名/resolve?name=域名
    url = f"{doh_base_url}/resolve?name={domain}"
    
    try:
        req = urllib.request.Request(url)
        # 模拟浏览器 Header
        req.add_header('Accept', 'application/dns-json')
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            
            if "Answer" in data:
                print(f"✅ 解析成功！{domain} 的结果为:")
                for answer in data["Answer"]:
                    # type 1 是 A 记录 (IPv4), type 28 是 AAAA 记录 (IPv6)
                    type_name = "IPv4" if answer['type'] == 1 else "IPv6" if answer['type'] == 28 else "Other"
                    print(f"   [{type_name}] {answer['data']}")
            else:
                print(f"⚠️ 未找到解析记录或服务端返回错误。")
                print(f"   原始响应: {data}")
                
    except Exception as e:
        print(f"❌ 请求失败: {e}")
    print("\n")

if __name__ == "__main__":
    # 你的自定义 DoH 地址 (注意：JSON 接口通常直接在根路径或 /resolve)
    # 因为你的 Caddyfile 配置了反代到 dns.nextdns.io，它会自动处理 /resolve
    MY_DOMAIN_URL = "https://XXXXXX.clawcloudrun.com"
    
    test_domains = [
        "www.baidu.com", 
        "www.google.com",
        "apple.com"
    ]
    
    for d in test_domains:
        test_dns_json(d, MY_DOMAIN_URL)
