import logging.config
import os
import sys
from logging import DEBUG, INFO, getLogger

import const as c

# ロガー設定
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)-3d %(levelname)-8s %(module)-18s %(funcName)-10s %(lineno)4s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
log = getLogger(__name__)
log.setLevel(INFO)


def main() -> None:
    """メイン関数。
    """

    # nanacoギフトメール読み込み
    urls = read_giftmail()
    log.info("GIFT COUNT: %s", len(urls))
    log.info("GIFT URLS: %s", urls)

    # ギフトURL書き込み
    write_gifturls(urls)


def read_giftmail() -> list:
    """nanacoギフトメールを読み込み、URLリストを返却する。

    Returns:
        list: nanacoギフトURL
    """

    urls = []   # ギフトURLリスト

    # nanacoギフトメールを読み込む。
    with open(c.PATH_MAIL, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith(c.PREFIX_GIFT):
                url = line[line.find(c.PREFIX_URL):].strip()
                urls.append(url)
    return urls


def write_gifturls(urls: list) -> None:
    """ギフトURLをファイル出力する。

    Args:
        urls (list): nanacoギフトURLリスト
    """
    # ギフトURLをファイル出力する。
    urls_lf = [url+'\n' for url in urls]
    with open(c.PATH_URLS, 'wt', encoding='utf-8') as f:
        f.writelines(urls_lf)


if __name__ == "__main__":
    main()
