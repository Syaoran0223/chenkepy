import json, math
from math import ceil
from flask import request, current_app
from sqlalchemy import distinct
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
        'created_at_end', 'school_id', 'grade_id',
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
            # 选择题
            if self.quest_type_id == '1':
                options = QOption.query.filter_by(qid=self.id).all()
                res['options'] = [option.to_dict() for option in options]
            # 填空题
            elif self.quest_type_id == '2':
                res['correct_answer'] = json.loads(self.correct_answer)
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
        totalCount = query.count()
        totalPage = ceil(totalCount / pageSize)
        query = query.\
            order_by(Question.order.desc()).\
            order_by(Question.created_at.desc()).\
            offset(page * pageSize).\
            limit(pageSize)
        exam_ids = query.all()
        
        exam_ids = [id[0] for id in exam_ids]
        exams = Exam.query.filter(Exam.id.in_(exam_ids)).all()
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