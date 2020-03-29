from collections import UserList
from typing import Any, Iterable, Sequence


class RotatingList(UserList):
    """
    A list which will hold only max_len items. Once more items are added then
    can fit in the list, items will be removed.

    When appending or extending items which will make the list larger than
    max_len, the earliest items in the list will
    be removed. When inserting an item which will make the list larger than
    max_len, the last item will be removed.
    """

    def __init__(self, items: Sequence[Any], max_len: int):
        self.max_len = max_len
        super().__init__(items)

    def append(self, item: Any):
        if len(self) == self.max_len:
            self.pop(0)
        super().append(item)

    def insert(self, index: int, item: Any):
        if len(self) == self.max_len:
            self.pop(-1)
        super().insert(index, item)

    def extend(self, items: Iterable[Any]):
        # TODO [#4]: more efficient implementation of RotatingList.extend
        [self.append(item) for item in items]
        # if len(items) >= self.max_len:
        #     self.data = items[-self.max_len:]
        # elif len(self) + len(items) > self.max_len:
