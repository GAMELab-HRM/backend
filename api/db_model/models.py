from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, LargeBinary , DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship 
import uuid, datetime
from db_model.database import Base 

# our database table format 

class Patient_info(Base):
    __tablename__ = "patient_info"
    record_id = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False, default=uuid.uuid4)
    patient_id = Column(String, nullable=False)
    sensor_num = Column(Integer, nullable=False)

    ws_data = relationship("Wet_swallows_10", back_populates="patient")
    rawdata = relationship("Raw_Data", back_populates="patient")
    time_data = relationship("Time_Record", back_populates="patient")

class Doctor_info(Base):
    __tablename__ = "doctor_info"
    doctor_id = Column(Integer, nullable=False, primary_key=True, unique=True)
    doctor_name = Column(String, nullable=False)

    ws_data = relationship("Wet_swallows_10", back_populates="doctor")
    time_data = relationship("Time_Record", back_populates="doctor")

class Wet_swallows_10(Base):
    __tablename__ = "wet_swallows_10"
    index = Column(Integer, primary_key=True)
    record_id = Column(UUID(as_uuid=True), ForeignKey("patient_info.record_id"), nullable=False, default=uuid.uuid4)
    doctor_id = Column(Integer, ForeignKey("doctor_info.doctor_id"), nullable=False)
    vigors = Column(LargeBinary)
    patterns = Column(LargeBinary)
    dcis = Column(LargeBinary)
    swallow_types = Column(LargeBinary)
    ws_result = Column(String)
    irp4s = Column(LargeBinary)
    dls = Column(LargeBinary)
    pressure_max = Column(Integer)
    pressure_min = Column(Integer)

    patient = relationship("Patient_info", back_populates="ws_data")
    doctor = relationship("Doctor_info", back_populates="ws_data")
    # bytea using sqlalchemy's LargeBinary

class Raw_Data(Base):
    __tablename__ = "raw_data"
    index = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    record_id = Column(UUID(as_uuid=True),  ForeignKey("patient_info.record_id"), nullable=False, default=uuid.uuid4)
    ws_10_raw = Column(LargeBinary)
    mrs_raw = Column(LargeBinary)
    rdc_raw = Column(LargeBinary)
    hh_raw = Column(LargeBinary)

    patient = relationship("Patient_info", back_populates="rawdata")

class Time_Record(Base):
    __tablename__ = "time_record"
    index = Column(Integer, primary_key=True)
    record_id = Column(UUID(as_uuid=True),  ForeignKey("patient_info.record_id"), nullable=False, default=uuid.uuid4)
    doctor_id = Column(Integer, ForeignKey("doctor_info.doctor_id"), nullable=False)
    last_update = Column(DateTime(timezone=True), default=datetime.datetime.now())

    patient = relationship("Patient_info", back_populates="time_data")
    doctor = relationship("Doctor_info", back_populates="time_data")