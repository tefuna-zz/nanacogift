import os
import time
from logging import getLogger

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


log = getLogger(__name__)


class GiftPage:

    DRIVER = os.path.dirname(__file__) + "\\..\\..\\driver\\chromedriver.exe"

    def __init__(self, number: str, cardno: str, urls: list):
        self.__number = number
        self.__cardno = cardno
        self.__urls = urls
        self.__driver = None
        self.__results = {"success": [], "duplicate": [], "failure": []}

    def register_gift(self) -> dict:

        for url in self.__urls:
            try:
                log.info("try registeration: %s", url)
                self.__init_driver()
                self.__register(url)
                self.__results["success"].append(url)
            except DuplicateException:
                self.__results["duplicate"].append(url)
            except:
                self.__results["failure"].append(url)
            finally:
                self.__driver.quit()
                time.sleep(3)

        self.__log_results()
        return

    def __init_driver(self) -> None:
        options = webdriver.ChromeOptions()
        options.add_argument('window-size=1200x600')
        driver = webdriver.Chrome(self.DRIVER, options=options)
        self.__driver = driver
        return

    def __register(self, url: str):

        # ログイン
        self.__driver.get(url)
        self.__driver.implicitly_wait(3)
        self.__driver.find_element_by_id(
            'nanacoNumber02').send_keys(self.__number)
        self.__driver.find_element_by_id(
            'cardNumber').send_keys(self.__cardno)
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
        giftpage_handle = self.__driver.window_handles[1]

        # ギフトコード確認
        self.__driver.switch_to.window(giftpage_handle)
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

        return

    def __log_results(self) -> None:
        log.info("PROCESS COUNT: success=%s, duplicate=%s, failure=%s",
                 len(self.__results["success"]),
                 len(self.__results["duplicate"]),
                 len(self.__results["failure"]))
        log.info("RESULT duplicate: %s", self.__results["duplicate"])
        log.info("RESULT failure: %s", self.__results["failure"])

        return


class DuplicateException(Exception):
    pass
