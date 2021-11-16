from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, LargeBinary , DateTime, Float
from sqlalchemy.types import ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship 
import uuid, datetime, pickle
from db_model.database import Base 

ws_temp = [""  for i in range(10)]
mrs_temp = ["" for i in range(5)]
init_position = [["","","",""] for i in range(5)] # mrs1 ~ mrs5

# our database table format 
class Patient_info(Base):
    __tablename__ = "patient_info"
    record_id = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False, default=uuid.uuid4)
    patient_id = Column(String, nullable=False)
    sensor_num = Column(Integer, nullable=False)

    ws_data = relationship("Wet_swallows_10", back_populates="patient", cascade="all, delete", passive_deletes=True)
    rawdata = relationship("Raw_Data", back_populates="patient", cascade="all, delete", passive_deletes=True)
    time_data = relationship("Time_Record", back_populates="patient", cascade="all, delete", passive_deletes=True)
    mrs_data = relationship("Mrs", back_populates="patient", cascade="all, delete", passive_deletes=True)
    hh_data = relationship("Hiatal_Hernia", back_populates="patient", cascade="all, delete", passive_deletes=True)

class Doctor_info(Base):
    __tablename__ = "doctor_info"
    doctor_id = Column(Integer, nullable=False, primary_key=True, unique=True)
    doctor_name = Column(String, nullable=False)

    ws_data = relationship("Wet_swallows_10", back_populates="doctor")
    time_data = relationship("Time_Record", back_populates="doctor")
    mrs_data = relationship("Mrs", back_populates="doctor")
    hh_data = relationship("Hiatal_Hernia", back_populates="doctor")

class Wet_swallows_10(Base):
    __tablename__ = "wet_swallows_10"
    index = Column(Integer, primary_key=True)
    record_id = Column(UUID(as_uuid=True), ForeignKey("patient_info.record_id", ondelete="CASCADE"), nullable=False, default=uuid.uuid4)
    doctor_id = Column(Integer, ForeignKey("doctor_info.doctor_id"), nullable=False)
    vigors = Column(ARRAY(String), default=ws_temp)
    patterns = Column(ARRAY(String), default=ws_temp)
    dcis = Column(ARRAY(String), default=ws_temp)
    swallow_types = Column(String, default=ws_temp)
    ws_result = Column(String, default="")
    irp4s = Column(ARRAY(String), default=ws_temp)
    dls = Column(ARRAY(String), default=ws_temp)

    pressure_max = Column(Integer)
    pressure_min = Column(Integer)

    patient = relationship("Patient_info", back_populates="ws_data")
    doctor = relationship("Doctor_info", back_populates="ws_data")
    
class Mrs(Base):
    __tablename__ = "mrs"
    index = Column(Integer, primary_key=True)
    record_id = Column(UUID(as_uuid=True), ForeignKey("patient_info.record_id", ondelete="CASCADE"), nullable=False, default=uuid.uuid4)
    mrs_dci_position = Column(ARRAY(String), default=init_position)
    mrs_dci = Column(ARRAY(String), default=mrs_temp)
    dci_after_mrs_position = Column(ARRAY(String), default=init_position)
    dci_after_mrs = Column(ARRAY(String), default=mrs_temp)
    irp1_position = Column(ARRAY(String), default=init_position)
    irp1 = Column(ARRAY(String), default=mrs_temp)
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
    les_position = Column(Float)
    cd_position = Column(Float)
    rip_position = Column(Float)
    seperate = Column(Boolean)
    hiatal_hernia_result = Column(String)
    rip_result = Column(String)
    doctor_id = Column(Integer, ForeignKey("doctor_info.doctor_id"), nullable=False)
    pressure_max = Column(Integer)
    pressure_min = Column(Integer)
    black_line = Column(Integer)

    # to do relationship
    patient = relationship("Patient_info", back_populates="hh_data")
    doctor = relationship("Doctor_info", back_populates="hh_data")
    
class Raw_Data(Base):
    __tablename__ = "raw_data"
    index = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    record_id = Column(UUID(as_uuid=True),  ForeignKey("patient_info.record_id", ondelete="CASCADE"), nullable=False, default=uuid.uuid4)
    ws_10_raw = Column(LargeBinary)
    mrs_raw = Column(LargeBinary)
    rdc_raw = Column(LargeBinary)
    hh_raw = Column(LargeBinary)

    patient = relationship("Patient_info", back_populates="rawdata")

class Time_Record(Base):
    __tablename__ = "time_record"
    index = Column(Integer, primary_key=True)
    record_id = Column(UUID(as_uuid=True),  ForeignKey("patient_info.record_id", ondelete="CASCADE"), nullable=False, default=uuid.uuid4)
    doctor_id = Column(Integer, ForeignKey("doctor_info.doctor_id"), nullable=False)
    last_update = Column(DateTime(timezone=True), default=datetime.datetime.now())

    patient = relationship("Patient_info", back_populates="time_data")
    doctor = relationship("Doctor_info", back_populates="time_data")