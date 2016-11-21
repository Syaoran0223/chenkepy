from app import db
from ._base import SessionMixin

class Question(db.Model, SessionMixin):
    __tablename__ = 'quest'

    def __init__(self, *args, **kwargs):
        Exam.register()
        super(Exam, self).__init__(*args, **kwargs)

    id = db.Column(db.Integer, primary_key=True)
    has_sub = db.Column(db.Boolean, default=False)
    exam_id = db.Column(db.Integer)
    quest_type_id = db.Column(db.Integer)
    quest_no = db.Column(db.Integer)
    quest_content = db.Column(db.String(1000))
    quest_content_html = db.Column(db.String(1000))
    qrows = db.Column(db.Integer)
    qcols = db.Column(db.Integer)
    kaodian = db.Column(db.String(255))
    fenxi = db.Column(db.String(255))
    jieda = db.Column(db.String(255))
    correct_answer = db.Column(db.String(255))
    knowledge_point = db.Column(db.String(255))
    state = db.Column(db.String(255))
    
    def __repr__(self):
        return '<Question: %r>' % self.id
