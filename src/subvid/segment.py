from pydantic import BaseModel
from typing import Optional

class Segment(BaseModel):
    start: float
    end: float
    text: str
    speaker: Optional[str] = None

    def duration(self) -> float:
        return self.end - self.start

    def __str__(self) -> str:
        return f"{self.start:.2f} - {self.end:.2f}: {self.text}"

    def to_srt_format(self, index: int) -> str:
        start_time = self.format_time(self.start)
        end_time = self.format_time(self.end)
        return f"{index}\n{start_time} --> {end_time}\n{self.text}\n"

    @staticmethod
    def format_time(seconds: float) -> str:
        hours = int(seconds / 3600)
        minutes = int((seconds % 3600) / 60)
        seconds = seconds % 60
        milliseconds = int((seconds - int(seconds)) * 1000)
        return f"{hours:02d}:{minutes:02d}:{int(seconds):02d},{milliseconds:03d}"
