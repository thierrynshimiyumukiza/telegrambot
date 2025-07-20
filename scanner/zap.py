import asyncio
from .base import BaseScanner
import shutil
from utils import ensure_url

class ZapScanner(BaseScanner):
    name = "OWASP ZAP"

    @classmethod
    def is_installed(cls):
        return shutil.which("zap-cli") is not None or shutil.which("zaproxy") is not None

    async def scan(self):
        url = ensure_url(self.target)
        if shutil.which("zap-cli"):
            cmd = ["zap-cli", "quick-scan", url]
        elif shutil.which("zaproxy"):
            cmd = ["zaproxy", "-cmd", "-quickurl", url]
        else:
            return {"summary": "OWASP ZAP not installed.", "detailed": ""}
        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=240)
            output = stdout.decode() + stderr.decode()
        except asyncio.TimeoutError:
            return {"summary": "OWASP ZAP: Scan timed out.", "detailed": ""}
        except Exception as e:
            return {"summary": f"OWASP ZAP: Error: {e}", "detailed": ""}
        # Look for alerts or issues of interest in output
        keywords = ["High", "Medium", "Alert", "Vulnerab", "finding"]
        summary_lines = [line for line in output.splitlines() if any(k in line for k in keywords)]
        summary = "\n".join(summary_lines) if summary_lines else "OWASP ZAP: No major findings."
        return {"summary": summary, "detailed": output}
