from app import db
from ._base import SessionMixin

class Device(db.Model, SessionMixin):
    __tablename__ = 'device'

    id = db.Column(db.Integer, primary_key=True)  # id
    device_code = db.Column(db.String(32), nullable=False, default='')  # 设备号
    project_id = db.Column(db.Integer, nullable=False, default=0) #专题

    def __repr__(self):
        return '<Device: %r>' % self.id

    @staticmethod
    def get_device(device_code):
        device = Device.query.filter_by(device_code=device_code).first()
        return device
