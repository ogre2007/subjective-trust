"""module represents opinion class and its operations"""

from typing import Union, TypeVar

Opinion = TypeVar("Opinion", bound="Opinion")


class Opinion:
    """Opinion class and math opeartions"""

    def __init__(self, opvec: tuple):
        assert sum(opvec) == 1
        assert len(opvec) == 3
        assert all(x >= 0 or x <= 1 for x in opvec)

        self.belief = opvec[0]
        self.dis = opvec[1]
        self.uncert = opvec[2]

    def __getitem__(self, i: int) -> float:
        lst = [self.belief, self.dis, self.uncert]
        return lst[i]

    def __and__(self, other: Union[Opinion, tuple]) -> Opinion:
        """conjunction operator"""
        other = check_type(other)
        b = self.belief * other.belief
        d = self.dis + other.dis - self.dis * other.dis
        u = (
            self.belief * other.uncert
            + self.uncert * other.belief
            + self.uncert * other.uncert
        )
        return Opinion((b, d, u))

    def __mul__(self, other: Union[Opinion, tuple]) -> Opinion:
        """recommendation operator"""
        other = check_type(other)
        b = self.belief * other.belief
        d = self.belief * other.dis
        u = self.dis + self.uncert + self.belief * other.uncert
        return Opinion((b, d, u))

    def __add__(self, other: Union[Opinion, tuple]) -> Opinion:
        """Additive fusion operator"""
        other = check_type(other)
        b = self.belief * other.uncert + other.belief * self.uncert
        div = self.uncert + other.uncert - self.uncert * other.uncert
        b /= div

        d = self.dis * other.uncert + other.dis * self.uncert
        d /= div

        u = self.uncert * other.uncert
        u /= div

        return Opinion((b, d, u))

    def Exp(self) -> float:
        return self.belief + self.uncert/2

    def __str__(self) -> str:
        return f"{self[:]}"


def check_type(opin: Union[Opinion, tuple]) -> Opinion:
    """return opinion"""
    if isinstance(opin, Opinion) is not True:
        opin = Opinion(opin)
    return opin


if __name__ == "__main__":
    print("TEST")

    w = Opinion((1.0, 0, 0))
    x = (0.95, 0.04, 0.01)
    print(f"w1:{w}, w2:{x}")
    print(f"conj: {w & x}")
    print(f"rec {w * x}")
    print(f"fus {w + x}")
