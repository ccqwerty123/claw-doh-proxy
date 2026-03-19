这是一个为你准备的专业版 README.md 内容。你可以直接复制，然后粘贴到你的 GitHub 项目中。

Claw-DoH-Proxy

基于 Caddy 和 ClawCloud Run 搭建的轻量化隐私保护 DoH (DNS-over-HTTPS) 转发服务，支持通过 NextDNS 实现自动国内外流量分流。

📖 项目简介

本服务旨在为您提供一个私有、加密的 DNS 查询通道，规避运营商 DNS 劫持与监控。通过 Caddy 反向代理，将用户的 DoH 请求安全转发至 NextDNS，利用其强大的全球节点和智能分流能力，实现国内域名高速解析、国外域名安全解析。

🚀 部署步骤
1. 准备工作

注册并登录 ClawCloud Run。

注册 NextDNS 账号，并在控制台获取您的 NextDNS ID (在控制台首页即可看到，例如 e14735)。

2. 创建容器应用

在 ClawCloud Run 控制台点击 Create App。

Application Name: 自定义（例如 my-doh-proxy）。

Image: 选择 public，Image Name 填入 caddy:latest。

资源配置: 建议 0.1 CPU + 64MB 内存（足够使用）。

端口设置:

Container Port: 80。

Internet Access: 必须开启（开启后即可获得你的专属公网域名 *.clawcloudrun.com）。

持久化存储: 添加一个 Local Storage，Mount Path 填 /data，以便自动管理 SSL 证书。

3. 配置 Caddyfile (关键)

在容器配置界面的 Configmaps 选项中，创建一个新文件：

File name: /etc/caddy/Caddyfile

File content:

code
Caddy
download
content_copy
expand_less
{
    # 彻底禁用 Caddy 自动尝试 HTTP 到 HTTPS 的重定向，交给云平台处理
    auto_https disable_redirects
}

:80 {
    # 转发请求给 NextDNS
    reverse_proxy https://dns.nextdns.io {
        header_up Host dns.nextdns.io
        # 在下方填入你在 NextDNS 后台获取的 ID
        header_up X-NextDNS-ID ❌❌❌❌❌❌
        
        transport http {
            tls_server_name dns.nextdns.io
        }
    }
}

⚠️ 注意事项：请将上述配置中的 ❌❌❌❌❌❌ 替换为您在 NextDNS 后台获取的 ID (例如：e14735)。

4. 部署与验证

点击 Deploy Application 部署容器。

等待几秒钟后，在 Logs 中查看日志，若显示 serving initial configuration 且没有报错，说明服务已上线。

如何使用：

你的 DoH 地址为：https://你的域名.clawcloudrun.com/dns-query

你可以直接将其填入 Firefox 浏览器、Android 系统“私密 DNS”设置或各类支持 DoH 的客户端中。

访问 https://test.nextdns.io/ 验证是否生效（看到 "Protocol: DoH" 及你的 ID 即为成功）。

🔒 安全与隐私声明

隐私风险提示：请务必使用您自己注册的 NextDNS ID。如果您在教程中直接使用他人的 ID，对方将能看到您的所有 DNS 查询记录（包括您访问了什么网站），这存在严重的隐私泄露风险。

资源限制：ClawCloud Run 提供的免费额度有限，此服务仅供个人或家庭小团体使用，请勿将其作为公共 DNS 节点开放给互联网，以防被滥用导致封号。

📄 开源协议

本项目采用 MIT License 开源，欢迎自由使用与修改。

如何在 GitHub 发布：

进入你的 GitHub 仓库页面。

点击 "Add a README"。

将上面的内容粘贴进去。

点击底部的 "Commit changes"。

你的教程现在看起来非常专业且安全！
