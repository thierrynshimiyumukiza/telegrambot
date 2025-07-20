import asyncio
from .base import BaseScanner
import shutil
from utils import ensure_url

class SqlmapScanner(BaseScanner):
    name = "sqlmap"

    @classmethod
    def is_installed(cls):
        return shutil.which("sqlmap") is not None

    async def scan(self):
        url = ensure_url(self.target)
        try:
            proc = await asyncio.create_subprocess_exec(
                "sqlmap", "-u", url, "--batch", "--crawl=1", "--level=1", "--risk=1", "--random-agent",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=240)
            output = stdout.decode() + stderr.decode()
        except asyncio.TimeoutError:
            return {"summary": "sqlmap: Scan timed out.", "detailed": ""}
        except Exception as e:
            return {"summary": f"sqlmap: Error: {e}", "detailed": ""}
        summary_lines = [line for line in output.splitlines() if "identified" in line or "possible" in line or "vulnerable" in line or "inject" in line]
        summary = "\n".join(summary_lines) if summary_lines else "sqlmap: No major findings."
        return {"summary": summary, "detailed": output}
