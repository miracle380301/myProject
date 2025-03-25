from sqlalchemy import Column, DateTime, Integer, String
from database import Base  # Import Base from database.py 
class Exchange(Base):
     __tablename__ = "exchanges"
 
     id = Column(Integer, primary_key=True, autoincrement=True)
     name = Column(String(100), nullable=False, unique=True)  # 거래소 이름
     year = Column(String(100), nullable=True, unique=False)  # 설립연도
     country = Column(String(100), nullable=True, unique=False)  # 국가
     url = Column(String(255), nullable=True)  # 거래소 링크
     logo = Column(String(255), nullable=True)  # 거래소 아이콘 (이미지 URL)
     origin = Column(String(255), nullable=True)  # 거래소 출처
     create_dt = Column(DateTime, nullable=False)  # 생성일
     update_dt = Column(DateTime, nullable=False)  # 수정일

     def __repr__(self):
         return f"<Exchange(name={self.name}, year={self.year}, country={self.country}, url={self.url}, logo={self.logo}, origin={self.origin}, create_dt={self.create_dt}, update_dt={self.update_dt})>"
