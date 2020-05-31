from app import models as m
from app.extensions import db


class PostbackLogRepository(object):

    def create(self, args):
        '''
        id = db.Column(GUID(), primary_key=True, default=uuid4)
        user_id = db.Column(GUID(), db.ForeignKey('users.id'), nullable=True)
        order_id = db.Column(db.Integer())
        offer_id = db.Column(GUID, db.ForeignKey('offers.id'), nullable=True)
        url = db.Column(db.String(255), nullable=False)
        raw_url = db.Column(db.String(255), nullable=False)
        raw_response = db.Column(db.Text)
        status = db.Column(db.Enum(PostbackLogStatus), default=lambda: PostbackLogStatus.SUCCESS)
        '''
        postback_log = m.PostbackLog(**args)
        db.session.add(postback_log)
        db.session.commit()
        return postback_log

    def create_from_args(self, args):
        try:
            postback_log = m.PostbackLog(**args)
            db.session.add(postback_log)
            db.session.commit()
            return postback_log
        except Exception as e:
            print(e)
            return None

    def get_list(self, args):
        return m.PostbackLog.query.all()


postback_log_repo = PostbackLogRepository()
