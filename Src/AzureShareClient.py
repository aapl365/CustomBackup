import json
import os

from azure.core.exceptions import ResourceNotFoundError
from azure.storage.fileshare import ShareClient

class AzureShareClient:
    """
    Facade to interface with Azure File Shares.
    """

    # Config file keys
    _SAS_TOKEN = 'SAS_TOKEN'
    _ACCOUNT_URL = 'ACCOUNT_URL'
    _SHARE_NAME = 'SHARE_NAME'

    def __init__(self, sas_token: str, account_url: str, share_name: str):
        self._azure_client_inner = ShareClient(
            account_url=account_url,
            share_name=share_name,
            credential=sas_token)

    @classmethod
    def init_by_file(cls, file_path: str):
        with open(file_path, 'r') as client_file:
            config = json.load(client_file)
        return cls(config[AzureShareClient._SAS_TOKEN],
                   config[AzureShareClient._ACCOUNT_URL],
                   config[AzureShareClient._SHARE_NAME] )

    def create_dir_in_root(self, dir_name: str):
        # TODO allow this to create nested directories.
        # Currently fails with azure.core.exceptions.ResourceNotFoundError
        if self._destination_dir_exists(dir_name):
            print('Skipped creating directory. {} exists'.format(dir_name))
            return

        dir_client = self._azure_client_inner.get_directory_client(dir_name)
        dir_client.create_directory()
        print('Created directory {}'.format(dir_name))

    def upload_file(self, file_path: str, dest_path: str=None, overwrite_existing: bool=False):
        """
        Upload a file to the share's root.
        Blocks until file is uploaded
        :param file_path: local file path
        :param dest_path: destination path for the upload. Defaults to the
            share's root if not specified. Directories must exist in the
            share if the path is nested.
        :param overwrite_existing: True if the client is allowed to overwrite an
            existing file of the same name in the file share
        :return: None
        """
        if not AzureShareClient._source_file_exists(file_path):
            print('Skipped upload of {}. Local file does not exist.'.format(file_path))
            return

        file_name = AzureShareClient._get_file_name(file_path)
        if dest_path is not None:
            file_name = dest_path
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

    def _destination_file_exists(self, file_path: str) -> bool:
        file_client = self._azure_client_inner.get_file_client(file_path)
        try:
            file_client.get_file_properties()
            return True
        except ResourceNotFoundError:
            return False

    def _destination_dir_exists(self, dir_path: str) -> bool:
        dir_client = self._azure_client_inner.get_directory_client(dir_path)
        try:
            dir_client.get_directory_properties()
            return True
        except ResourceNotFoundError:
            return False

    @staticmethod
    def _get_file_name(file_path: str):
        return os.path.basename(file_path)

    @staticmethod
    def _source_file_exists(file_path: str) -> bool:
        return os.path.exists(file_path)

