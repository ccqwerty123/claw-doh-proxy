这是一份为你准备的 README.md 内容模板，你可以直接复制到 GitHub 仓库中使用。我已经使用 Markdown 的代码块语法，确保用户复制时代码格式整洁，并且清晰地标注了需要修改的地方。

Claw-DoH-Proxy

一个基于 ClawCloud Run 和 Caddy 的轻量级隐私保护 DNS-over-HTTPS (DoH) 转发器。

本方案将你的 DNS 查询通过加密通道转发至 NextDNS，利用其强大的全球节点和自动分流功能，有效规避 DNS 劫持，保障网络隐私。

🚀 核心特性

轻量化：仅占用极少量的 CPU 和内存 (约 0.1C/64M)。

全链路加密：使用 DoH 协议，防止 DNS 查询被运营商或中间人劫持。

自动分流：依托 NextDNS，自动实现国内外流量分流，国内解析高速，国外解析安全。

配置简单：无需复杂编译，直接使用 Caddy 官方镜像。

🛠 部署指南
1. 准备工作

注册并登录 NextDNS.io，在控制台获取你的 NextDNS ID。

登录 ClawCloud Run。

2. 创建容器应用

点击 Create App。

Application Name: 自定义（如 my-doh）。

Image Name: 输入 caddy:latest。

Resources: 配置 0.1 CPU 和 64MB Memory 即可。

Container Port: 填入 80。

Enable Internet Access: 务必开启（开关变绿）。

Local Storage: 添加路径 /data (用于存储 SSL 证书)。

3. 配置 Caddyfile (Configmaps)

在容器配置页面的 Configmaps 选项中，添加文件：

File name: /etc/caddy/Caddyfile

File content: (请复制以下代码，并替换其中的 你的域名 和 你的NextDNS_ID)

```
{
    # 彻底禁用 Caddy 自动尝试 HTTP 到 HTTPS 的重定向，交给云平台处理
    auto_https disable_redirects
}

:80 {
    # 无论用户访问什么路径，都确保转发给 NextDNS 的时候包含了 ID
    # 这样你访问 domain.com/ 也能解析，访问 domain.com/dns-query 也能解析
    reverse_proxy https://dns.nextdns.io {
        header_up Host dns.nextdns.io
        header_up X-NextDNS-ID e14735
        
        # 强制指定后端 SNI，这是连接 HTTPS 后端必须的
        transport http {
            tls_server_name dns.nextdns.io
        }
    }
}
```

注意：如果不使用 NextDNS，也可以删除 header_up X-NextDNS-ID 这一行，并直接将 dns.nextdns.io 替换为 cloudflare-dns.com 即可使用 Cloudflare 公共 DNS。

4. 部署与使用

点击 Deploy Application 完成部署。

查看 Logs，等待 Certificate obtained successfully 字样出现，表明 SSL 证书已自动签发。

验证 DoH:
在浏览器（如 Firefox）设置中填入你的 DoH 地址：
https://你的域名.clawcloudrun.com/dns-query
然后访问 https://test.nextdns.io/，若显示 "Protocol: DoH" 且对应你的 ID，即部署成功！

⚠️ 安全警告

隐私保护：请务必使用自己的 NextDNS ID，严禁直接使用他人 ID，否则你的 DNS 查询记录将泄露给他人。

限流提示：ClawCloud Run 提供免费额度，请勿将此域名公开至公共互联网，避免被恶意刷流量导致账号受限。

合规说明：本项目仅供学习和个人隐私保护使用，请遵守当地法律法规。

如何自定义配置？

如果你想在 GitHub 上显示得更好看，可以在仓库首页点击 Add file -> Create new file，名称填 README.md，然后把上面这些文字粘贴进去即可。GitHub 会自动渲染出漂亮的教程页面！
