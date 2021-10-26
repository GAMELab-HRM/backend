from sqlalchemy import Boolean, Column, ForeignKey, Integer, String 
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship 
import uuid 
from db_model.database import Base 

class Patient(Base):
    __tablename__ = "patient_info"
    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False, default=uuid.uuid4)
    patient_id = Column(String, nullable=False)
    sensor_num = Column(Integer, nullable=False)
