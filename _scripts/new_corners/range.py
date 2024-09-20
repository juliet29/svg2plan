from dataclasses import dataclass
from decimal import Decimal
from collections import namedtuple
from log_setter.log_settings import logger


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

    # TODO check that min << max always.. ~ can use post init .. 

    @property
    def size(self):
        return self.max - self.min

    def __repr__(self) -> str:
        return f"[{self.min}-{self.max}]"
    
    def __getitem__(self, i):
        return getattr(self, i)

    # def overlaps(self, other):
    #     return not other.min < self.min and not other.max > self.max
    
    # def is_within(self, other):
    #     return other.min < self.min and other.max > self.max
    
    def is_larger(self, other):
        return self.min >= other.max
    
    def is_smaller(self, other):
        return self.max <= other.min
    
    def compare_ranges(self, other):
        if self.is_smaller(other):
            return ComparedRange(Lesser=self, Greater=other)
        elif self.is_larger(other):
            return ComparedRange(Lesser=other, Greater=self)
        else:
            return ComparedRange(Lesser=None, Greater=None)


@dataclass
class ComparedRange:
    Lesser: Range | None
    Greater: Range | None
    def __repr__(self) -> str:
        return f"(Lesser={self.Lesser}, Greater={self.Greater})"
    
    def is_empty(self):
        if not self.Lesser and not self.Greater:
            return True
        

            
