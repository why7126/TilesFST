"""Strip signed capabilities and storage paths even when nested under unexpected keys."""
import re
import logging
import traceback

_SIGNED = re.compile(r'(?:https?://|/api/v1/media/read\?)[^\s<>\"\']+', re.I)
_QUERY_SECRET = re.compile(r'(?:[?&]|^)(?:ticket|signature|q-signature|q-ak|q-key-time|x-amz-signature|x-amz-credential|x-amz-security-token)=', re.I)
_KEY = re.compile(r'(?:/media/)?(?:images|original|files|videos|thumbnails|tmp)/[a-zA-Z0-9_./%+-]+')
_JWT = re.compile(r'\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b')


def redact_media_text(value: str) -> str:
    value = _SIGNED.sub(lambda match: '******' if _QUERY_SECRET.search(match.group()) else match.group(), value)
    return _JWT.sub('******', _KEY.sub('******', value))


class MediaAccessLogFilter(logging.Filter):
    def filter(self, record):
        if isinstance(record.args, tuple):
            record.args = tuple(redact_media_text(value) if isinstance(value, str) else value for value in record.args)
        if isinstance(record.msg, str):
            record.msg = redact_media_text(record.msg)
        if record.exc_info:
            record.exc_text = redact_media_text(''.join(traceback.format_exception(*record.exc_info)))
            record.exc_info = None
        return True


def install_media_access_log_filter():
    for name in ("uvicorn.access", "uvicorn.error"):
        logger = logging.getLogger(name)
        if not any(isinstance(item, MediaAccessLogFilter) for item in logger.filters):
            logger.addFilter(MediaAccessLogFilter())
