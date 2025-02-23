from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text
from utils.database import Base

db = SQLAlchemy()


class SitesBorrow(Base):
    def __init__(self, id, apply_id, site_name, name, student_id, phonenum, email, purpose, mentor_name,
                 mentor_phone_num, picture, start_time, end_time, state, reason, created_at, updated_at):
        super().__init__(id)
        self.id = id
        self.site_name = site_name
        self.name = name
        self.student_id = student_id
        self.phonenum = phonenum
        self.email = email
        self.purpose = purpose
        self.mentor_name = mentor_name
        self.mentor_phone_num = mentor_phone_num
        self.picture = picture
        self.start_time = start_time
        self.end_time = end_time
        self.state = state
        self.reason = reason
        self.created_at = created_at
        self.updated_at = updated_at
        self.apply_id = apply_id

    __tablename__ = 'sites_borrow'
    id = Column(Integer, primary_key=True)
    apply_id = Column(String)
    name = Column(String)
    student_id = Column(String)
    phonenum = Column(String)
    email = Column(String)
    purpose = Column(String)
    mentor_name = Column(String)
    mentor_phone_num = Column(String)
    picture = Column(Text)
    start_time = Column(String)
    end_time = Column(String)
    state = Column(Integer, default=0)  # 0: 待审核，1: 已通过 2: 已拒绝 3: 已取消
    reason = Column(Text, default=None)
    created_at = Column(String)
    updated_at = Column(String)
