from AzureShareClient import AzureShareClient
from BackupQueue import BackupQueue

if __name__ == '__main__':
    AZURE_SHARE_CONFIG_FILE_PATH = './Config/azureShareConfig.json'
    BACKUP_QUEUE_FILE_PATH = './Config/backupQueue.txt'

    client = AzureShareClient.init_by_file(AZURE_SHARE_CONFIG_FILE_PATH)

    backup_queue = BackupQueue(BACKUP_QUEUE_FILE_PATH)
    while True:
        try:
            (src_path, dest_path) = backup_queue.dequeue()
            if dest_path is not None:
                client.upload_file(str(src_path), dest_path=str(dest_path))
            else:
                client.upload_file(str(src_path))

        except IndexError:
            break
