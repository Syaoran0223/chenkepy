import json, math
from math import ceil
from flask import request, current_app
from sqlalchemy import distinct, func
from app import db
from app.const import EXAM_STATUS,QUEST_STATUS
from app.utils import pagination
from ._base import SessionMixin
from .quest_review_log import QuestReviewLog
from .questLog import QuestLog
from .exam import Exam
from .schools import School
from .qoption import QOption
from .sub_quest import SubQuestion
from .qtype import QType

class Question(db.Model, SessionMixin):
    __tablename__ = 'quest'

    def __init__(self, *args, **kwargs):
        Question.register()
        super(Question, self).__init__(*args, **kwargs)

    id = db.Column(db.Integer, primary_key=True)
    has_sub = db.Column(db.Integer, default=0)
    exam_id = db.Column(db.Integer)
    quest_type_id = db.Column(db.String(16))
    quest_image =  db.Column(db.JsonBlob(), default=[])
    answer_image =  db.Column(db.JsonBlob(), default=[])
    quest_no = db.Column(db.Integer)
    quest_content = db.Column(db.Text)
    quest_content_html = db.Column(db.Text)
    option_count = db.Column(db.Integer)
    options1 = db.Column(db.JsonBlob(), default=[])
    options2 = db.Column(db.JsonBlob(), default=[])
    answer_list1 = db.Column(db.JsonBlob(), default=[])
    answer_list2 = db.Column(db.JsonBlob(), default=[])
    sub_items1 = db.Column(db.JsonBlob(), default=[])
    sub_items2 = db.Column(db.JsonBlob(), default=[])
    qrows = db.Column(db.Integer)
    qcols = db.Column(db.Integer)
    kaodian = db.Column(db.Text)
    fenxi = db.Column(db.Text)
    jieda = db.Column(db.Text)
    correct_answer = db.Column(db.Text)
    correct_answer1 = db.Column(db.Text)
    correct_answer2 = db.Column(db.Text)
    dianpin = db.Column(db.Text)
    knowledge_point = db.Column(db.Text)
    state = db.Column(db.Integer)
    insert_user_id = db.Column(db.Integer)
    refer_quest_id = db.Column(db.Integer, default=0)
    order = db.Column(db.Integer, nullable=False, default=0)
    
    search_fields = ['exam_id','state',
        'created_at_begin', 'subject',
        'created_at_end', 'school_id',
        'city_id', 'province_id', 'area_id']

    @staticmethod
    def search(args):
        query = db.session.query(Question, Exam).\
            outerjoin(Exam, Question.exam_id==Exam.id)
        if args.get('exam_id'):
            query = query.filter(Question.exam_id==args.get('exam_id'))
        if args.get('state') is not None:
            query = query.filter(Question.state==args.get('state'))
        if args.get('created_at_begin'):
            query = query.filter(Question.create_at>=args.get('created_at_begin'))
        if args.get('created_at_end'):
            query = query.filter(Question.created_at<=args.get('created_at_end'))
        if args.get('subject'):
            query = query.filter(Exam.subject==args.get('subject'))
        if args.get('school_id'):
            query = query.filter(Exam.school_id==args.get('school_id'))
        if args.get('grade_id'):
            query = query.filter(Exam.grade_id==args.get('grade_id'))
        if args.get('city_id'):
            query = query.filter(Exam.city_id==args.get('city_id'))
        if args.get('province_id'):
            query = query.filter(Exam.province_id==args.get('province_id'))
        if args.get('area_id'):
            query = query.filter(Exam.area_id==args.get('area_id'))
        page = int(args.get('pageIndex', 0))
        pageSize = int(args.get('pageSize', current_app.config['PER_PAGE']))
        total = query.count()
        query = query.limit(pageSize).offset(pageSize * page)
        res = query.all()
        data = []
        for (question, exam) in res:
            q = question.to_dict()
            q['exam_dict'] = exam.to_dict()
            data.append(q)
        return {
            'items': data,
            'pageIndex': page,
            'pageSize': pageSize,
            'totalCount': total,
            'totalPage': math.ceil(total/pageSize)
        }
        
    
    def __repr__(self):
        return '<Question: %r>' % self.id

    def get_dtl(self):
        exam = Exam.query.get(self.exam_id)
        exam_dict = exam.to_dict() if exam else {}
        res = self.to_dict()
        res['exam'] = exam_dict
        return res

    def get_answer_dtl(self):
        exam = Exam.query.get(self.exam_id)
        exam_dict = exam.to_dict() if exam else {}
        res = self.to_dict()
        res['exam'] = exam_dict
        return res

    def get_verify_dtl(self):
        exam = Exam.query.get(self.exam_id)
        exam_dict = exam.to_dict() if exam else {}
        res = self.to_dict()
        res['exam'] = exam_dict
        # 大小题
        if self.has_sub:
            sub_items = SubQuestion.query.filter_by(parent_id=self.id).all()
            res['sub_items'] = [item.to_dict() for item in sub_items]
        else:
            qtype = QType.query.get(self.quest_type_id)
            # 选择题
            if qtype.is_selector():
                options = QOption.query.filter_by(qid=self.id).all()
                res['options'] = [option.to_dict() for option in options]
        return res

    @staticmethod
    def add_pre_process_quest(exam_id, quest_no,has_sub, quest_type_id, option_count, quest_image, user_id, review_memo, answer_image):
        quest = Question(exam_id=exam_id, quest_no=quest_no,
            has_sub=has_sub, quest_type_id=quest_type_id,
            option_count=option_count, quest_image=quest_image,
            answer_image=answer_image, state=QUEST_STATUS['未处理'],
            insert_user_id=user_id)
        quest.save()

        res = Question.query.get(quest.id)
        return res.to_dict()

    @staticmethod
    def get_quest_by_state(state):
        query = Question.query.filter_by(state=state).\
            order_by(Question.order.desc()).\
            order_by(Question.created_at.desc())
        res = pagination(query)
        items = res.get('items',[])
        items = Exam.bind_auto(items,['name', 'year', 'school_id', 'section', 'subject', 'grade'])
        items = School.bind_auto(items, 'name', 'exam_school_id')
        res['items'] = items
        return res

    # 获取题目状态为state的试卷列表
    @staticmethod
    def get_exam_by_state(state):
        page = int(request.args.get('pageIndex', 0))
        pageSize = int(request.args.get('pageSize', 5))
        query = db.session.query(distinct(Question.exam_id)).\
            filter_by(state=state)
        query = query.\
            order_by(Question.order.desc()).\
            order_by(Question.created_at.desc()).\
            offset(page * pageSize).\
            limit(pageSize)
        exam_ids = query.all()
        
        exam_ids = [id[0] for id in exam_ids]
        exam_query = Exam.query.filter(Exam.id.in_(exam_ids))
        if request.args.get('name'):
            exam_query = exam_query.filter(Exam.name.like('%{}%'.format(request.args.get('name'))))
        if request.args.get('subject'):
            exam_query = exam_query.filter(Exam.subject==request.args.get('subject'))
        if request.args.get('paper_types'):
            exam_query = exam_query.filter(Exam.paper_types==request.args.get('paper_types'))
        if request.args.get('province_id'):
            exam_query = exam_query.filter(Exam.province_id==request.args.get('province_id'))
        if request.args.get('city_id'):
            exam_query = exam_query.filter(Exam.city_id==request.args.get('city_id'))
        if request.args.get('area_id'):
            exam_query = exam_query.filter(Exam.area_id==request.args.get('area_id'))
        if request.args.get('school_id'):
            exam_query = exam_query.filter(Exam.school_id==request.args.get('school_id'))
        if request.args.get('year'):
            exam_query = exam_query.filter(Exam.year==request.args.get('year'))
        if request.args.get('grade'):
            exam_query = exam_query.filter(Exam.grade==request.args.get('grade'))
        totalCount = exam_query.count()
        totalPage = ceil(totalCount / pageSize)
        exams = exam_query.all()
        items = []
        for item in exams:
            questions = Question.query.filter_by(state=state).\
                filter_by(exam_id=item.id).\
                order_by(Question.order.desc()).\
                order_by(Question.created_at.desc())
            questions = [q.to_dict() for q in questions]
            item = item.get_dtl()
            item['open'] = False
            item['questions'] = questions
            items.append(item)

        res = {
            'items': items,
            'pageIndex': page,
            'pageSize': pageSize,
            'totalCount': totalCount,
            'totalPage': totalPage
        }
        return res

    @staticmethod
    def get_sumary(args):
        query = Question.query.join(Exam, Question.exam_id==Exam.id)
        query = Exam.get_query(args, query)
        total = query.count()
        ready = query.filter(Question.state==0).count()
        typing = query.filter(Question.state==1).count()
        no_pass = query.filter(Question.state==2).count()
        ready_answer = query.filter(Question.state==3).count()
        answering = query.filter(Question.state==4).count()
        ready_check = query.filter(Question.state==5).count()
        checking = query.filter(Question.state==6).count()
        ready_judge = query.filter(Question.state==7).count()
        judging = query.filter(Question.state==8).count()
        ready_verify = query.filter(Question.state==9).count()
        verifying = query.filter(Question.state==10).count()
        finished = query.filter(Question.state==99).count()

        return {
            'total': total,
            'ready': ready,
            'typing': typing,
            'no_pass': no_pass,
            'ready_answer': ready_answer,
            'answering': answering,
            'ready_check': ready_check,
            'checking': checking,
            'ready_judge': ready_judge,
            'judging': judging,
            'ready_verify': ready_verify,
            'verifying': verifying,
            'finished': finished
        }

    @staticmethod
    def get_timeline(args):
        query = db.session.query(func.date(Question.created_at), func.count(Question.id)).\
            join(Exam, Question.exam_id==Exam.id)
        query = Question.get_query(args, query)
        res = query.group_by(func.date(Question.created_at)).all()
        data = {}
        for (t, count) in res:
            data[t.strftime('%Y-%m-%d')] = count
        return data

    @staticmethod
    def get_statistic(args):
        statistic_type = args.get('statistic_type', 'quest_type_id')
        if statistic_type in ('quest_type_id', 'state'):
            return Question.type_statistic(args, statistic_type, Question)
        else:
            return Question.type_statistic(args, statistic_type, Exam)
        

    @staticmethod
    def type_statistic(args, types, Obj):
        query = db.session.query(getattr(Obj, types), func.count(Question.id))
        if Obj is Question:
            query = query.join(Exam, Question.exam_id==Exam.id)
        else:
            query = query.join(Question, Question.exam_id==Exam.id)
        query = Question.get_query(args, query)
        res = query.group_by(getattr(Obj, types)).all()
        data = {}
        for (key, count) in res:
            if key is None:
                key = 'unknown'
            data[key] = count
        return data
    
    @staticmethod
    def get_query(args, query):
        query = query.filter(Question.state!=-99)
        if args.get('begin_time'):
            query = query.filter(Question.created_at>=args.get('begin_time'))
        if args.get('end_time'):
            query = query.filter(Question.created_at<=args.get('end_time'))
        if args.get('province_id'):
            query = query.filter(Exam.province_id==args.get('province_id'))
        if args.get('city_id'):
            query = query.filter(Exam.city_id==args.get('city_id'))
        if args.get('area_id'):
            query = query.filter(Exam.area_id==args.get('area_id'))
        if args.get('school_id'):
            query = query.filter(Exam.school_id==args.get('school_id'))
        if args.get('grade'):
            query = query.filter(Exam.grade==args.get('grade'))
        return query