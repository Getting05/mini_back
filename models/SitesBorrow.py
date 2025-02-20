from .base import BaseModel
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.sql import func
from utils.database import Base


class SitesBorrow(Base):
    def __init__(self, id, site_name, borrow_date):
        super().__init__(id)
        self.site_name = site_name
        self.borrow_date = borrow_date


    __tablename__ = 'sites_borrow'
    id = Column(Integer, primary_key=True)
    apply_id = Column(String, unique=True)
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
    updated_at = Column(String)  # 使用DateTime类型还是String?
