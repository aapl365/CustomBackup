from AzureShareClient import AzureShareClient
from BackupQueue import BackupQueue
from Scheduler import Scheduler

if __name__ == '__main__':
    AZURE_SHARE_CONFIG_FILE_PATH = './Config/azureShareConfig.json'
    BACKUP_QUEUE_FILE_PATH = './Config/backupQueue.txt'

    client = AzureShareClient.init_by_file(AZURE_SHARE_CONFIG_FILE_PATH)

    backup_queue = BackupQueue(BACKUP_QUEUE_FILE_PATH)

    try:
        while True:
            if not Scheduler.is_low_traffic_time():
                print('Not low traffic time. Ending')
                exit(0)

            try:
                (src_path, dest_path) = backup_queue.dequeue()
            except IndexError:
                print('DONE. No items in queue?')
                break

            if dest_path is not None:
                client.upload_file(str(src_path), dest_path=str(dest_path))
            else:
                client.upload_file(str(src_path))

    except Exception as e:
        print('FAIL exited main loop: ', e)
