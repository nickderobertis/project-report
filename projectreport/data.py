import datetime
from typing import Dict, Union

AnalysisData = Dict[str, Union["AnalysisData", str, int, None, datetime.date, datetime.datetime]]  # type: ignore
