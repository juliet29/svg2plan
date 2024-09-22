from dataclasses import dataclass
from decimal import Decimal
from typing import Callable
from log_setter.log_settings import logger
from copy import copy, deepcopy


class InvalidRangeException(Exception):
    pass


@dataclass(frozen=True)
class nonDecimalRange:
    min: float
    max: float

    def toRange(self):
        return Range(Decimal(self.min), Decimal(self.max))


@dataclass(frozen=True)
class Range:
    min: Decimal
    max: Decimal

    def __post_init__(self):
        try:
            assert self.min < self.max
        except AssertionError:
            raise InvalidRangeException

    def __repr__(self) -> str:
        return f"[{self.min}-{self.max}]"

    def __getitem__(self, i):
        return getattr(self, i)

    @property
    def size(self):
        return self.max - self.min

    def is_larger(self, other):
        return self.min >= other.max

    def is_smaller(self, other):
        return self.max <= other.min

    def is_overlapping_and_larger(self, other):
        return self.max > other.max and other.min <= self.min <= other.max

    def is_overlapping_and_smaller(self, other):
        return self.min < other.min and other.min <= self.max <= other.max

    def compare_ranges(self, other, consider_overlap=False):
        if self.is_smaller(other):
            return ComparedRange(Lesser=self, Greater=other)
        elif self.is_larger(other):
            return ComparedRange(Lesser=other, Greater=self)
        else:
            if consider_overlap:
                if self.is_overlapping_and_smaller(other):
                    return ComparedRange(Lesser=self, Greater=other)
                elif self.is_overlapping_and_larger(other):
                    return ComparedRange(Lesser=other, Greater=self)
            return ComparedRange(Lesser=None, Greater=None)

    def get_other_side(self, side: str):
        [other_side] = set(self.__annotations__.keys()).difference({side})
        return other_side
    
    def modify(self, fx: Callable[[Decimal], Decimal]):
        return self.__class__(fx(self.min), fx(self.max) )
    
    @classmethod
    def create_range(cls, a:Decimal, b:Decimal):
        return cls(a, b)


@dataclass
class ComparedRange:
    Lesser: Range | None
    Greater: Range | None

    def __repr__(self) -> str:
        return f"(Lesser={self.Lesser}, Greater={self.Greater})"

    def is_empty(self):
        if not self.Lesser and not self.Greater:
            return True

