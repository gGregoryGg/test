import argparse
from pathlib import Path

from pydantic import (
    BaseModel,
    model_validator,
)


class Settings(BaseModel):
    threads_quantity: int = 3
    batch_size: int = 2
    files: list[Path] | None = None
    report_file_name: Path | None = None

    @model_validator(mode="before")
    @classmethod
    def validate(cls, v: dict):
        files, report = cls.get_args()
        res = {
            "files": [vi for vi in [Path(p) for p in files] if vi.exists()],
            "report_file_name": report if report is not None and report in ["handlers"] else None,
        }
        return res

    @staticmethod
    def get_args():
        parser = argparse.ArgumentParser()
        parser.add_argument("files", nargs="+", help="Paths to log files to analyze")
        parser.add_argument("--report", help="handlers")

        arg = parser.parse_args()
        return arg.files, arg.report


settings = Settings()
