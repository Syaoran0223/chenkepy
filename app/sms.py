# -*- coding: utf-8 -*-

import random, json, time
from app.alidayu import AlibabaAliqinFcSmsNumSendRequest
from app import cache

class SmsServer(object):
    def __init__(self):
        self.appkey = '23481421'
        self.secret = 'dc696756fd6dc352331f2fa0eeecb1fb'
        self.url = 'https://eco.taobao.com/router/rest'
        
    def generate_code(self, phone):
        # 判断生成频率
        code_exit_key = "code_exit_{}".format(phone)
        if cache.get(code_exit_key):
            return False, ''
        code = random.randint(10000, 99999)
        valid_code_key = "code_{}".format(phone)
        # 设置到期时间10分钟
        cache.set(valid_code_key, code, timeout=600)
        # 设置频率 60秒后允许重新生成
        cache.set(code_exit_key, time.time(), 60)
        return True, code


    def send_code(self, code, phone, product="试卷收集系统"):
        req = AlibabaAliqinFcSmsNumSendRequest(self.appkey, self.secret, self.url)
        req.extend = ""
        req.sms_type = "normal"
        req.sms_free_sign_name = "注册验证"
        params = {
            'code': str(code),
            'product': product
        }
        req.sms_param = json.dumps(params)
        req.rec_num = phone
        req.sms_template_code = "SMS_13745472"
        resp = req.getResponse()
        if resp.get('error_response'):
            res = {
                'success': 'false',
                'code': resp.get('error_response', {}).get('code'),
                'msg': resp.get('error_response', {}).get('sub_msg', '')
            }
            return res
        result = resp.get('alibaba_aliqin_fc_sms_num_send_response', {}).get('result')
        return {
            'success': result.get('success', False),
            'code': result.get('err_code', 400),
            'msg': result.get('msg', '')
        }

    def check_code(self, code, phone):
        valid_code_key = "code_{}".format(phone)
        return cache.get(valid_code_key) == code
