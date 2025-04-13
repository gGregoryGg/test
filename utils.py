import re
from operator import add
from itertools import islice
from collections import defaultdict
from typing import (
    Iterable,
    Any,
)

from conf import settings

PATTERN = re.compile(r"^\s*\S+\s+\S+\s+(\S+)\s+django\.request:.*?(/[^ ]+)")
template = {
    "DEBUG": 0,
    "INFO": 1,
    "WARNING": 2,
    "ERROR": 3,
    "CRITICAL": 4,
}


def get_batches(data: Iterable[Any], batch_size: int = 2) -> list[Any]:
    if batch_size > 0:
        div, mod = divmod(len(data), batch_size)
        mod = 1 if len(data) % batch_size else 0
        it = iter(data)
        return [list(islice(it, batch_size)) for _ in range(div + mod)]
    raise ValueError


def get_info(line: str) -> None | tuple:
    match: re.Match = PATTERN.match(line)
    if match:
        return match.groups()
    return None


def get_file_iter(file_path):
    with open(file_path, mode="r") as f:
        for line in f:
            yield line.strip()


def process_file(file_path) -> dict:
    result: dict = defaultdict(lambda: [0] * 5)
    for line in get_file_iter(file_path):
        info: tuple[str, str] | None = get_info(line)
        if info:
            level, endpoint = info
            result[endpoint][template[level]] += 1
    return result


def process_files(files) -> list[dict]:
    return [process_file(file) for file in files]


def save(data: dict, quantity: int) -> None:
    report: str = ""
    headers: list[str] = ["HANDLER"] + list(template.keys())

    col_widths: list = [
        max(len(headers[0]), max(len(handler) for handler in data.keys())) + 2,
        *[max(len(level), 7) + 2 for level in template.keys()],
    ]

    report += f"\nTotal requests: {quantity}\n\n"

    header_line: str = "".join(f"{header:<{width}}" for header, width in zip(headers, col_widths))

    report += header_line + "\n" + "-" * len(header_line) + "\n"

    for handler, counts in data.items():
        row = [handler] + [str(counts[template[level]]) for level in template.keys()]
        row_line = "".join(f"{cell:<{width}}" for cell, width in zip(row, col_widths))
        report += row_line + "\n"
    if settings.report_file_name:
        with open(settings.report_file_name, mode="w") as f:
            f.write(report)
            f.close()
    else:
        print(report)


def make_report(futures: list["Future"]) -> None:
    result = defaultdict(lambda: [0] * 5)
    for future in futures:
        results = future.result()
        for res in results:
            for key, values in res.items():
                result[key] = list(map(add, result[key], values))
    quantity = sum(sum(lst) for lst in result.values())
    save(result, quantity)
