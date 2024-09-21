from dataclasses import dataclass
from decimal import Decimal


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

    def is_covering(self, other):
        return self.min <= other.min and self.max >= other.max

    def is_covered_by(self, other):
        return other.min <= self.min and other.max >= self.max
    
    def is_sharing_space_with(self, other):
        return other.min <= self.min or  other.max >= self.max
    
    def is_partially_overlapping(self, other):
        return self.is_sharing_space_with(other) and not self.is_covered_by(other) and not self.is_covering(other)


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


@dataclass
class ComparedRange:
    Lesser: Range | None
    Greater: Range | None

    def __repr__(self) -> str:
        return f"(Lesser={self.Lesser}, Greater={self.Greater})"

    def is_empty(self):
        if not self.Lesser and not self.Greater:
            return True
