from pathlib import Path

class BackupQueue:
    """
    Holds queue of what files or directories to backup.
    """
    def __init__(self, queue_file_path):
        self._queue = []
        with open(queue_file_path, 'r') as queue_file:
            for line in queue_file:
                cleaned_line = line.strip()
                if not cleaned_line.startswith('#'):
                    self.enqueue(cleaned_line)

    def enqueue(self, file_path: str):
        self._queue.append(Path(file_path))

    def dequeue(self) -> Path:
        return self._queue.pop(0)
