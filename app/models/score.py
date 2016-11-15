from app import db
from ._base import SessionMixin

class Score(db.Model, SessionMixin):
    __tablename__ = 'score'

    def __init__(self, *args, **kwargs):
        Score.register()
        super(Score, self).__init__(*args, **kwargs)

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    info = db.Column(db.String(400))
    score = db.Column(db.Integer)
    type = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    @staticmethod
    def add(user_id, title, info, score):
        score = Score(
            title = title,
            info = info,
            score = score,
            type = 1,
            user_id = user_id
        )
        score.save()

    @staticmethod
    def reduce(user_id, title, info, score):
        score = Score(
            title = title,
            info = info,
            score = score,
            type = -1,
            user_id = user_id
        )
        score.save()

    def __repr__(self):
        return '<Score: %r>' % self.title
