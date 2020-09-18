import urllib.request
import zipfile
from os import remove
from pathlib import Path

def request_file(url, filename, zipped=True):
    if zipped:
        urllib.request.urlretrieve(url, filename)
        with zipfile.ZipFile(filename, 'r') as zip_ref:
            zip_ref.extractall('')
        # Removes hashfile (if generated)
        if Path(filename[:-4]+'.sha256sum').is_file():
            remove(filename[:-4]+'.sha256sum')
        # Removes zipfile
        remove(filename)
    else:
        urllib.request.urlretrieve(url, filename)


if __name__ == '__main__':
    pass
    request_file('https://bin.arnastofnun.is/django/api/nidurhal/?file=ordmyndir.txt.zip', 'ordmyndir.txt.zip')
    request_file('https://bin.arnastofnun.is/django/api/nidurhal/?file=SHsnid.csv.zip', 'SHsnid.csv.zip')
