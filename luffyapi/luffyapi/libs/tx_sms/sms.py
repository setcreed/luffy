import random
# 随机获取六位数字验证码
def get_sms_code():
    code = ''
    for i in range(6):
        code += str(random.randint(0, 9))
    return code

from .settings import APP_ID, APP_KEY, TEMPLATE_ID, SMS_SIGN
from qcloudsms_py import SmsSingleSender
sender = SmsSingleSender(APP_ID, APP_KEY)

from utils.logging import logger
def send_sms(mobile, code, exp):
    try:
        response = sender.send_with_param(86, mobile, TEMPLATE_ID, (code, exp), sign=SMS_SIGN, extend="", ext="")
        if response and response.get('result') == 0:
            return True  # 成功
        logger.error('短信发送失败，状态码：%s, 错误信息：%s' % (response.get('result'), response.get('errmsg')))
    except Exception as e:
        logger.error('短信发送异常，异常信息为：%s' % e)
    return False