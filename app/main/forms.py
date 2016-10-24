from flask.ext.wtf import Form
from wtforms import StringField,PasswordField,BooleanField,SubmitField, IntegerField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(Form):
    user_name = StringField('用户名',validators=[Required('请输入用户名'), Length(1,64)])
    password = PasswordField('密码',validators=[Required('请输入密码')])
    remember_me = BooleanField('保持登录')
    submit = SubmitField('登录')

class RegisterForm(Form):
    phone = StringField('Phone', validators=[Required('请输入手机号'),
        Length(11, 11, '手机号不正确')])
    valid_code = StringField('ValidCode', validators=[Required('请输入验证码')])
    visit_code = StringField('VisitCode', validators=[Required('请输入邀请码')])

class RegisterInfoForm(Form):
    phone = StringField('Phone', validators=[Required('请输入手机号'),
        Length(11, 11, '手机号不正确')])
    user_name = StringField('用户名',validators=[Required('请输入用户名'), Length(1,64)])
    password = PasswordField('密码',validators=[Required('请输入密码')])
    repassword = PasswordField('密码',validators=[Required('请输入密码'), EqualTo('password', '两次输入密码不一致')])
    email = StringField('邮箱', validators=[Required('请输入邮箱'),
                                             Email("邮箱格式不正确")])
    province_id = IntegerField('省', validators=[Required('请选择省')])
    city_id = IntegerField('市', validators=[Required('请选择市')])
    area_id = IntegerField('县/区', validators=[Required('请选择县/区')])
    school_id = IntegerField('学校', validators=[Required('请选择学校')])
    grade_id = IntegerField('年级', validators=[Required('请选择年级')])

class PasswordResetRequestForm(Form):
    email = StringField('邮箱', validators=[Required(), Length(1, 64),
                                             Email()])
    submit = SubmitField('提交')

class PasswordResetForm(Form):
    email = StringField('邮箱', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField('新密码', validators=[
        Required(), EqualTo('password2', message='确认新密码不一致')])
    password2 = PasswordField('确认新密码', validators=[Required()])
    submit = SubmitField('重置密码')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('未发现使用该邮箱的帐号')

