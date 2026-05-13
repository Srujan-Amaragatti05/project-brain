from dataclasses import dataclass


@dataclass
class DoctorCheck:
    category: str
    name: str
    status: str
    message: str
    fix: str = ""