import unittest
import yaml
from channels.enterprise_wechat_app import QYWXApp


class TestQYWXApp(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        # 全局变量
        TestQYWXApp.chatid = ''
        TestQYWXApp.media_id= ''

        # 配置信息获取，实例化QYWXAPP
        with open(".vscode/credentials.yml","r") as f:
            credentials=yaml.load(f.read(),Loader=yaml.Loader)
            qywx_config = credentials['channels.enterprise_wechat_channel.EnterpriseWechatChannel']
        self.app = QYWXApp(**qywx_config)

    def test_get_access_token(self):
        """测试获取access_token"""
        access_token = self.app._get_access_token()

        assert isinstance(access_token, str)
        assert len(access_token) != 0

    def test_requests_validate_expired(self):
        """测试当access_token过期时此函数能否正常的获取新token并再次发送请求"""
        expired_access_token = "HfetFsU8eFxbm20_p56ALkwtwj5261ej_FgjDSgPtNB6lpJS2Lbaw-dQ2L0lr_6FNRlhjb0M_06C2WfGvcO54n6diS5xikZfI1xcFIr9GYDr4IXXC_wgXrUZg7r39ryg4i69kdW_XwFRsfcgxkbB4vfckw9PORz1g9TrTRB34VOxMQcY7K7riHWNhiPrJfmUPAyWmSWbswnYCdBH5Y8p2w"
        get_group_url = self.app.APPCHAT_GET.format(expired_access_token, TestQYWXApp.chatid)
        request_params = {"method": "get", "url": get_group_url}
        res = self.app._requests_validate_expired(**request_params)
        assert res["errcode"] == 0

    def test_create_group(self):
        params = {
            "group_name": "创建群聊测试用例执行，即将删除",
            "group_owner": "WangBeiNing",
            "group_user_list": ["WangBeiNing", "601532214", "601429829"],
        }
        TestQYWXApp.chatid = self.app.create_group(**params)
        assert isinstance(TestQYWXApp.chatid, str)
        assert len(TestQYWXApp.chatid) != 0

    def test_update_group(self):
        params = {
            "chatid": TestQYWXApp.chatid,
            "del_user_list": ["601532214", "601429829"],
        }
        res = self.app.update_group(**params)
        assert res["errcode"] == 0

    def test_get_group(self):
        res = self.app.get_group(TestQYWXApp.chatid)
        assert res["errcode"] == 0

    def test_get_img_media_id(self):
        # 图床图片（图片类型在尾部）
        # img_url = "https://cdn.jsdelivr.net/gh/bainningking/pic_repo@main/img/opspilot.png"
        # DALL-E图片
        img_url = "https://oaidalleapiprodscus.blob.core.windows.net/private/org-x5cPubqlMOCWwX4scmcSvPU3/user-drxZ69DpevXcbdpwlc7xDpL8/img-mjpqVG4ojlbi8GidyXh1RMxu.png?st=2023-07-20T05%3A18%3A28Z&se=2023-07-20T07%3A18%3A28Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2023-07-19T20%3A04%3A40Z&ske=2023-07-20T20%3A04%3A40Z&sks=b&skv=2021-08-06&sig=QD/1eC1C5oS8V4um0y8DYuqWbuUHIWt/9l8x8F3aRs4%3D"
        TestQYWXApp.media_id = self.app._get_img_media_id(img_url)
        assert isinstance(TestQYWXApp.media_id, str)
        assert len(TestQYWXApp.media_id) != 0


    def test_post_msg(self):
        content = "这是OpsPilot内的测试用例所发出"
        # 企微应用向群聊发送文本消息
        res = self.app.post_msg(chatid=TestQYWXApp.chatid, content=content)
        assert res["errcode"] == 0
        # 企微应用向群聊发送图片消息
        res = self.app.post_msg(chatid=TestQYWXApp.chatid, msgtype="image", media_id=TestQYWXApp.media_id)
        assert res["errcode"] == 0
        # 企微应用向用户发送文本消息
        res = self.app.post_msg(user_id="WangBeiNing", content=content)
        assert res["errcode"] == 0
        # 企微应用向用户发送图片消息
        res = self.app.post_msg(user_id="WangBeiNing", msgtype='image', media_id=TestQYWXApp.media_id)
        assert res["errcode"] == 0

    def test_name_to_userid(self):
        # 将下面的人名换成企微内的，tips:可以通过群成员右边的三个点复制群成员名称
        name1 = "张三;李四;王五(wangwu);"
        name2 = "张三;"
        res = QYWXApp.name_to_userid(name1)
        assert len(res) != 0
        res = QYWXApp.name_to_userid(name2)
        assert len(res) != 0
if __name__ == "__main__":
    # 构造测试套件，按顺序执行测试用例
    suite = unittest.TestSuite()
    suite.addTest(TestQYWXApp("test_get_access_token"))
    suite.addTest(TestQYWXApp("test_create_group"))
    suite.addTest(TestQYWXApp("test_get_group"))
    suite.addTest(TestQYWXApp("test_requests_validate_expired"))
    suite.addTest(TestQYWXApp("test_get_img_media_id"))
    suite.addTest(TestQYWXApp("test_post_msg"))
    suite.addTest(TestQYWXApp("test_update_group"))
    suite.addTest(TestQYWXApp("test_name_to_userid"))

    # 运行测试套件
    runner = unittest.TextTestRunner()
    runner.run(suite)
