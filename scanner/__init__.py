from .nmap import NmapScanner
from .nikto import NiktoScanner
from .sqlmap import SqlmapScanner
from .zap import ZapScanner

SCANNERS = [NmapScanner, NiktoScanner, SqlmapScanner, ZapScanner]
