class BaseScanner:
    name = "BaseScanner"

    def __init__(self, target):
        self.target = target

    async def scan(self):
        raise NotImplementedError("Each scanner must implement the scan() method.")

    @classmethod
    def is_installed(cls):
        # Override to check if the tool is installed
        return True
