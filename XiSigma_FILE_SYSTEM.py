class FileSystem:
    def __init__(self):
        pass

    def read_file(self, path):
        return "Mock Content"

    def write_file(self, path, content):
        print(f"[MOCK FS] Writing to {path}")
        return True
