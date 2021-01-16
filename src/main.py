import os
from nanacogift import cli

if __name__ == '__main__':

    # ログイン情報
    NUMBER = os.environ["NANACO_NUMBER_KEY"]
    CARDNO = os.environ["NANACO_CARDNO_KEY"]
    PATH = "C:\\workspace\\local-tools\\nanacogift\\data\\giftmail.txt"

    cli.main(PATH, NUMBER, CARDNO)
