# **Telegram Vulnerability Bot** 🤖

![Build Status](https://github.com/thierrynshimiyumukiza/telegrambot/actions/workflows/ci.yml/badge.svg)
![License](https://img.shields.io/github/license/thierrynshimiyumukiza/telegrambot)
![Last Commit](https://img.shields.io/github/last-commit/thierrynshimiyumukiza/telegrambot)
                      
![Telegram Bot Demo](https://github.com/user-attachments/assets/b7890dca-f3b4-4366-8d78-386e69afa8a6)

<details>
  <summary><strong>📑 Table of Contents</strong></summary>

- [**Overview**](#overview)
- [**Features**](#features)
- [**Sample Scan Report**](#sample-scan-report)
- [**Usage**](#usage)
- [**Exploit Modules**](#exploit-modules)
- [**Technical Stack**](#technical-stack)
- [**GitHub Stats & Activity**](#github-stats--activity)
- [**Important Notes**](#important-notes)
- [**License**](#license)
</details>

---

## 📌 **Overview**

An **AI-powered Telegram bot** for **automated web vulnerability assessments** and **reconnaissance operations**.

This bot integrates various open-source tools to:
- 🔍 Scan networks
- 🛡 Detect vulnerabilities
- 🚀 Auto-demonstrate exploits
- 📄 Summarize results — all via Telegram

> ⚡ **AI-Powered**: Get instant explanations and scan summaries using **Natural Language Processing (NLP)**.

---

## 🚀 **Features**

- **🔍 Network Scanning** — Scan IPs & subnets using **Nmap**  
- **🛡 Vulnerability Detection** — Powered by **Nikto, sqlmap**, and **OWASP ZAP**  
- **📁 File Extraction** — Pull target system files  
- **🧠 AI Summarization** — Text/file summarizer using **NLTK**  
- **💥 Auto-Exploitation** — Demonstrates **RCE, XSS, SQLi**, and more  
- **📅 Persistence** — Adds **cron jobs** for access retention  
- **🧹 Log Clearing** — Removes traces from the system  
- **📚 Command Explanation** — Get simplified explanations for complex reports

---

## 📄 **Sample Scan Report**  
**Target**: `www.bracu.ac.bd`

| **Port**     | **State** | **Service**    |
|--------------|-----------|----------------|
| 53/tcp       | open      | domain         |
| 80/tcp       | open      | http           |
| 443/tcp      | open      | https          |
| 8080/tcp     | open      | http-proxy     |
| 8443/tcp     | open      | https-alt      |

- **Nikto**: ⏱ Timeout - no conclusive results  
- **sqlmap**: ✅ No major vulnerabilities found  
- **OWASP ZAP**: ✅ No major issues detected

---

## 💡 **Usage**

Interact with the bot using the following **Telegram commands**:

| **Command**                | **Description**                                |
|----------------------------|------------------------------------------------|
| `/start`                   | **Welcome message**                            |
| `/help`                    | **Show help menu**                             |
| `/exec <cmd>`              | **Execute shell command (restricted)**         |
| `/get_file <path>`         | **Retrieve file from system**                  |
| `/scan_network <subnet>`   | **Nmap subnet scan**                           |
| `/persist`                 | **Add persistence via cron**                   |
| `/ddos <url> [count]`      | **Demo a DDoS attempt**                        |
| `/auto_attack`             | **Initiate automated scan/exploit cycle**      |
| `/clear_logs`              | **Clear system logs**                          |
| `/scan <target>`           | **Run all scanners**                           |
| `/summarize <text/file>`   | **AI summary of given input**                  |
| `/explain <text>`          | **AI explanation of commands/output**          |

---

## 💣 **Exploit Modules**

| **Exploit Command**        | **Description**                                |
|----------------------------|------------------------------------------------|
| `/xss <url> <param>`       | **Reflected XSS demo**                         |
| `/sqli <url> <param>`      | **SQL Injection test**                         |
| `/rce <url> <param>`       | **Remote Code Execution**                      |
| `/lfi <url> <param>`       | **Local File Inclusion**                       |
| `/rfi <url> <param>`       | **Remote File Inclusion**                      |
| `/xxe <url> <param>`       | **XXE Payload test**                           |
| `/cmdinj <url> <param>`    | **Command Injection**                          |
| `/openredir <url> <param>` | **Open Redirect vulnerability test**           |
| `/patht <url> <param>`     | **Path Traversal demo**                        |
| `/fileupload <url>`        | **Malicious File Upload**                      |
| `/deserialize <url>`       | **PHP/Java Deserialization attack**            |
| `/csrf <url>`              | **Cross-Site Request Forgery test**            |

---

## 🧰 **Technical Stack**

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-0088CC?style=for-the-badge&logo=telegram&logoColor=white)
![Nmap](https://img.shields.io/badge/Nmap-0C71C3?style=for-the-badge&logo=nmap&logoColor=white)
![Nikto](https://img.shields.io/badge/Nikto-FF6C37?style=for-the-badge&logo=nikto&logoColor=white)
![sqlmap](https://img.shields.io/badge/sqlmap-27A844?style=for-the-badge&logo=sqlmap&logoColor=white)
![OWASP ZAP](https://img.shields.io/badge/OWASP%20ZAP-239120?style=for-the-badge&logo=owasp&logoColor=white)
![NLTK](https://img.shields.io/badge/NLTK-FFCC00?style=for-the-badge&logo=nltk&logoColor=black)

---

## 📊 **GitHub Stats & Activity**

![Thierry's GitHub stats](https://github-readme-stats.vercel.app/api?username=thierrynshimiyumukiza&show_icons=true&theme=radical)

![Activity Graph](https://activity-graph.herokuapp.com/graph?username=thierrynshimiyumukiza&theme=react-dark)

---

## ⚠️ **Important Notes**

- **NLTK** is required for **text summarization** features.  
- If you encounter missing tokenizer errors, run:

```bash
python -c "import nltk; nltk.download('punkt')"
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
                                          
  
  
  
  
  
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
                      
  
