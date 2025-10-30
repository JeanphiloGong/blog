# **为什么能 Ping 通却 SSH 不通？一次“假 SSH 真 VNC” 的排查过程**

> **副标题：** 从连接被拒到协议识别，带你彻底理解 TCP、SSH 与 VNC 的区别
> **阅读时长：** 7 分钟
> **标签：** 网络排查、SSH、VNC、Linux、远程连接
> **SEO 关键词：** SSH连接失败、kex_exchange_identification、VNC端口5905、RFB 003.008、SSH vs VNC

---

## 🎯 目标读者

* Linux 使用者、开发者、服务器维护人员
* 想学习网络排错思路的中级工程师
* 对 SSH/VNC 协议机制有兴趣的读者

---

## 💡 背景与动机

你是否遇到过这样的情况：

> “服务器能 ping 通，但 SSH 连不上？”

这类问题很常见，尤其是在多服务（SSH、VNC、HTTP）混跑的远程主机上。
本文通过一次真实案例，展示从“SSH 连接失败”到“发现端口跑的是 VNC”的完整分析过程。

---

## 🔍 问题现象

执行命令：

```bash
ssh chenhm@101.6.142.82 -p 5905
```

输出：

```
kex_exchange_identification: Connection closed by remote host
Connection closed by 101.6.142.82 port 5905
```

尝试 `ping`：

```bash
ping 101.6.142.82
```

能通，没有丢包。

于是我们知道：

* 主机在线；
* 网络连通；
* 但 SSH 握手阶段失败。

---

## 🧠 核心概念解析

| 概念            | 解释                             |
| ------------- | ------------------------------ |
| **Ping**      | 使用 ICMP 协议，只测试网络连通性。           |
| **TCP**       | 传输层协议，负责建立连接（如三次握手）。           |
| **SSH**       | 应用层协议，基于 TCP 提供加密远程登录。         |
| **VNC / RFB** | 图形远程桌面协议（Remote Frame Buffer）。 |

换句话说：**Ping 通 ≠ SSH 通**，因为它们运行在不同协议层。

---

## ⚙️ 实践排查步骤

### Step 1. 测试 TCP 是否连通

```bash
telnet 101.6.142.82 5905
```

输出：

```
Trying 101.6.142.82...
Connected to 101.6.142.82.
Escape character is '^]'.
RFB 003.008
```

🚨 **关键线索**：
`RFB 003.008` 是 **VNC 协议的握手字符串**（Remote Frame Buffer version 3.8）。

这说明：

* 5905 端口确实开放；
* 但运行的是 **VNC 服务**，而不是 SSH。

---

## 🧩 原理解释

SSH 客户端在 TCP 层连上后，会发出加密握手请求（`SSH-2.0-OpenSSH_8.x`）。
而 VNC 服务器在相同阶段返回 `RFB 003.008`。
协议不匹配 → SSH 客户端直接关闭连接。

这正是 `kex_exchange_identification` 错误的本质原因。

---

## 🧰 验证与确认

1️⃣ **查看端口服务**

```bash
sudo ss -tlnp | grep 5905
```

可能输出：

```
LISTEN  0  5  0.0.0.0:5905  ...  /usr/bin/Xvnc
```

说明该端口属于 VNC 服务。

2️⃣ **查看 SSH 监听端口**

```bash
sudo grep ^Port /etc/ssh/sshd_config
```

如果返回 `Port 22`，那 SSH 仍在默认端口。

---

## 🧭 正确的连接方式

### ✅ 若你想连接图形界面

使用 VNC 客户端：

```bash
vncviewer 101.6.142.82:5905
```

或使用工具：

* RealVNC
* TigerVNC
* TightVNC

### ✅ 若你想连接终端

使用 SSH（默认端口）：

```bash
ssh chenhm@101.6.142.82 -p 22
```

---

## 🛠️ 常见问题与注意事项

| 问题                                 | 可能原因           | 解决方式                                           |
| ---------------------------------- | -------------- | ---------------------------------------------- |
| `Connection closed by remote host` | 协议不匹配（SSH→VNC） | 使用正确协议连接                                       |
| SSH 无法连接任何端口                       | SSH 服务未启动      | `sudo systemctl start sshd`                    |
| VNC 连接拒绝                           | 防火墙未放行端口       | `firewall-cmd --add-port=5905/tcp --permanent` |
| SSH 被断开                            | fail2ban 封禁    | 检查 `/var/log/auth.log`                         |

---

## 🧩 最佳实践与建议

* **区分端口与协议**：仅凭端口号不能判断服务类型。
* **使用 `telnet` / `nc` 探测协议标识**，是快速判断服务类型的技巧。
* **养成查看日志的习惯**：`journalctl -u ssh`、`/var/log/auth.log`。
* **为多服务主机设置清晰端口规划**，例如：

  ```
  SSH → 22
  VNC → 5900+
  HTTP → 80/8080
  HTTPS → 443
  ```

---

## 🧾 小结

本文通过一个“能 ping 通但 ssh 不通”的案例，展示了：

1. 如何区分网络层、传输层与应用层问题；
2. 如何识别协议（RFB vs SSH）；
3. 如何快速定位真正运行的服务。

> 一句话总结：
> **不是 SSH 坏了，而是你连错了服务。**

---

## 🔗 参考与延伸阅读

* [OpenSSH 官方文档](https://www.openssh.com/manual.html)
* [TigerVNC GitHub](https://github.com/TigerVNC/tigervnc)
* [Linux man pages: ssh, telnet, ss, netstat]
* [RFC 6143: The Remote Framebuffer Protocol (RFB)](https://datatracker.ietf.org/doc/html/rfc6143)

---

## 🚀 行动号召

👉 **试试看！**
在你自己的服务器上运行：

```bash
nc <server_ip> <port>
```

看看它返回什么协议头，也许你会发现更多“隐藏服务”。

💬 **有趣的网络排查案例？** 欢迎在评论区分享你的故事或问题。
