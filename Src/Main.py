from AzureShareClient import AzureShareClient
from BackupQueue import BackupQueue

if __name__ == '__main__':
    AZURE_SHARE_CONFIG_FILE_PATH = './Config/azureShareConfig.json'
    BACKUP_QUEUE_FILE_PATH = './Config/backupQueue.txt'

    client = AzureShareClient.init_by_file(AZURE_SHARE_CONFIG_FILE_PATH)

    backup_queue = BackupQueue(BACKUP_QUEUE_FILE_PATH)
    while True:
        try:
            file_path = backup_queue.dequeue()
            client.upload_file_to_root(str(file_path))
        except IndexError:
            break
