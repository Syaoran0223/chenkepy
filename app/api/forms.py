from wtforms.form import Form
from wtforms import validators
from wtforms.validators import ValidationError
from wtforms.fields import StringField, IntegerField, DateField

from app import const

class SmsForm(Form):
    phone = StringField('Phone', validators=[validators.DataRequired(),
        validators.length(11, 11, '手机号不正确')])

class PaperUploadForm(Form):
    year = StringField('Year', validators=[
        validators.AnyOf(list(const.SCHOOL_YEAR.keys()), '年度不正确')])
    section = StringField('Section', validators=[
        validators.AnyOf(list(const.SECTION.keys()), '学期不正确')])
    paper_types = StringField('PaperType', validators=[
        validators.AnyOf(list(const.PAPER_TYPE.keys()), '试卷类型不正确')])
    school_id = IntegerField('SchoolId', validators=[
        validators.DataRequired('请选择学校')])
    province_id = IntegerField('ProvinceId',validators=[validators.DataRequired('请选择省份')])
    city_id = IntegerField('CityId', validators=[validators.DataRequired('请选择城市')])
    area_id = IntegerField('AreaId', validators=[validators.DataRequired('请选择地区')])

    subject = IntegerField('Subject',validators=[validators.DataRequired('学科不正确')])
    grade = StringField('Subject', validators=[
        validators.AnyOf(list(const.GRADE.keys()), '年级不正确')])
    name = StringField('Name', validators=[
        validators.DataRequired('请输入试卷名称')])
    exam_date = DateField('ExamDate', validators=[
        validators.DataRequired('请选择考试时间')])
    is_fast = IntegerField('IsFast')

class RegisterInfoForm(Form):
    phone = StringField('Phone', validators=[validators.DataRequired('请输入手机号'),
        validators.length(11, 11, '手机号不正确')])
    user_name = StringField('用户名',validators=[validators.DataRequired('请输入用户名'), validators.length(1,64)])
    password = StringField('密码',validators=[validators.DataRequired('请输入密码')])
    repassword = StringField('密码',validators=[validators.DataRequired('请输入密码'), validators.equal_to('password', '两次输入密码不一致')])
    email = StringField('邮箱', validators=[validators.DataRequired('请输入邮箱'),
                                             validators.email("邮箱格式不正确")])
    province_id = IntegerField('省', validators=[validators.DataRequired('请选择省')])
    city_id = IntegerField('市', validators=[validators.DataRequired('请选择市')])
    area_id = IntegerField('县/区', validators=[validators.DataRequired('请选择县/区')])
    school_id = IntegerField('学校', validators=[validators.DataRequired('请选择学校')])
    grade_id = IntegerField('年级', validators=[validators.DataRequired('请选择年级')])


