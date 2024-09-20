from dataclasses import dataclass
from decimal import Decimal
from collections import namedtuple


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

    def __repr__(self) -> str:
        return f"Range({self.min}, {self.max})"

    def overlaps(self, other):
        return not other.min < self.min and not other.max > self.max
    
    def is_within(self, other):
        return other.min < self.min and other.max > self.max
    
    def is_larger(self, other):
        return self.min >= other.max
    
    def is_smaller(self, other):
        return self.max <= other.min
    
    def compare_ranges(self, other):
        if self.__eq__(other):
            print(f"{self} equals {other}")
            return 
        if self.overlaps(other):
            print(f"{self} overlaps {other}")
            return 
        if self.is_within(other):
            print(f"{self} is within {other}")
            return 
        
        if self.is_smaller(other):
            return ComparedRange(Lesser=self, Greater=other)
        
        if self.is_larger(other):
            return ComparedRange(Lesser=other, Greater=self)


@dataclass
class ComparedRange:
    Lesser: Range
    Greater: Range
    def __repr__(self) -> str:
        return f"(Lesser={self.Lesser}, Greater={self.Greater})"
        

            
