from concurrent.futures import ThreadPoolExecutor

from conf import settings
from utils import (
    get_batches,
    make_report,
    process_files,
)


def main():
    files_batch: list["Path"] = get_batches(data=settings.files, batch_size=settings.batch_size)
    with ThreadPoolExecutor(max_workers=settings.threads_quantity) as executor:
        futures = [executor.submit(lambda files: process_files(files), files) for files in files_batch]

        make_report(futures)


if __name__ == "__main__":
    main()
