import io
import json
import mimetypes
import os
import sys
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload


def download_file() -> None:
    file_name = os.getenv("FILE_NAME")
    file_id = os.getenv("FILE_ID")
    _download_file(file_id, file_name)


def _get_output_file_path() -> Path:
    chosen_path = os.getenv("DOWNLOAD_TO")
    mime_type = os.getenv("EXPORT_MEDIA_TYPE")
    output_file_path = Path(chosen_path)
    
    # add an appropriate extension if file_name does not
    # have an extension, and if we can guess the appropriate
    # extension
    if not output_file_path.suffix and mime_type:
        extension = mimetypes.guess_extension(mime_type)
        if extension:
            output_file_path = output_file_path.with_suffix(extension)

    return output_file_path


def _download_file(file_id: str, file_name: str) -> None:
    mime_type = os.getenv("EXPORT_MEDIA_TYPE")
    if mime_type:
        request = drive_service.files().export_media(
            fileId=file_id,
            mimeType=mime_type,
        )
    else:
        request = drive_service.files().get_media(fileId=file_id)
    output_path = _get_output_file_path()
    output_file_path = io.FileIO(output_path, 'w+b')
    downloader = MediaIoBaseDownload(output_file_path, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))


if __name__ == '__main__':
    service_account_info = json.loads(os.getenv("SERVICE_ACCOUNT_KEY_JSON"))
    credentials = service_account.Credentials.from_service_account_info(service_account_info)
    drive_service = build('drive', 'v3', credentials=credentials)
    download_file()
