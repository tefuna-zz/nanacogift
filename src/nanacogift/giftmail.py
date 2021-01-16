from logging import getLogger


log = getLogger(__name__)


class GiftMail:

    PREFIX_GIFT = "【PC・スマートフォン用】ギフトID付登録URL : "
    PREFIX_URL = "https"

    def __init__(self, path: str) -> None:
        self.__path = path
        log.info("path: %s", path)

    def read_mail(self) -> list:
        urls = []
        with open(self.__path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith(self.PREFIX_GIFT):
                    url = line[line.find(self.PREFIX_URL):].strip()
                    urls.append(url)

        log.info("count: %s, urls: %s", len(urls), urls)
        return urls
