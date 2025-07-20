import asyncio
from .base import BaseScanner
import shutil
from utils import ensure_url

class NiktoScanner(BaseScanner):
    name = "Nikto"

    @classmethod
    def is_installed(cls):
        return shutil.which("nikto") is not None

    async def scan(self):
        url = ensure_url(self.target)
        try:
            proc = await asyncio.create_subprocess_exec(
                "nikto", "-h", url,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=180)
            output = stdout.decode() + stderr.decode()
        except asyncio.TimeoutError:
            return {"summary": "Nikto: Scan timed out.", "detailed": ""}
        except Exception as e:
            return {"summary": f"Nikto: Error: {e}", "detailed": ""}
        # Grab lines with findings or vulnerabilities
        summary_lines = [line for line in output.splitlines() if "OSVDB" in line or "Server" in line or "vulnerab" in line or "finding" in line]
        summary = "\n".join(summary_lines) if summary_lines else "Nikto: No major findings."
        return {"summary": summary, "detailed": output}
