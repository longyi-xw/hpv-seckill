import re
from typing import Optional
from decorator import handle_exceptions
from urllib.parse import quote
from md5 import hexMd5
import requests

# 登陆用户信息 (没有应该也没有影响，会根据tk查询你的信息)
LOGIN_USER = """
{

};
"""


@handle_exceptions
class MiaoApp:
    """
    秒苗api
    """

    __key = "ux$ad70*b"
    api = "https://miaomiao.scmttec.com/seckill"
    request: dict = { }
    tgw_cookie = { }

    def __init__(self, tk):
        self.tk = tk
        self.request["headers"] = {
            "Host": "miaomiao.scmttec.com",
            "Connection": "keep-alive",
            "Cookie": "",
            "tk": tk,
            "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.20(0x1800142f) NetType/WIFI Language/zh_CN",
            "Content-Type": "application/json",
            "Accept": "application/json, text/plain, */*",
            "referer": "https://servicewechat.com/wxff8cad2e9bf18719/37/page-frame.html",
            "xweb_xhr": "1",
            "X-Requested-With": "XMLHttpRequest",
            "Accept-Encoding": "gzip, deflate, br"
        }
        # proxyman ssl证书(非proxyman抓包软件可取消)
        self.request['verify'] = "/Users/xxx/.proxyman/proxyman-ca.pem"
        self.request['headers']['Cookie'] = self.__get_cookie()
        self.session = requests.session()

    def getUser(self, name: str, card_id: str, suffix="/linkman/findByUserId.do") -> Optional[dict]:
        """
        接种人接口
        :param name:
        :param card_id:
        :param suffix:
        :return:
        """
        self.request['url'] = self.api + suffix
        result = self.session.get(**self.request)
        users = list(result.json()['data'])
        if users is not None:
            return [u for u in users if u['name'] == name and u['idCardNo'] == card_id][0]
        return None

    def getMiaoList(self, suffix='/seckill/list.do') -> list:
        """
        疫苗接口
        8806: 2
        8802: 4
        8803: 9
        :param suffix:
        :return:
        """
        self.request['url'] = self.api + suffix
        self.request['params'] = {
            'offset': '0',
            'limit': '10',
            'regionCode': '5101'
        }
        result = self.session.get(**self.request)
        return result.json()

    def checkStock(self, m_id: str, suffix="/seckill/checkstock2.do"):
        """
        获取st验证是否还有余苗
        :param m_id:
        :param suffix:
        :return {stock: 1 | 0, st: dateTime}:
        "set-cookie"
        """
        self.request['url'] = self.api + suffix
        self.request['params'] = { 'id': m_id }
        result = self.session.get(**self.request)
        self.request['headers']['Cookie'] = self.__get_cookie() + self.__get_tgw_cookie(result.headers['Set-Cookie'])
        return result.json()

    def submitOrder(self, seckill_id: str, u_id: str, card_id: str, st: str, suffix="/seckill/subscribe.do"):
        """
        提交秒杀接口
        :param seckill_id:
        :param u_id:
        :param card_id:
        :param st:
        :param suffix:
        :return:
        """
        self.request['headers']['Content-Type'] = "application/x-www-form-urlencoded;charset=UTF-8"
        self.request['headers']['ecc-hs'] = self.set_ecc_hs(seckill_id, u_id, st)
        self.request['headers']['isFormData'] = "[object Boolean]"
        self.request['url'] = self.api + suffix
        self.request['data'] = {
            "seckillId": seckill_id,
            "linkmanId": u_id,
            "idCardNo": card_id
        }
        result = self.session.post(**self.request)
        return result.json()

    def set_ecc_hs(self, ms_id, u_id, st):
        """
        生成ecc-hs
        :param ms_id: 秒杀id
        :param u_id: 接种人id
        :param st: checkstock 返回时间戳
        :return:
        """
        return hexMd5(hexMd5(f"{ms_id}{u_id}{st}") + self.__key)

    def __get_cookie(self):
        login_user = quote(LOGIN_USER.replace("\n", "").replace(" ", ""), safe='~()*!.\'').replace("/", "%2F")
        self.cookie = f"_xxhm_={login_user}_xzkj_={self.tk};"
        return self.cookie

    def __get_tgw_cookie(self, set_cookies: str):
        """
        tgw_cookie 不知道有什么用，但秒杀的时候有这个，所以就加上
        :param set_cookies:
        :return:
        """
        set_cookies = set_cookies.split(";")
        filter_keywords = ["path", "Max-Age", "Expires"]
        filter_cookies = [x for x in set_cookies if all(y not in x for y in filter_keywords)]
        for keyword in filter_cookies:
            pattern = r"\b[A-Za-z0-9]{4}=[A-Za-z0-9]+\b"
            match = re.findall(pattern, keyword)
            key, value = ["", ""]
            if keyword.startswith("tgw_l7_route"):
                key, value = keyword.split("=")
            elif match:
                key, value = match[0].split("=")
            self.tgw_cookie[key] = value
        tgw_cookie = ""
        for key, value in self.tgw_cookie.items():
            tgw_cookie += f"{key}={value};"
        return tgw_cookie
