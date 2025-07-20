import asyncio
from .base import BaseScanner
import shutil
from utils import extract_hostname

class NmapScanner(BaseScanner):
    name = "Nmap"

    @classmethod
    def is_installed(cls):
        return shutil.which("nmap") is not None

    async def scan(self):
        # Try to extract a valid hostname or IP; fallback to raw target if parsing fails
        hostname = extract_hostname(self.target)
        if not hostname:
            hostname = self.target.strip()
        if not hostname or "/" in hostname:
            return {"summary": "Nmap: Invalid target (cannot extract hostname).", "detailed": ""}
        try:
            proc = await asyncio.create_subprocess_exec(
                "nmap", "-Pn", hostname,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=90)
            output = stdout.decode() + stderr.decode()
        except asyncio.TimeoutError:
            return {"summary": "Nmap: Scan timed out.", "detailed": ""}
        except Exception as e:
            return {"summary": f"Nmap: Error: {e}", "detailed": ""}
        summary_lines = [line for line in output.splitlines() if ("open" in line and "/" in line)]
        summary = "\n".join(summary_lines) if summary_lines else "Nmap: No major findings."
        return {"summary": summary, "detailed": output}
