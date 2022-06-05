from datetime import datetime
from typing import Any, Callable, Dict, List, Sequence, Union

from github.Repository import Repository

from projectreport.analyzer.ts.types import DictList


class TimeSeriesAnalysis:
    analysis_attrs: Sequence[str] = tuple()

    def get_event_data(self, item: str, **kwargs) -> DictList:
        func = self.event_functions[item]
        return func(*self.analysis_items, **kwargs)

    def get_counts(self, item: str, freq: str, **kwargs) -> DictList:
        event_data = self.get_event_data(item)
        func = self.count_functions[item]
        return func(event_data, freq, **kwargs)

    @property
    def event_functions(self) -> Dict[str, Callable]:
        raise NotImplementedError

    @property
    def count_functions(self) -> Dict[str, Callable]:
        raise NotImplementedError

    @property
    def analysis_items(self) -> List[Any]:
        return [getattr(self, attr) for attr in self.analysis_attrs]

    @property
    def supported_items(self) -> List[str]:
        return list(self.event_functions.keys())
