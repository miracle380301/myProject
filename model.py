from sqlalchemy import Column, Integer, String
from database import Base  # Import Base from database.py

class Exchange(Base):
    __tablename__ = "exchanges"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)  # 거래소 이름
    link = Column(String(255), nullable=False)  # 거래소 링크
    logo = Column(String(255), nullable=True)  # 거래소 아이콘 (이미지 URL)
    origin = Column(String(255), nullable=True)  # 거래소 출처

    def __repr__(self):
        return f"<Exchange(id={self.id}, name={self.name}, link={self.link}, logo={self.logo})>"
