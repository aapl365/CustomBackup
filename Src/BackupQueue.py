from pathlib import Path

class BackupQueue:
    """
    Holds queue of what files or directories to backup.
    """
    _SRC_DEST_DELIMETER = '::'

    def __init__(self, queue_file_path):
        self._queue = []
        with open(queue_file_path, 'r') as queue_file:
            for line in queue_file:
                self.enqueue_file_line(line)

    def enqueue_file_line(self, file_line: str):
        cleaned_line = file_line.strip()
        if cleaned_line.startswith('#'):
            return

        src_dest_split = cleaned_line.split(BackupQueue._SRC_DEST_DELIMETER)
        if len(src_dest_split) == 2:
            # Destination path provided
            self.enqueue(src_dest_split[0], src_dest_split[1])
        else:
            # Only source path provided
            self.enqueue(cleaned_line)

    def enqueue(self, src_path: str, dest_path: str=None):
        src = Path(src_path.strip())
        dest = Path(dest_path.strip()) if dest_path is not None else None
        self._queue.append((src, dest))

    def dequeue(self) -> Path:
        return self._queue.pop(0)
