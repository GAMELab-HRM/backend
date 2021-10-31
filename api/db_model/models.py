from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, LargeBinary , DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship 
import uuid 
from db_model.database import Base 

# our database table format 

class Patient_info(Base):
    __tablename__ = "patient_info"
    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False, default=uuid.uuid4)
    patient_id = Column(String, nullable=False)
    sensor_num = Column(Integer, nullable=False)
    ws_data = relationship("Wet_swallows_10", back_populates="patient")

class Doctor_info(Base):
    __tablename__ = "doctor_info"
    doctor_id = Column(Integer, nullable=False, primary_key=True, unique=True)
    doctor_name = Column(String, nullable=False)
    ws_data = relationship("Wet_swallows_10", back_populates="doctor")

class Wet_swallows_10(Base):
    __tablename__ = "wet_swallows_10"
    id = Column(UUID(as_uuid=True), ForeignKey("patient_info.id"), primary_key=True, unique=True, nullable=False, default=uuid.uuid4)
    doctor_id = Column(Integer, ForeignKey("doctor_info.doctor_id"), primary_key=True, nullable=False, unique=True)
    vigors = Column(LargeBinary)
    patterns = Column(LargeBinary)
    dcis = Column(LargeBinary)
    swallow_types = Column(LargeBinary)
    irp4s = Column(LargeBinary)
    dls = Column(LargeBinary)
    pressure_max = Column(Integer)
    pressure_min = Column(Integer)

    patient = relationship("Patient_info", back_populates="ws_data")
    doctor = relationship("Doctor_info", back_populates="ws_data")
    # bytea using sqlalchemy's LargeBinary

class Raw_Data(Base):
    __tablename__ = "raw_data"
    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False, default=uuid.uuid4)
    doctor_id = Column(Integer, primary_key=True, nullable=False, unique=True)
    last_update = Column(DateTime(timezone=True))
    ws_10_raw = Column(LargeBinary)
    mrs_raw = Column(LargeBinary)
    rdc_raw = Column(LargeBinary)
    hh_raw = Column(LargeBinary)