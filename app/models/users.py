from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date

from sqlalchemy import text
from flask.ext.login import UserMixin, AnonymousUserMixin
from app import db, login_manager
from app.models.permissions import Permission
from ._base import SessionMixin
from app.models.regions import Region
from app.models.schools import School

class User(db.Model, SessionMixin, UserMixin):
    __tablename__ = 'user'
    protected_field = ['password','password_hash', 'last_login_ip', 'code']
    search_fields = ['name_like',
        'phone_like', 'state', 'created_at_begin',
        'created_at_end', 'school_id', 'grade_id',
        'city_id', 'province_id', 'area_id',
        'permissions_like']

    def __init__(self, *args, **kwargs):
        User.register()
        super(User, self).__init__(*args, **kwargs)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    school_id = db.Column(db.Integer)
    grade_id = db.Column(db.Integer)
    city_id = db.Column(db.Integer)
    province_id = db.Column(db.Integer)
    area_id = db.Column(db.Integer)
    user_type = db.Column(db.Integer)
    last_login_ip = db.Column(db.String(64))
    state = db.Column(db.Integer, default=0)
    phone = db.Column(db.String(16))
    code = db.Column(db.String(12))
    permissions = db.Column(db.JsonBlob(), default=[])
    openid = db.Column(db.String(400))
    scores = db.relationship('Score', backref='user',
                                lazy='dynamic')
    messages = db.relationship('Message', backref='user',
                                lazy='dynamic')

    @property
    def password(self):
        return AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def get_menus(self):
        permissions = self.permissions
        menus = []
        for p in permissions:
            menus += Permission.__dict__.get(p, [])
        return [{'identity': m} for m in menus]

    def to_dict(self):
        res = super(User, self).to_dict()
        res = Region.bind_auto(res, 'name', 'province_id', 'id', 'province')
        res = Region.bind_auto(res, 'name', 'city_id', 'id', 'city')
        res = Region.bind_auto(res, 'name', 'area_id', 'id', 'area')
        res = School.bind_auto(res, 'name', 'school_id', 'id', 'school')
        return res

    def get_admin_summary(self, begin_time=None, end_time=None):
        res = []
        if 'UPLOAD_PERMISSION' in self.permissions:
            data = self.get_upload_sumary(begin_time, end_time)
            res.append(data)
        if 'CONFIRM_PERMISSION' in self.permissions:
            data = self.get_confirm_sumary(begin_time, end_time)
            res.append(data)
        if 'DEAL_PERMISSION' in self.permissions:
            data = self.get_deal_sumary(begin_time, end_time)
            res.append(data)
        if 'INPUT_PERMISSION' in self.permissions:
            data = self.get_input_sumary(begin_time, end_time)
            res.append(data)
        if 'ANSWER_PERMISSION' in self.permissions:
            data = self.get_anwer_sumary(begin_time, end_time)
            res.append(data)
        if 'CHECK_PERMISSION' in self.permissions:
            data = self.get_check_sumary(begin_time, end_time)
            res.append(data)
        if 'JUDGE_PERMISSION' in self.permissions:
            data = self.get_judge_sumary(begin_time, end_time)
            res.append(data)
        if 'VERIFY_PERMISSION' in self.permissions:
            data = self.get_verify_sumary(begin_time, end_time)
            res.append(data)
        return res


    def get_upload_sumary(self, begin_time, end_time):
        sql = '''select
                    convert(sum(case when state=0 then 1 else 0 end), char(20)) as ready,
                    convert(sum(case when state=1 then 1 else 0 end), char(20)) as confirming,
                    convert(sum(case when state=5 then 1 else 0 end), char(20)) as pass,
                    convert(sum(case when state>=2 and state <=4 then 1 else 0 end), char(20)) as useage
                from `exam`
                where upload_user={}'''.format(self.id)
        if begin_time:
            sql = sql + ' and created_at >= "{}"'.format(begin_time)
        if end_time:
            sql = sql + ' and created_at <= "{}"'.format(end_time)
        sql = text(sql)
        res = db.engine.execute(sql)
        res = res.fetchone()
        data = {
            'title': '试卷上传',
            'ready': res[0] or '0',
            'confirming': res[1] or '0',
            'pass': res[2] or '0',
            'useage': res[3] or '0'
        }      
        return data

    def get_confirm_sumary(self, begin_time, end_time):
        sql = '''select
                    convert(sum(case when review_state=-1 then 1 else 0 end), char(20)) as reject,
                    convert(sum(case when review_state=1 then 1 else 0 end), char(20)) as confirming,
                    convert(sum(case when review_state=5 then 1 else 0 end), char(20)) as pass,
                    convert(sum(case when review_state=2 then 1 else 0 end), char(20)) as useage
                from `review`
                where reviewer_id={}'''.format(self.id)
        if begin_time:
            sql = sql + ' and created_at >= "{}"'.format(begin_time)
        if end_time:
            sql = sql + ' and created_at <= "{}"'.format(end_time)
        sql = text(sql)
        res = db.engine.execute(sql)
        res = res.fetchone()
        data = {
            'title': '审核',
            'reject': res[0] or '0',
            'confirming': res[1] or '0',
            'pass': res[2] or '0',
            'useage': res[3] or '0'
        }      
        return data

    def get_deal_sumary(self, begin_time, end_time):
        sql = '''select
                    convert(sum(case when state=3 then 1 else 0 end), char(20)) as dealing,
                    convert(sum(case when state=4 then 1 else 0 end), char(20)) as complete
                from `pre_process`
                where operator_id={}'''.format(self.id)
        if begin_time:
            sql = sql + ' and created_at >= "{}"'.format(begin_time)
        if end_time:
            sql = sql + ' and created_at <= "{}"'.format(end_time)
        sql = text(sql)
        res = db.engine.execute(sql)
        res = res.fetchone()
        data = {
            'title': '预处理',
            'dealing': res[0] or '0',
            'complete': res[1] or '0'
        }
        return data

    def get_input_sumary(self, begin_time, end_time):
        sql = '''select
                    convert(sum(case when state=1 then 1 else 0 end), char(20)) as typing,
                    convert(sum(case when state=3 then 1 else 0 end), char(20)) as complete,
                    convert(sum(case when state=5 then 1 else 0 end), char(20)) as complete_answer,
                    convert(sum(case when state=99 then 1 else 0 end), char(20)) as finish
                from `quest_typing`
                where operator_id={}'''.format(self.id)
        if begin_time:
            sql = sql + ' and created_at >= "{}"'.format(begin_time)
        if end_time:
            sql = sql + ' and created_at <= "{}"'.format(end_time)
        sql = text(sql)
        res = db.engine.execute(sql)
        res = res.fetchone()
        data = {
            'title': '录题',
            'typing': res[0] or '0',
            'complete': res[1] or '0',
            'complete_answer': res[2] or '0',
            'finish': res[3] or '0'
        }
        return data

    def get_anwer_sumary(self, begin_time, end_time):
        sql = '''select
                    convert(sum(case when state=4 then 1 else 0 end), char(20)) as answering,
                    convert(sum(case when state=5 then 1 else 0 end), char(20)) as complete_answer
                from `quest_answer`
                where operator_id={}'''.format(self.id)
        if begin_time:
            sql = sql + ' and created_at >= "{}"'.format(begin_time)
        if end_time:
            sql = sql + ' and created_at <= "{}"'.format(end_time)
        sql = text(sql)
        res = db.engine.execute(sql)
        res = res.fetchone()
        data = {
            'title': '解答',
            'answering': res[0] or '0',
            'complete_answer': res[1] or '0'
        }
        return data

    def get_check_sumary(self, begin_time, end_time):
        sql = '''select
                    convert(sum(case when state=6 then 1 else 0 end), char(20)) as checking,
                    convert(sum(case when state=7 or state=9 then 1 else 0 end), char(20)) as complete
                from `quest_check`
                where operator_id={}'''.format(self.id)
        if begin_time:
            sql = sql + ' and created_at >= "{}"'.format(begin_time)
        if end_time:
            sql = sql + ' and created_at <= "{}"'.format(end_time)
        sql = text(sql)
        res = db.engine.execute(sql)
        res = res.fetchone()
        data = {
            'title': '检查',
            'checking': res[0] or '0',
            'complete': res[1] or '0'
        }
        return data

    def get_judge_sumary(self, begin_time, end_time):
        sql = '''select
                    convert(sum(case when state=8 then 1 else 0 end), char(20)) as judging,
                    convert(sum(case when state=9 then 1 else 0 end), char(20)) as complete
                from `quest_judge`
                where operator_id={}'''.format(self.id)
        if begin_time:
            sql = sql + ' and created_at >= "{}"'.format(begin_time)
        if end_time:
            sql = sql + ' and created_at <= "{}"'.format(end_time)
        sql = text(sql)
        res = db.engine.execute(sql)
        res = res.fetchone()
        data = {
            'title': '裁定',
            'judging': res[0] or '0',
            'complete': res[1] or '0'
        }
        return data

    def get_verify_sumary(self, begin_time, end_time):
        sql = '''select
                    convert(sum(case when state=10 then 1 else 0 end), char(20)) as verifying,
                    convert(sum(case when state=99 then 1 else 0 end), char(20)) as complete
                from `quest_verify`
                where operator_id={}'''.format(self.id)
        if begin_time:
            sql = sql + ' and created_at >= "{}"'.format(begin_time)
        if end_time:
            sql = sql + ' and created_at <= "{}"'.format(end_time)
        sql = text(sql)
        res = db.engine.execute(sql)
        res = res.fetchone()
        data = {
            'title': '校对',
            'verifying': res[0] or '0',
            'complete': res[1] or '0'
        }
        return data


    def get_statistic(self, begin_time, end_time, time_type, statistic_type, status):
        if statistic_type == 'UPLOAD_PERMISSION':
            return self.get_upload_statistic(begin_time, end_time, time_type, status)
        if statistic_type == 'CONFIRM_PERMISSION':
            return self.get_confirm_statistic(begin_time, end_time, time_type, status)
        if statistic_type == 'DEAL_PERMISSION':
            return self.get_deal_statistic(begin_time, end_time, time_type, status)
        if statistic_type == 'INPUT_PERMISSION':
            return self.get_input_statistic(begin_time, end_time, time_type, status)
        if statistic_type == 'ANSWER_PERMISSION':
            return self.get_anwer_statistic(begin_time, end_time, time_type, status)
        if statistic_type == 'CHECK_PERMISSION':
            return self.get_check_statistic(begin_time, end_time, time_type, status)
        if statistic_type == 'JUDGE_PERMISSION':
            return self.get_judge_statistic(begin_time, end_time, time_type, status)
        if statistic_type == 'VERIFY_PERMISSION':
            return self.get_verify_statistic(begin_time, end_time, time_type, status)
        
    def get_upload_statistic(self, begin_time, end_time, time_type, status):
        if time_type == 'HOUR':
            time = 'HOUR(created_at)'
        elif time_type == 'MONTH':
            time = 'MONTH(created_at)'
        else:
            time = 'date(created_at)'
        sql = '''select count(*) as count, {} as time from exam where upload_user={} '''.format(time, self.id)
        if status == 'ready':
            sql = sql + ' and state=0'
        elif status == 'confirming':
            sql = sql + ' and state=1'
        elif status == 'pass':
            sql = sql + ' and state=5'
        elif status == 'useage':
            sql = sql + ' and state>=2 and state <=4'
        if begin_time:
            sql = sql + ' and created_at >= "{}"'.format(begin_time)
        if end_time:
            sql = sql + ' and created_at <= "{}"'.format(end_time)
        sql = sql + ' group by {}'.format(time)
        sql = text(sql)
        res = db.engine.execute(sql)
        res = res.fetchall()
        res = [{'count': d[0], 'time': d[1].strftime('%Y-%m-%d') if isinstance(d[1], date) else d[1]} for d in res]
        return res
    
    def get_confirm_statistic(self, begin_time, end_time, time_type, status):
        if time_type == 'HOUR':
            time = 'HOUR(created_at)'
        elif time_type == 'MONTH':
            time = 'MONTH(created_at)'
        else:
            time = 'date(created_at)'
        sql = '''select count(*) as count, {} as time from review where reviewer_id={} '''.format(time, self.id)
        if status == 'reject':
            sql = sql + ' and review_state=-1'
        elif status == 'confirming':
            sql = sql + ' and review_state=1'
        elif status == 'pass':
            sql = sql + ' and review_state=5'
        elif status == 'usage':
            sql = sql + ' and review_state=2'
        if begin_time:
            sql = sql + ' and created_at >= "{}"'.format(begin_time)
        if end_time:
            sql = sql + ' and created_at <= "{}"'.format(end_time)
        sql = sql + ' group by {}'.format(time)
        sql = text(sql)
        res = db.engine.execute(sql)
        res = res.fetchall()
        res = [{'count': d[0], 'time': d[1].strftime('%Y-%m-%d') if isinstance(d[1], date) else d[1]} for d in res]
        return res

    def get_deal_statistic(self, begin_time, end_time, time_type, status):
        if time_type == 'HOUR':
            time = 'HOUR(created_at)'
        elif time_type == 'MONTH':
            time = 'MONTH(created_at)'
        else:
            time = 'date(created_at)'
        sql = '''select count(*) as count, {} as time from pre_process where operator_id={} '''.format(time, self.id)
        if status == 'dealing':
            sql = sql + ' and state=3'
        elif status == 'complete':
            sql = sql + ' and state=4'
        if begin_time:
            sql = sql + ' and created_at >= "{}"'.format(begin_time)
        if end_time:
            sql = sql + ' and created_at <= "{}"'.format(end_time)
        sql = sql + ' group by {}'.format(time)
        sql = text(sql)
        res = db.engine.execute(sql)
        res = res.fetchall()
        res = [{'count': d[0], 'time': d[1].strftime('%Y-%m-%d') if isinstance(d[1], date) else d[1]} for d in res]
        return res

    def get_input_statistic(self, begin_time, end_time, time_type, status):
        if time_type == 'HOUR':
            time = 'HOUR(created_at)'
        elif time_type == 'MONTH':
            time = 'MONTH(created_at)'
        else:
            time = 'date(created_at)'
        sql = '''select count(*) as count, {} as time from quest_typing where operator_id={} '''.format(time, self.id)
        if status == 'complete':
            sql = sql + ' and state=3'
        elif status == 'complete_answer':
            sql = sql + ' and state=4'
        elif status == 'finish':
            sql = sql + ' and state=4'
        elif status == 'typing':
            sql = sql + ' and state=4'
        if begin_time:
            sql = sql + ' and created_at >= "{}"'.format(begin_time)
        if end_time:
            sql = sql + ' and created_at <= "{}"'.format(end_time)
        sql = sql + ' group by {}'.format(time)
        sql = text(sql)
        res = db.engine.execute(sql)
        res = res.fetchall()
        res = [{'count': d[0], 'time': d[1].strftime('%Y-%m-%d') if isinstance(d[1], date) else d[1]} for d in res]
        return res

    def get_anwer_statistic(self, begin_time, end_time, time_type, status):
        if time_type == 'HOUR':
            time = 'HOUR(created_at)'
        elif time_type == 'MONTH':
            time = 'MONTH(created_at)'
        else:
            time = 'date(created_at)'
        sql = '''select count(*) as count, {} as time from quest_answer where operator_id={} '''.format(time, self.id)
        if status == 'answering':
            sql = sql + ' and state=4'
        elif status == 'complete_answer':
            sql = sql + ' and state=5'
        if begin_time:
            sql = sql + ' and created_at >= "{}"'.format(begin_time)
        if end_time:
            sql = sql + ' and created_at <= "{}"'.format(end_time)
        sql = sql + ' group by {}'.format(time)
        sql = text(sql)
        res = db.engine.execute(sql)
        res = res.fetchall()
        res = [{'count': d[0], 'time': d[1].strftime('%Y-%m-%d') if isinstance(d[1], date) else d[1]} for d in res]
        return res

    def get_check_statistic(self, begin_time, end_time, time_type, status):
        if time_type == 'HOUR':
            time = 'HOUR(created_at)'
        elif time_type == 'MONTH':
            time = 'MONTH(created_at)'
        else:
            time = 'date(created_at)'
        sql = '''select count(*) as count, {} as time from quest_check where operator_id={} '''.format(time, self.id)
        if status == 'checking':
            sql = sql + ' and state=6'
        elif status == 'complete':
            sql = sql + ' and state=7'
        if begin_time:
            sql = sql + ' and created_at >= "{}"'.format(begin_time)
        if end_time:
            sql = sql + ' and created_at <= "{}"'.format(end_time)
        sql = sql + ' group by {}'.format(time)
        sql = text(sql)
        res = db.engine.execute(sql)
        res = res.fetchall()
        res = [{'count': d[0], 'time': d[1].strftime('%Y-%m-%d') if isinstance(d[1], date) else d[1]} for d in res]
        return res

    def get_judge_statistic(self, begin_time, end_time, time_type, status):
        if time_type == 'HOUR':
            time = 'HOUR(created_at)'
        elif time_type == 'MONTH':
            time = 'MONTH(created_at)'
        else:
            time = 'date(created_at)'
        sql = '''select count(*) as count, {} as time from quest_judge where operator_id={} '''.format(time, self.id)
        if status == 'judging':
            sql = sql + ' and state=8'
        elif status == 'complete':
            sql = sql + ' and state=9'
        if begin_time:
            sql = sql + ' and created_at >= "{}"'.format(begin_time)
        if end_time:
            sql = sql + ' and created_at <= "{}"'.format(end_time)
        sql = sql + ' group by {}'.format(time)
        sql = text(sql)
        res = db.engine.execute(sql)
        res = res.fetchall()
        res = [{'count': d[0], 'time': d[1].strftime('%Y-%m-%d') if isinstance(d[1], date) else d[1]} for d in res]
        return res

    def get_verify_statistic(self, begin_time, end_time, time_type, status):
        if time_type == 'HOUR':
            time = 'HOUR(created_at)'
        elif time_type == 'MONTH':
            time = 'MONTH(created_at)'
        else:
            time = 'date(created_at)'
        sql = '''select count(*) as count, {} as time from quest_verify where operator_id={} '''.format(time, self.id)
        if status == 'verifying':
            sql = sql + ' and state=10'
        elif status == 'complete':
            sql = sql + ' and state=99'
        if begin_time:
            sql = sql + ' and created_at >= "{}"'.format(begin_time)
        if end_time:
            sql = sql + ' and created_at <= "{}"'.format(end_time)
        sql = sql + ' group by {}'.format(time)
        sql = text(sql)
        res = db.engine.execute(sql)
        res = res.fetchall()
        res = [{'count': d[0], 'time': d[1].strftime('%Y-%m-%d') if isinstance(d[1], date) else d[1]} for d in res]
        return res

    def __repr__(self):
        return '<User: %r>' % self.name

class AnonymousUser(AnonymousUserMixin):
    def is_admin(self):
        return False

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

login_manager.anonymous_user = AnonymousUser