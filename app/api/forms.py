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

    subject = StringField('Subject', validators=[
        validators.AnyOf(list(const.SUBJECT.keys()), '学科不正确')])
    grade = StringField('Subject', validators=[
        validators.AnyOf(list(const.GRADE.keys()), '年级不正确')])
    name = StringField('Name', validators=[
        validators.DataRequired('请输入试卷名称')])
    exam_date = DateField('ExamDate', validators=[
        validators.DataRequired('请选择考试时间')])


