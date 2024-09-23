# for all adjacent nodes, check if one is within another.. 
# define on range, then on domain
# first check that the ranges are not equal.. 
import typing


Argument = typing.Literal['foo', 'bar']
# VALID_ARGUMENTS: typing.Tuple[Argument, ...] = typing.get_args(Argument)


class Test:
    def __init__(self, a:Argument ) -> None:
        self.a: Argument 
        self.b: int

# https://stackoverflow.com/questions/64522040/dynamically-create-literal-alias-from-list-of-valid-values