import logging
import time
from logging.handlers import RotatingFileHandler

import requests
from secrets import camera_fingerprint, image_source_url, prusa_camera_api_token  # gitignored for security


PRUSA_CONNECT_URL = "https://webcam.connect.prusa3d.com/c/snapshot"
POLL_INTERVAL_SECONDS = 10
SNAPSHOT_TIMEOUT_SECONDS = 10
UPLOAD_TIMEOUT_SECONDS = 15
MAX_SNAPSHOT_SIZE_BYTES = 16 * 1024 * 1024  # API limit: 16 MiB
LOG_FILE = "prusa-connect-camera-upload.log"
LOG_MAX_BYTES = 1 * 1024 * 1024  # 1 MiB
LOG_BACKUP_COUNT = 5


def setup_logging():
    """Configure console + rolling file logging for long-running usage."""
    logger = logging.getLogger("prusa_camera_uploader")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=LOG_MAX_BYTES,
        backupCount=LOG_BACKUP_COUNT,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.handlers.clear()
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger

def fetch_snapshot(session, url, logger):
    """
    Fetches a snapshot from the given URL and returns the image data.

    Parameters:
    - url (str): The URL of the snapshot.

    Returns:
    - bytes: The image data if successful.
    - None: If there was an error fetching the snapshot.
    """
    try:
        response = session.get(url, timeout=SNAPSHOT_TIMEOUT_SECONDS)
        if response.status_code == 200:
            return response.content

        logger.warning("Snapshot fetch failed with status code %s", response.status_code)
        return None
    except requests.RequestException as exc:
        logger.warning("Snapshot fetch failed: %s", exc)
        return None

def upload_image(session, http_url, fingerprint, token, image):
    """Upload an image over http"""
    response = session.put(
        http_url,
        headers={
            "accept": "*/*",
            "content-type": "image/jpg",
            "fingerprint": fingerprint,
            "token": token,
        },
        data=image,
        timeout=UPLOAD_TIMEOUT_SECONDS,
    )
    return response
    
def main():
    logger = setup_logging()
    logger.info("Starting Prusa Connect camera uploader")
    session = requests.Session()

    try:
        while True:
            try:
                image = fetch_snapshot(session, image_source_url, logger)
                if not image:
                    logger.warning("Skipping upload because snapshot retrieval failed")
                    continue

                if len(image) > MAX_SNAPSHOT_SIZE_BYTES:
                    logger.warning(
                        "Skipping upload because snapshot is too large: %s bytes (max %s)",
                        len(image),
                        MAX_SNAPSHOT_SIZE_BYTES,
                    )
                    continue

                response = upload_image(
                    session,
                    PRUSA_CONNECT_URL,
                    camera_fingerprint,
                    prusa_camera_api_token,
                    image,
                )
                if response.status_code == 204:
                    logger.info(
                        "Uploaded snapshot (%s bytes), response status=204",
                        len(image),
                    )
                else:
                    if response.status_code in (401, 403, 404):
                        logger.error(
                            "Upload auth/resource error: status=%s, body=%s",
                            response.status_code,
                            response.text[:300],
                        )
                    logger.warning(
                        "Upload failed with status code %s, body=%s",
                        response.status_code,
                        response.text[:300],
                    )
            except requests.RequestException as exc:
                logger.exception("Network error in upload loop: %s", exc)
            except (OSError, ValueError, TypeError, RuntimeError) as exc:
                logger.exception("Unexpected error in upload loop: %s", exc)
            finally:
                time.sleep(POLL_INTERVAL_SECONDS)
    except KeyboardInterrupt:
        logger.info("Program interrupted and stopped")
    finally:
        session.close()
        

if __name__ == "__main__":
    main()
