from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, LargeBinary 
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship 
import uuid 
from db_model.database import Base 

# our database table format 

class Patient(Base):
    __tablename__ = "patient_info"
    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False, default=uuid.uuid4)
    patient_id = Column(String, nullable=False)
    sensor_num = Column(Integer, nullable=False)

class Doctor(Base):
    __tablename__ = "doctor_info"
    doctor_id = Column(Integer, nullable=False, primary_key=True, unique=True)
    doctor_name = Column(String, nullable=False)

class Wetswallows(Base):
    __tablename__ = "wet_swallows_10"
    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False, default=uuid.uuid4)
    doctor_id = Column(Integer, primary_key=True, nullable=False, unique=True)
    vigors = Column(LargeBinary)
    patterns = Column(LargeBinary)
    dcis = Column(LargeBinary)
    swallow_types = Column(LargeBinary)
    irp4s = Column(LargeBinary)
    dls = Column(LargeBinary)
    pressure_max = Column(Integer)
    pressure_min = Column(Integer)
    # bytea using sqlalchemy's LargeBinary