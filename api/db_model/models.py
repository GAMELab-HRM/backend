from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, LargeBinary , DateTime, Float, JSON
from sqlalchemy.types import ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship 
import uuid, datetime, pickle
from db_model.database import Base 

ws_temp = [""  for i in range(10)]

# our database table format 
class Patient_info(Base):
    __tablename__ = "patient_info"
    record_id = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False, default=uuid.uuid4)
    patient_id = Column(String, nullable=False)
    catheter_type = Column(Integer, default=-1)
    ws_data = relationship("Wet_swallows_10", back_populates="patient", cascade="all, delete", passive_deletes=True)
    rawdata = relationship("Raw_Data", back_populates="patient", cascade="all, delete", passive_deletes=True)
    time_data = relationship("Time_Record", back_populates="patient", cascade="all, delete", passive_deletes=True)
    mrs_data = relationship("Mrs", back_populates="patient", cascade="all, delete", passive_deletes=True)
    hh_data = relationship("Hiatal_Hernia", back_populates="patient", cascade="all, delete", passive_deletes=True)
    leg_data = relationship("Leg", back_populates="patient", cascade="all, delete", passive_deletes=True)
    air_data = relationship("Air", back_populates="patient", cascade="all, delete", passive_deletes=True)

class Doctor_info(Base):
    __tablename__ = "doctor_info"
    doctor_id = Column(Integer, nullable=False, primary_key=True, unique=True)
    doctor_name = Column(String, nullable=False)
    ws_data = relationship("Wet_swallows_10", back_populates="doctor")
    time_data = relationship("Time_Record", back_populates="doctor")
    mrs_data = relationship("Mrs", back_populates="doctor")
    hh_data = relationship("Hiatal_Hernia", back_populates="doctor")
    leg_data = relationship("Leg", back_populates="doctor")
    air_data = relationship("Air", back_populates="doctor")
    
class Wet_swallows_10(Base):
    __tablename__ = "wet_swallows_10"
    index = Column(Integer, primary_key=True)
    record_id = Column(UUID(as_uuid=True), ForeignKey("patient_info.record_id", ondelete="CASCADE"), nullable=False, default=uuid.uuid4)
    doctor_id = Column(Integer, ForeignKey("doctor_info.doctor_id"), nullable=False)
    vigors = Column(ARRAY(String), default=ws_temp)
    patterns = Column(ARRAY(String), default=ws_temp)
    dcis = Column(ARRAY(String), default=ws_temp)
    breaks = Column(ARRAY(String), default=ws_temp)
    swallow_types = Column(String, default=ws_temp)
    ws_result = Column(String, default="")
    irp4s = Column(ARRAY(String), default=ws_temp)
    dls = Column(ARRAY(String), default=ws_temp)
    pressure_max = Column(Integer)
    pressure_min = Column(Integer)
    patient = relationship("Patient_info", back_populates="ws_data")
    doctor = relationship("Doctor_info", back_populates="ws_data")

class Air(Base):
    __tablename__ = "air"
    index = Column(Integer, primary_key=True)
    record_id = Column(UUID(as_uuid=True), ForeignKey("patient_info.record_id", ondelete="CASCADE"), nullable=False, default=uuid.uuid4)
    doctor_id = Column(Integer, ForeignKey("doctor_info.doctor_id"), nullable=False)
    air_metric = Column(JSON, default={})
    patient = relationship("Patient_info", back_populates="air_data")
    doctor = relationship("Doctor_info", back_populates="air_data")
    
class Mrs(Base):
    __tablename__ = "mrs"
    index = Column(Integer, primary_key=True)
    record_id = Column(UUID(as_uuid=True), ForeignKey("patient_info.record_id", ondelete="CASCADE"), nullable=False, default=uuid.uuid4)
    draw_info = Column(JSON, default={})
    mrs_metric = Column(JSON, default={})
    doctor_id = Column(Integer, ForeignKey("doctor_info.doctor_id"), nullable=False)
    mrs_result = Column(String, default="")
    pressure_max = Column(Integer)
    pressure_min = Column(Integer)
    patient = relationship("Patient_info", back_populates="mrs_data")
    doctor = relationship("Doctor_info", back_populates="mrs_data")

class Hiatal_Hernia(Base):
    __tablename__ = "hiatal_hernia"
    index = Column(Integer, primary_key=True)
    record_id = Column(UUID(as_uuid=True), ForeignKey("patient_info.record_id", ondelete="CASCADE"), nullable=False, default=uuid.uuid4)
    draw_info = Column(JSON, default={})
    hh_metric = Column(JSON, default={})
    hiatal_hernia_result = Column(String, default="")
    rip_result = Column(String, default="")
    doctor_id = Column(Integer, ForeignKey("doctor_info.doctor_id"), nullable=False)
    pressure_max = Column(Integer)
    pressure_min = Column(Integer)
    black_line = Column(Integer)
    patient = relationship("Patient_info", back_populates="hh_data")
    doctor = relationship("Doctor_info", back_populates="hh_data")

class Leg(Base):
    __tablename__ = "leg"
    index = Column(Integer, primary_key=True)
    record_id = Column(UUID(as_uuid=True), ForeignKey("patient_info.record_id", ondelete="CASCADE"), nullable=False, default=uuid.uuid4)
    draw_info = Column(JSON, default={})
    leg_metric = Column(JSON, default={})
    leg_result = Column(String, default="")
    doctor_id = Column(Integer, ForeignKey("doctor_info.doctor_id"), nullable=False)
    patient = relationship("Patient_info", back_populates="leg_data")
    doctor = relationship("Doctor_info", back_populates="leg_data")
    
class Raw_Data(Base):
    __tablename__ = "raw_data"
    index = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    record_id = Column(UUID(as_uuid=True),  ForeignKey("patient_info.record_id", ondelete="CASCADE"), nullable=False, default=uuid.uuid4)
    all_raw = Column(LargeBinary)
    ws_10_raw = Column(LargeBinary)
    ws_10_index = Column(ARRAY(Integer))
    mrs_raw = Column(LargeBinary)
    mrs_index = Column(ARRAY(Integer))
    rdc_raw = Column(LargeBinary)
    rdc_index = Column(ARRAY(Integer))
    hh_raw = Column(LargeBinary)
    hh_index = Column(ARRAY(Integer))
    leg_raw = Column(LargeBinary)
    leg_index = Column(ARRAY(Integer))
    patient = relationship("Patient_info", back_populates="rawdata")

class Time_Record(Base):
    __tablename__ = "time_record"
    index = Column(Integer, primary_key=True)
    record_id = Column(UUID(as_uuid=True),  ForeignKey("patient_info.record_id", ondelete="CASCADE"), nullable=False, default=uuid.uuid4)
    doctor_id = Column(Integer, ForeignKey("doctor_info.doctor_id"), nullable=False)
    last_update = Column(DateTime(timezone=True), default=datetime.datetime.now())
    patient = relationship("Patient_info", back_populates="time_data")
    doctor = relationship("Doctor_info", back_populates="time_data")

class User_Record(Base):
    __tablename__ = "user_record"
    username = Column(String, primary_key=True)
    password = Column(String, nullable=False)