from AzureShareClient import AzureShareClient
from BackupQueue import BackupQueue

if __name__ == '__main__':
    SAS_TOKEN = '<sas_token_here>'
    ACCOUNT_URL = '<account_url_here>'
    SHARE_NAME = '<share_name_here>'

    BACKUP_QUEUE_FILE_PATH = './Config/backupQueue.txt'

    client = AzureShareClient(SAS_TOKEN, ACCOUNT_URL, SHARE_NAME)

    backup_queue = BackupQueue(BACKUP_QUEUE_FILE_PATH)
    while True:
        try:
            file_path = backup_queue.dequeue()
            client.upload_file_to_root(str(file_path))
        except IndexError:
            break
