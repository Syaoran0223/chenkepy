from app import db
from ._base import SessionMixin

class SubQuestion(db.Model, SessionMixin):
    __tablename__ = 'sub_quest'

    def __init__(self, *args, **kwargs):
        SubQuestion.register()
        super(SubQuestion, self).__init__(*args, **kwargs)

    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer)
    quest_content = db.Column(db.String(1000))
    quest_content_html = db.Column(db.String(1000))

    quest_option_html = db.Column(db.String(1000))
    kaodian = db.Column(db.String(255))
    fenxi = db.Column(db.String(1000))
    jieda = db.Column(db.String(1000))
    dianpin = db.Column(db.String(1000))
    correct_answer = db.Column(db.String(255))
    quest_image = db.Column(db.JsonBlob(), default=[])
    answer_image = db.Column(db.JsonBlob(), default=[])
    quest_no = db.Column(db.Integer)
    qtype = db.Column(db.String(200))
    quest_type_id = db.Column(db.Integer)
    option_count = db.Column(db.Integer)
    qrows = db.Column(db.Integer)
    qcols = db.Column(db.Integer)
    state = db.Column(db.Integer)
    insert_user_id = db.Column(db.Integer)

    def __repr__(self):
        return '<SubQuestion: %r>' % self.id
