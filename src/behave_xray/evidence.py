import base64
from typing import AnyStr, Dict

from behave_xray.exceptions import XrayError

# Content Types
IMAGE_JPEG: str = 'image/jpeg'
IMAGE_PNG: str = 'image/png'
PLAIN_TEXT: str = 'plain/text'
CSV: str = 'plain/csv'
JSON: str = 'plain/json'
ZIP: str = 'application/zip'
XML: str = 'application/xml'
GZIP: str = 'appliaction/gzip'


def evidence(data: AnyStr, filename: str, content_type: str) -> Dict[str, str]:
    if isinstance(data, bytes):
        data_base64: str = base64.b64encode(data).decode('utf-8')
    elif isinstance(data, str):
        data_base64 = base64.b64encode(data.encode('utf-8')).decode('utf-8')
    else:
        raise XrayError('data must be string or bytes')

    return {
        'data': data_base64,
        'filename': filename,
        'contentType': content_type
    }


def jpeg(data: AnyStr, filename: str) -> Dict[str, str]:
    return evidence(data, filename, IMAGE_JPEG)


def png(data: AnyStr, filename: str) -> Dict[str, str]:
    return evidence(data, filename, IMAGE_PNG)


def text(data: AnyStr, filename: str) -> Dict[str, str]:
    return evidence(data, filename, PLAIN_TEXT)


def csv(data: AnyStr, filename: str) -> Dict[str, str]:
    return evidence(data, filename, CSV)


def json(data: AnyStr, filename: str) -> Dict[str, str]:
    return evidence(data, filename, JSON)


def xml(data: AnyStr, filename: str) -> Dict[str, str]:
    return evidence(data, filename, XML)


def zip(data: AnyStr, filename: str) -> Dict[str, str]:
    return evidence(data, filename, ZIP)


def gzip(data: AnyStr, filename: str) -> Dict[str, str]:
    return evidence(data, filename, GZIP)
