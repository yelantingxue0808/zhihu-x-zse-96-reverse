"""
@Author  : 孔天宇
@Desc    : 
"""
import pprint
from hashlib import md5
from urllib.parse import urlencode

import requests
# execjs Windows中文编码修复
import subprocess
from functools import partial

subprocess.Popen = partial(subprocess.Popen, encoding='utf-8')

import execjs


class CrawlData:
    def __init__(self):
        self.content = input('请输入要查询的内容：')
        self.params = {
            'gk_version': 'gz-gaokao',
            't': 'general',
            'q': self.content,
            'correction': '1',
            'offset': '20',
            'limit': '20',
            'filter_fields': '',
            'lc_idx': '0',
            'show_all_topics': '0',
            'search_source': 'Suggestion',
            'zhida_source': 'ai_search_general',
        }
        self.er = "/api/v4/search_v3?" + urlencode(self.params)

        self.url = 'https://www.zhihu.com/api/v4/search_v3'
        self.cookies = {
            '_zap': '4c8043a7-ad81-4d6d-8ef9-978a40489ae8',
            '_xsrf': '8faf82ab-3597-4ac6-953e-9279a601cd36',
            'd_c0': 'ZKXZnD4k8xyPTou8z5PIzci3L5h5ShTFAK4=|1790133292',
            'Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49': '1790133293',
            'HMACCOUNT': '2C034BA00C40162A',
            '__snaker__id': '4HN6to0IIkpJ7HtZ',
            'SESSIONID': 'eWCZJuJgpr3IP2wBe3K0W4npF6Zby6fJ0aPKxU19uF1',
            'gdxidpyhxdE': '2DM2gEMf07idDd9DT2TnPE8nf0ojZS2ILx74Wqy%5Ci2njstxZ3WX%2B5QfIYaRvX0y6LHEYR80fav7HavDkN4uKmuSJX1R56lVcMgdMV0zLdfuVLsIq4N5ZEbYg%2BbI6j0YapvtoolNRAuwS2cDRBQfna%5CDdXQCtTO9VILsyBUEDSk8UPXyQ%3A1790134196497',
            'JOID': 'UVoWB0rMTP-FBF6FJg2uqIdEfXU6qBq72kwqzka-P83LUW7zZeMOTugHXoMkrAw4qULJuLlglhwz34Gpt8CaiWc=',
            'osd': 'U1sRBkjOTfiEBlyEIQysqoZDfHc4qR262E4ryUe8PczMUGzxZOQPTOoGWYImrg0_qEDLub5hlB4y2ICrtcGdiGU=',
            'DATE': '1790133296973',
            'cmci9xde': 'U2FsdGVkX1+7+J+NNNmktKgbFp08uWM9EtmEuy8+uaWrNURCEF+CoZv+U8N0yF2DlbWZlue0ouYYktvj0yN8OQ==',
            'pmck9xge': 'U2FsdGVkX1/IqKSwOOQesZwOWNkn0SmJMU6uVERGaKo=',
            'assva6': 'U2FsdGVkX19VlXP6wnwYySMcKf1j5304lJLX8OiPvfU=',
            'assva5': 'U2FsdGVkX19qWZB3sKMbcYp/xztPz3Yvw7KEigEK5lwWzDlAGnLxNPufBnlZOM+jeieFgX+liqvxuQveQt59yw==',
            'crystal': 'U2FsdGVkX1/UAeB5z5kpmRVNWxDAdcBb1taSLSxX3AS2XoyfsK13OzsRzv4iRf/4NPgF6YmLvKSEu8hKdNgbHRXI1cI5VjXxJ5bPjQkNwU4CaV0xEO2EFRfVH0ATJuf4qkgCTW146i0Ayxm4erIVSa5FXhPPNG2U3nCj+soYbRe/tCu2rR5jRTrBbrV8clPa3PtwRpib8Gs6YTgx93pfFuefVVIvBPLFm33lH4N4Z5mAUANSWw28g6p787xAWnaI',
            'vmce9xdq': 'U2FsdGVkX1+9CbunwIDtvIGm5kPyH9NMmZ4GXbCehm35r4u9QXJcz0/iXNvcSHXgNm8ciEFUpihQoGbRFnVjgt+mZgUlItvSHOg3MoDuCqj5659MXB9SgNLl/87ZtXEOwepPP2yRBqilHjYCftmx3x1FX9HYQ5vOwotaTEj+FXQ=',
            'captcha_session_v2': '2|1:0|10:1790133297|18:captcha_session_v2|88:TFh6eDBPcEoreXoxbGRwYkEzb0FaaXVmVGNLV2pjczhrNzV0azZjQzB1bkNkRk1Qby9za2tXMVBSWVYrQ3AwcQ==|df21304efd43822a46dbf646141fc4af8434dbfce4b42aba088742e73fe4d03c',
            'captcha_ticket_v2': '2|1:0|10:1790133311|17:captcha_ticket_v2|728:eyJ2YWxpZGF0ZSI6IkNOMzFfS3hnZ0ZwTWNERkdwdzVsbmV4dGM2QldxVmY1eXhjamp6RkhOLmwzYzFZc3lxOS5PWjJFaXozNV9DckpjWnFrYk1JSnVIUl93YXdKZCpGWk1XZlR0WDBfY29sTlluQWtzdWdSZzlWWktEM2NLanpvQUx1dVkxS2RVQXAyWmJ6VlVrQWpFYXFKUTVPYTEyRXRodzNhQzlpUEVhVC5VZlBoTUk5R2VydlhqKk9NVWdmcnFMUGUxcip4ZHhEX1BQMTlCM1NoWThVY2dFU1dLWGFwenlnaDBiX2pQQ1Bmb3VTNWkza2JzOVpkUjI5UEF2VWxCVWJTUzZJSGM5ODFkR1VMdU9FNDFhRDhxRWNaWW5PV0c4SWJQamU0Qi5ReXEqV2RiTm95U2N6UkplVzAzc1V3NmhWOFFzRjYuZEdPZm5xZ1ZYWnV4dFJkUDV0dlYyayouR05wX2Z2Y056b296dzNnUUZ1RWFiUFZnZHAxQTR1b3VFTlBudjUqQWpyQ3ViYW5zSVRNTEdOT3owbVlNNkltdWFVM0MzYVUuQ2hKQSpiVFA1bTFpeFpHeVdEajIyWk45ODBXU1cxQkkyTlRGQUZHcUxKclJVdE9meXZuSFRCWUtkYnAuYXRCYXB5YmFFd0pVWUZudXVsSnUybU5WX3pMX2pxZGs4ZVltaENNR0gwOSozeElub2c3N192X2lfMSJ9|11698cbfc589b9e53b5886505edab2c2b0e39de37b308228eba24a2c2ba851d1',
            'z_c0': '2|1:0|10:1790133312|4:z_c0|92:Mi4xcm5OZERnQUFBQUJrcGRtY1BpVHpIQ1lBQUFCZ0FsVk5RSktnYXdBUEVrT3RZd211X0Vmei1uMTdaY0k2Wm84djZn|a32baba7223c146b4db58e43d8b28a27d77ca0f35f0e2a3dfe5b27e9f5debf98',
            'q_c1': '81a58d0750ab4ab09743592acee39fda|1790133312000|1790133312000',
            'Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49': '1790133995',
            'BEC': 'b7b0f394f3fd074c6bdd2ebbdd598b4e',
        }
        self.headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://www.zhihu.com/search?type=content&q=%E5%AD%A6%E4%B9%A0python',
            'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
            'x-api-version': '3.0.91',
            'x-app-za': 'OS=Web',
            'x-requested-with': 'fetch',
            'x-zse-93': '101_3_3.0',
            # 'x-zse-96': '2.0_z8AArbUHv6rBYZKht+FGyipgb5/3NSU3v4dS+LLXvnLl1q4fJ1Ze8AstvKL7wYk3',
            'x-zst-81': '3_2.0aR_sn77yn6O92wOB8hPZnQr0EMYxc4f18wNBUgpTQ6nxERFZY_Y0-4Lm-h3_tufIwJS8gcxTgJS_AuPZNcXCTwxI78YxEM20s4PGDwN8gGcYAupMWufIeQuK7AFpS6O1vukyQ_R0rRnsyukMGvxBEqeCiRnxEL2ZZrxmDucmqhPXnXFMTAoTF6RhRuLPF4LO2hX1_qC88rX_VhSqbqtLuvXOg92VqgS9DqS8obx0yBwV6USfQUFMqucTv0Nx2HtG69VObuSqqCSVawcfx9F_bQof6HNYBhXqzGwLkQUOOUgBBg2Yih2MUho0FgesWvCCTGNGIgwfUwcpk_em7UO_iJU_3Dxs3we0PbOL6vN_CCH9CqfzqCe067N_eUcu1GtfZCSBLCNCSXX1AJLygbLOzDrYVCeLZwSClGY860wKk_pxTqtC-Ce1QA3MaqpBFBH8BDH0tvNOiugVAhHMXrN1XugLAhwBQTHCwwYC',
            # 'cookie': '_xsrf=SkQ5Wm5T9yn9WuaWnDgVur3x8oE2wJm0; _zap=ed472ca3-a436-44f8-b928-b0243a52e3d9; d_c0=kTZYSIOEehyPTgabXUr8v3Spbabw5u_AlPg=|1782038356; __snaker__id=m7v8wlqMLPwIJ898; __zse_ck=005_fllEZKBE6ZHagnGdFWhrGh21soSQGPfBZOGZFtImIh5rl9CLuDLsqy6lfCwg9SNQZoFuysK7uwQ2PqXR3yQKjJ/WN3XWo38BafhAgv8lxIz5r7V3uJTa/0Quaz/hfhd6-y4LH/U3i6mUuj9lfGvSw19XOZq/IHCN25vi6MSwVeukIWdCSWpNOzqnOvHSl+8pyxtqS9xyIfhS0m7Hi8Bt8RJRAGDRkvsqQ7xjITnDXDP51IW2mHMLh/5IPFXMj16Qz; BEC=9de1a923fbc880d97a5571e917aeb532; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1786529251; HMACCOUNT=808752F02F03EC57; DATE=1782036111138; cmci9xde=U2FsdGVkX1+4ePE8nAoS/dp2/JWpbM6eZIv1AX6G5tRTSwAZ+J/qtTXFdWYVScmgeUIjOzGyFtfxAgdAggjaxg==; pmck9xge=U2FsdGVkX19xH9QyXdxXc4kcbJ0S4y7XCdz/UL+mOqo=; crystal=U2FsdGVkX19H7hyAyZxxKj4xUQUv3koFltm4YOGWYpwEep2S2U5tzFqi1x6wqQlgNGJlpj14ZgRB8D57CmQD81SaQ2b7pqiuFF+rCJbJj/zIp7l+7qhGeshzlulKfNZHfqAiVBteqr/v2lsKIiPEjDaRKJzyuBOeiYsS5Pqqv53AXmrjr8iMs/3dIJd/9QIwqGzVk//wSnnAGFFwbTeC2XXhokJKVNm1GK4Aslwh9AF+0+Ucr5HcO4YiMisKfTiD; assva6=U2FsdGVkX1/R8XtDQ9DMldxnnysFvDIRky6M3KhNGH0=; assva5=U2FsdGVkX1/ECI8CWO7po7QsYvZpmhk6fq+LieUcFG5KH40liw7bpb10L8FxFzjKkfOl3BQBLgn/UZgbstm5qw==; SESSIONID=GTtA3nyCKJcjYLToq6V8KjPsRKuMnFBJxOBAnSRgVdL; JOID=VF4RCkJWkRjOj17vAlZOgpUG1ZocEcdhj7MwlEwS23mp1h27b7DbaauAXOAPZ9e5J1FH7VeegOGD6ZKWsxR40Uk=; osd=UlEUBExQnh3AgVjgB1hAhJoD25QaHsJvgbU_kUIc3Xas2BO9YLXVZ62PWe4BYdi8KV9B4lKQjueM7JyYtRt930c=; vmce9xdq=U2FsdGVkX18+K3WIaN6lE8qgCVgrQRpwYQtCuXI13ckeG83GOXCevmTdUmtCQLYnDi3JnoaUFLJL6KoiPQC/6lKegzeLO2C7DOo0PbLZNVI/8246X/dVgN//BdVg6ua3k3YUe5XU2rNJr6wt9LWgRYZTcXiUG6zvlChe4SXERQw=; gdxidpyhxdE=QfUDqv%5Caemw14IZNoT1GULCIUoaXCRxi2ZfjKXLOM7M8DTbVHXTS7YZw8oZDaTL%2F%5CnQ3Nnzi8n4AwnjwinwgJvKO%2F1UMj2au%2BHD1su%2F8ZE5hHx8Q9ILwrOHEMnzrT4tCU51YsiK54eWJl0ON19ZGoSn8ogr5%2FjS%2FbILz%5C05EQATCeG1B%3A1786530152452; captcha_session_v2=2|1:0|10:1786529277|18:captcha_session_v2|88:eGdFM1hiOGl6RCtWOVBReVU0MGs1Y0E5bGE4ZkpJc052V29mWHBFSkpaZmhaWGt3NEhiMmtpeEJqc1dXSU51aQ==|2541d3ee9c2da23442e8e074ad39e3825e032839a207327583f5864b97fd8c56; captcha_ticket_v2=2|1:0|10:1786529299|17:captcha_ticket_v2|728:eyJ2YWxpZGF0ZSI6IkNOMzFfeWtBLkRCLk9kNmtac3F0T2dTNFFzS0VQRVIzWWxjTkVNZG5HOG9mMW8qS01GMk1RQkVjdUY0MEZ3WGsyaVJLYjhTSjBkRCpOQ1JWZGNZTTY1aDM4QnJidUdrOXNUSUJJa0hHbmhOSlhaLlJRRExOdTR5ODFmaVNNUFA1bDZPeGNtQ1pWT3Zqdjh6SVkqSjByRGEuYksqNUdaMTREaWNlNC5jemN3dHl4TnYqUjlzUkViNVhaQkJ2bmw1clFzNnpiekE4cmg4Mmp3cHptblF6MEFxSHNSZ0F4SzVjdGd0RHFyR2hLUU5XLk54b0YzRkdsR2M1ZzMueHdLekFvTFNVQnBiczJnKjBnYk82cUxHZkJqUXRFeE1pdlB4am1jcio0KmF6OGxqZUoweDNPKlB6V1QzcXBNOUNwOWR5UzNXS0RvMDMzSTRPNWdpQTRXT1ZkQSpzRVpuT3dLUTM1NWtPd3J6aEw1T1B6WklucWVkeE9VcTVQdlM2SGFiQkRyeTNQREhqTmN6bU91T3ZlZjB1UUJqQWpJS3ZRcHRXbHpoX2VQazBhOFZiMHNtKnVFVWxGWmdBNWpBaTUuQk1DV3RnSGtOQ0VFREVEZ0NPdGVWOEFTbWRRX18wTkp6dlhrZ0ZWTGVGZTNBajgwQ2pTZ052aWxGbW9raWZIVXJFU0J0UENpMHlYT003N192X2lfMSJ9|0787abcd34d0da3688f485a391210bb4de1a9fe4afad9210862fd25fec6ca78f; z_c0=2|1:0|10:1786529317|4:z_c0|92:Mi4xcm5OZERnQUFBQUNSTmxoSWc0UjZIQ1lBQUFCZ0FsVk5KWlJwYXdCeUhNcFhsTG9malZFUklJRmxhZm5tdDFJOUJB|c706ad3dc18ba63fd10156546636d02d9b0c8194b08e348738bc61d930d89158; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1786529318',
        }
        self.eo = {
            "zse93": "101_3_3.0",
            "dc0": "kTZYSIOEehyPTgabXUr8v3Spbabw5u_AlPg=|1782038356",
            "xZst81": "3_2.0aR_sn77yn6O92wOB8hPZnQr0EMYxc4f18wNBUgpTQ6nxERFZY_Y0-4Lm-h3_tufIwJS8gcxTgJS_AuPZNcXCTwxI78YxEM20s4PGDwN8gGcYAupMWufIeQuK7AFpS6O1vukyQ_R0rRnsyukMGvxBEqeCiRnxEL2ZZrxmDucmqhPXnXFMTAoTF6RhRuLPF4LO2hX1_qC88rX_VhSqbqtLuvXOg92VqgS9DqS8obx0yBwV6USfQUFMqucTv0Nx2HtG69VObuSqqCSVawcfx9F_bQof6HNYBhXqzGwLkQUOOUgBBg2Yih2MUho0FgesWvCCTGNGIgwfUwcpk_em7UO_iJU_3Dxs3we0PbOL6vN_CCH9CqfzqCe067N_eUcu1GtfZCSBLCNCSXX1AJLygbLOzDrYVCeLZwSClGY860wKk_pxTqtC-Ce1QA3MaqpBFBH8BDH0tvNOiugVAhHMXrN1XugLAhwBQTHCwwYC"
        }

    def md5_val(self):
        obj = md5()
        # 向加密对象添加内容
        add_data = self.eo["zse93"] + '+api/v4/search_v3?' + urlencode(self.params) + self.eo["dc0"]
        # print(add_data)
        obj.update(add_data.encode(encoding='utf-8'))
        md5_res = obj.hexdigest()
        return md5_res

    def encrypt_data(self):
        js = execjs.compile(open('./loader.js', 'r', encoding='utf-8').read())
        # print(js)
        encryptData = js.call('params', self.er, str(self.md5_val()), self.eo)
        x_zse_96_value = '2.0_' + encryptData.get('signature', '')
        return x_zse_96_value

    def parse_data(self):
        # 向请求头中添加x-zse-96参数值
        self.headers["x-zse-96"] = self.encrypt_data()
        response_data = requests.get(self.url, params=self.params, cookies=self.cookies, headers=self.headers)
        return response_data.json()


if __name__ == '__main__':
    data = CrawlData()
    pprint.pprint(data.parse_data())
