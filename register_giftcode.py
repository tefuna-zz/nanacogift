import logging.config
import os
import sys
import time
from logging import DEBUG, ERROR, INFO, getLogger

import bs4
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

import const as c

# ロガー設定
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d %(levelname)-8s %(module)-18s %(funcName)-10s %(lineno)4s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
log = getLogger(__name__)
log.setLevel(INFO)


class NanacoGift:

    def __init__(self, number: str, cardno: str, url: str):

        if not url.startswith(c.PREFIX_URL):
            raise ValueError("unexpected url: %s", url)

        self.__nanaco_number = number
        self.__nanaco_cardno = cardno
        self.__url = url

        # driver設定
        options = webdriver.ChromeOptions()
        options.add_argument('window-size=1200x600')
        driver = webdriver.Chrome(options=options)
        self.__driver = driver

    def register_gift(self) -> None:

        try:
            # ログイン
            self.__driver.get(self.__url)
            self.__driver.implicitly_wait(3)
            self.__driver.find_element_by_id(
                'nanacoNumber02').send_keys(self.__nanaco_number)
            self.__driver.find_element_by_id(
                'cardNumber').send_keys(self.__nanaco_cardno)
            self.__driver.find_element_by_id('loginPass02').click()

            # 会員メニュー→ギフト登録
            self.__driver.implicitly_wait(3)
            self.__driver.find_element_by_id('memberNavi02').click()

            # ギフトコード入力（別ウィンドウ）
            time.sleep(3)
            self.__driver.find_element_by_xpath(
                "//input[contains(@alt, '登録')]").click()
            WebDriverWait(self.__driver, 3).until(
                lambda d: len(d.window_handles) > 1)
            gift_page_handle = self.__driver.window_handles[1]

            # ギフトコード確認
            self.__driver.switch_to.window(gift_page_handle)
            self.__driver.find_element_by_id('submit-button').click()

            # すでに登録済みの場合はエラーとして終了
            self.__driver.implicitly_wait(3)
            if self.__driver.title == 'nanaco / ギフトID登録完了':
                raise DuplicateException()

            # ギフトコード登録
            self.__driver.find_element_by_xpath(
                "//input[contains(@alt, '登録する')]").click()

            # 登録チェック
            if not self.__driver.title == "nanaco / ギフトID登録完了":
                raise Exception()

            # 正常終了
            time.sleep(3)

        finally:
            self.__driver.quit()


class DuplicateException(Exception):
    pass


def main() -> None:

    # 前提チェック
    if not os.path.exists(c.PATH_URLS):
        raise Exception("file not found.")

    # ログイン情報
    number = os.environ[c.NANACO_NUMBER_KEY]
    cardno = os.environ[c.NANACO_CARDNO_KEY]

    # 結果
    results = {
        "success": [],
        "duplicate": [],
        "failure": []
    }

    # ギフト読み込み＋ギフト登録
    with open(c.PATH_URLS, 'r', encoding='utf-8') as f:
        urls = f.readlines()
        for url in urls:
            try:
                nanaco = NanacoGift(number, cardno, url)
                nanaco.register_gift()
            except ValueError as ve:
                log.info("skip url: %s", url)
            except DuplicateException as de:
                results["duplicate"].append(url)
            except:
                results["failure"].append(url)
            else:
                results["success"].append(url)

    # 結果出力
    log.info("PROCESS COUNT: success=%s, duplicate=%s, failure=%s",
             len(results["success"]),
             len(results["duplicate"]),
             len(results["failure"]))
    log.info("RESULT duplicate: %s", results["duplicate"])
    log.info("RESULT failure: %s", results["failure"])


if __name__ == "__main__":
    main()
