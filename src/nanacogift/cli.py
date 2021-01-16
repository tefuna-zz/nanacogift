import logging.config
from logging import DEBUG, getLogger
from . import giftmail, giftpage


# setup logger.
logging.basicConfig(
    level=DEBUG,
    format='%(asctime)s.%(msecs)-3d %(levelname)-8s %(module)-18s %(funcName)-10s %(lineno)4s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
log = getLogger(__name__)
log.setLevel(DEBUG)


def main(path: str, number: str, cardno: str) -> None:
    """ Main function of nanacogift.

    Args:
        path (str): path to giftmail text.
        number (str): nanaco member's number.
        cardno (str): nanaco card number.
    """

    # read gift urls.
    mail = giftmail.GiftMail(path)
    urls = mail.read_mail()

    # register giftcode.
    page = giftpage.GiftPage(number, cardno, urls)
    page.register_gift()
