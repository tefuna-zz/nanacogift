from nanacogift.cli import main
from nanacogift.giftmail import GiftMail


def test_main():
    print("bbb")


def test_main2():
    """[summary]
    """
    print("bbb")


def test_main3():
    assert "a" == "c"


def test_main4():
    g = GiftMail("aaaaa")
    print(dir(g))
