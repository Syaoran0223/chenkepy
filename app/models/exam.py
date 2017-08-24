from flask import g, current_app, request
from itertools import groupby
from sqlalchemy import distinct, func
from app import db
from ._base import SessionMixin
from app.utils import pagination
from app.models import School, Region
from app.const import EXAM_STATUS
import datetime
class Exam(db.Model, SessionMixin):
    __tablename__ = 'exam'

    def __init__(self, *args, **kwargs):
        Exam.register()
        super(Exam, self).__init__(*args, **kwargs)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    section = db.Column(db.String(12))
    subject = db.Column(db.String(5))
    paper_types = db.Column(db.String(17))
    province_id = db.Column(db.Integer)
    city_id = db.Column(db.Integer)
    area_id = db.Column(db.Integer)
    school_id = db.Column(db.Integer)
    year = db.Column(db.Integer)
    grade = db.Column(db.Integer)
    state = db.Column(db.Integer)
    upload_user = db.Column(db.Integer)
    struct = db.Column(db.JsonBlob(), default=[])
    has_struct = db.Column(db.Boolean, default=False)
    attachments = db.Column(db.JsonBlob(), default=[])
    exam_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    review_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    order = db.Column(db.Integer, nullable=False, default=0)
    is_fast = db.Column(db.Integer, nullable=False, default=0) # 是否快速通道

    search_fields = ['name_like','state',
        'created_at_begin', 'subject', 'paper_types',
        'created_at_end', 'school_id',
        'city_id', 'province_id', 'area_id', 'year',
        'grade']

    def get_dtl(self):
        result = super(Exam, self).to_dict()
        result = Region.bind_auto(result, 'name', 'city_id', 'id', 'city')
        result = Region.bind_auto(result, 'name', 'province_id', 'id', 'province')
        result = Region.bind_auto(result, 'name', 'area_id', 'id', 'area')
        result = School.bind_auto(result, 'name', 'school_id', 'id', 'school')
        return result

    def to_dict(self):
        return self.get_dtl()

    def to_suggest(self):
        return {'id': self.id, 'name': self.name}

    @staticmethod
    def get_exams(upload_user):
        #查询上传用户试卷记录
        query = Exam.query.\
            filter(Exam.upload_user == upload_user, Exam.state >= EXAM_STATUS['审核不通过'], Exam.is_fast!=1).\
            order_by(Exam.created_at.desc(), Exam.state)
        res = pagination(query)
        return res

    @staticmethod
    def list_exams(state=EXAM_STATUS['已采纳'] ):
        query = Exam.query.filter(Exam.state == state).\
                order_by(Exam.order.desc()).\
                order_by(Exam.created_at.desc())
        if request.args.get('name'):
            query = query.filter(Exam.name.like('%{}%'.format(request.args.get('name'))))
        if request.args.get('subject'):
            query = query.filter(Exam.subject==request.args.get('subject'))
        if request.args.get('paper_types'):
            query = query.filter(Exam.paper_types==request.args.get('paper_types'))
        if request.args.get('province_id'):
            query = query.filter(Exam.province_id==request.args.get('province_id'))
        if request.args.get('city_id'):
            query = query.filter(Exam.city_id==request.args.get('city_id'))
        if request.args.get('area_id'):
            query = query.filter(Exam.area_id==request.args.get('area_id'))
        if request.args.get('school_id'):
            query = query.filter(Exam.school_id==request.args.get('school_id'))
        if request.args.get('year'):
            query = query.filter(Exam.year==request.args.get('year'))
        if request.args.get('grade'):
            query = query.filter(Exam.grade==request.args.get('grade'))
        res = pagination(query)
        return res

    @staticmethod
    def get_exam(id):
        result = Exam.query.get(int(id))
        if result is not None:
            result = result.to_dict()
        else:
            return None
        result = Region.bind_auto(result, 'name', 'city_id', 'id', 'city')
        result = Region.bind_auto(result, 'name', 'province_id', 'id', 'province')
        result = Region.bind_auto(result, 'name', 'area_id', 'id', 'area')
        result = School.bind_auto(result, 'name', 'school_id', 'id', 'school')

        return result

    def get_history(self):
        start_date = self.exam_date - datetime.timedelta(days=5)
        end_date = self.exam_date + datetime.timedelta(days=5)
        query = Exam.query.filter_by(subject=self.subject,
            year=self.year,
            section=self.section,
            school_id=self.school_id,
            grade=self.grade).\
            filter(Exam.id!=self.id).\
            filter(Exam.exam_date >= start_date).\
            filter(Exam.exam_date <= end_date).\
            order_by(Exam.exam_date.desc())
        res = pagination(query)
        return res

    @staticmethod
    def deal_quest_items(items):
        items.sort(key=lambda x: x['exam_id'])
        res = [{'exam_id': eid, 'items': list(items), 'open': False} for eid, items in groupby(items, lambda x: x['exam_id'])]
        for item in res:
            exam = Exam.query.get(item['exam_id'])
            item['exam'] = exam.get_dtl()
        return res

    @staticmethod
    def get_deal_list(deal_obj):
        query = db.session.query(distinct(deal_obj.exam_id)).\
            filter_by(operator_id=g.user.id).\
            order_by(deal_obj.created_at.desc())
        exam_ids = query.all()
        exam_ids = [id[0] for id in exam_ids]
        exam_query = Exam.query.filter(Exam.id.in_(exam_ids))
        exams = pagination(exam_query)
        items = []
        for item in exams['items']:
            questions = deal_obj.query.\
                filter_by(operator_id=g.user.id).\
                filter_by(exam_id=item['id']).\
                order_by(deal_obj.created_at.desc()).\
                all()
            
            questions = [q.get_question_dtl() for q in questions]
            item['open'] = False
            item['questions'] = questions
            items.append(item)
        exams['items'] = School.bind_auto(items, 'name')
        return exams

    @staticmethod
    def get_query(args, query):
        query = query.filter(Exam.state!=-99)
        if args.get('begin_time'):
            query = query.filter(Exam.created_at>=args.get('begin_time'))
        if args.get('end_time'):
            query = query.filter(Exam.created_at<=args.get('end_time'))
        if args.get('province_id'):
            query = query.filter_by(province_id=args.get('province_id'))
        if args.get('city_id'):
            query = query.filter_by(city_id=args.get('city_id'))
        if args.get('area_id'):
            query = query.filter_by(area_id=args.get('area_id'))
        if args.get('school_id'):
            query = query.filter_by(school_id=args.get('school_id'))
        if args.get('grade'):
            query = query.filter_by(grade=args.get('grade'))
        return query

    @staticmethod
    def get_timeline(args):
        query = db.session.query(func.date(Exam.created_at), func.count(Exam.id))
        query = Exam.get_query(args, query)
        res = query.group_by(func.date(Exam.created_at)).all()
        data = {}
        for (t, count) in res:
            data[t.strftime('%Y-%m-%d')] = count
        return data

    @staticmethod
    def get_sumary(args):
        query = Exam.query.filter(Exam.state!=-99)
        query = Exam.get_query(args, query)
        total = query.count()
        ready = query.filter_by(state=0).count()
        reject = query.filter_by(state=-1).count()
        confirming = query.filter_by(state=1).count()
        confirm_pass = query.filter_by(state=5).count()
        usage = query.filter(Exam.state>=2).filter(Exam.state<=4).count()

        return {
            'total': total,
            'ready': ready,
            'reject': reject,
            'confirming': confirming,
            'confirm_pass': confirm_pass,
            'usage': usage
        }
        
    @staticmethod
    def get_statistic(args):
        statistic_type = args.get('statistic_type', 'paper_types')
        return Exam.type_statistic(args, statistic_type)
        

    @staticmethod
    def type_statistic(args, types):
        query = db.session.query(getattr(Exam, types), func.count(Exam.id))
        query = Exam.get_query(args, query)
        res = query.group_by(getattr(Exam, types)).all()
        data = {}
        for (key, count) in res:
            data[key] = count
        return data

    @staticmethod
    def get_suggest(args):
        name = args.get('name', '')
        query = Exam.query.filter(Exam.name.like('%{}%'.format(name)))
        page = int(args.get('pageIndex', 0))
        pageSize = int(args.get('pageSize', current_app.config['PER_PAGE']))
        data = query.paginate(page+1, pageSize, error_out=False)
        items = []
        for item in data.items:
            items.append(item.to_suggest())

        res = {
            'items': items,
            'pageIndex': data.page - 1,
            'pageSize': data.per_page,
            'totalCount': data.total,
            'totalPage': data.pages
        }
        return res


    def __repr__(self):
        return '<Exam: %r>' % self.name
