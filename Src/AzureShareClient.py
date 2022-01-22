import os

from azure.core.exceptions import ResourceNotFoundError
from azure.storage.fileshare import ShareClient

class AzureShareClient:
    """
    Facade to interface with Azure File Shares.
    """

    def __init__(self, sas_token: str, account_url: str, share_name: str):
        self._azure_client_inner = ShareClient(
            account_url=account_url,
            share_name=share_name,
            credential=sas_token)

    def upload_file_to_root(self, file_path: str, overwrite_existing: bool=False):
        """
        Upload a file to the share's root.
        Blocks until file is uploaded
        :param file_path: local file path
        :param overwrite_existing: True if the client is allowed to overwrite an
            existing file of the same name in the file share
        :return: None
        """
        if not AzureShareClient._source_file_exists(file_path):
            print('Skipped upload of {}. Local file does not exist.'.format(file_path))
            return

        file_name = AzureShareClient._get_file_name(file_path)
        file_client = self._azure_client_inner.get_file_client(file_name)

        if not overwrite_existing and self._destination_file_exists(file_name):
            print('Skipped upload of {}. {} exists.'.format(file_path, file_name))
            return

        with open(file_path, "rb") as source_file:
            print('Uploading {} to {}...'.format(file_path, file_name))
            try:
                file_client.upload_file(source_file)
                print('SUCCESS {} to {}'.format(file_path, file_name))
            except Exception as err:
                print('FAILED {} to {}. {}'.format(file_path, file_name, err))

    @staticmethod
    def _get_file_name(file_path: str):
        return os.path.basename(file_path)

    @staticmethod
    def _source_file_exists(file_path: str) -> bool:
        return os.path.exists(file_path)

    def _destination_file_exists(self, file_name: str) -> bool:
        cleaned_file_name = AzureShareClient._get_file_name(file_name)
        file_client = self._azure_client_inner.get_file_client(cleaned_file_name)
        try:
            file_client.get_file_properties()
            return True
        except ResourceNotFoundError:
            return False

