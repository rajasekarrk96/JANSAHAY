import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Boolean, Integer, Text, DateTime, JSON, ForeignKey, Enum
)
from sqlalchemy.orm import relationship
from app.db.base import Base

def generate_uuid():
    return str(uuid.uuid4())

class UserRole(str):
    CITIZEN = "CITIZEN"
    VERIFICATION_OFFICER = "VERIFICATION_OFFICER"
    DEPARTMENT_OFFICER = "DEPARTMENT_OFFICER"
    APPROVING_OFFICER = "APPROVING_OFFICER"
    SYSTEM_ADMIN = "SYSTEM_ADMIN"

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    username = Column(String(64), unique=True, index=True, nullable=False)
    email = Column(String(128), unique=True, index=True, nullable=False)
    phone_number = Column(String(20), nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(32), nullable=False, default=UserRole.CITIZEN)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    citizen_profile = relationship("Citizen", back_populates="user", uselist=False, cascade="all, delete-orphan")
    officer_profile = relationship("Officer", back_populates="user", uselist=False, cascade="all, delete-orphan")
    notifications = relationship("NotificationOutbox", back_populates="recipient")

class Citizen(Base):
    __tablename__ = "citizens"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), unique=True, nullable=False)
    full_name = Column(String(128), nullable=False)
    synthetic_aadhaar_last4 = Column(String(4), nullable=False, default="1234")
    date_of_birth = Column(String(32), nullable=False, default="1990-01-01")
    address_line = Column(Text, nullable=False)
    district = Column(String(64), nullable=False)
    state = Column(String(64), nullable=False)
    pincode = Column(String(6), nullable=False)

    user = relationship("User", back_populates="citizen_profile")
    cases = relationship("Case", back_populates="citizen")

class Department(Base):
    __tablename__ = "departments"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    code = Column(String(32), unique=True, index=True, nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(Text, nullable=True)

    officers = relationship("Officer", back_populates="department")
    services = relationship("Service", back_populates="department")
    cases = relationship("Case", back_populates="department")

class Jurisdiction(Base):
    __tablename__ = "jurisdictions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    code = Column(String(32), unique=True, index=True, nullable=False)
    name = Column(String(128), nullable=False)
    state = Column(String(64), nullable=False)

    officers = relationship("Officer", back_populates="jurisdiction")
    cases = relationship("Case", back_populates="jurisdiction")

class Officer(Base):
    __tablename__ = "officers"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), unique=True, nullable=False)
    employee_code = Column(String(32), unique=True, index=True, nullable=False)
    full_name = Column(String(128), nullable=False)
    designation = Column(String(128), nullable=False)
    department_id = Column(String(36), ForeignKey("departments.id"), nullable=False)
    jurisdiction_id = Column(String(36), ForeignKey("jurisdictions.id"), nullable=False)

    user = relationship("User", back_populates="officer_profile")
    department = relationship("Department", back_populates="officers")
    jurisdiction = relationship("Jurisdiction", back_populates="officers")
    assigned_cases = relationship("Case", back_populates="assigned_officer")

class Service(Base):
    __tablename__ = "services"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    code = Column(String(64), unique=True, index=True, nullable=False)
    title = Column(String(128), nullable=False)
    category = Column(String(64), nullable=False) # CERTIFICATES, SOCIAL_SECURITY, GRIEVANCES
    department_id = Column(String(36), ForeignKey("departments.id"), nullable=False)
    sla_days = Column(Integer, default=7, nullable=False)
    eligibility_criteria_json = Column(JSON, default=dict, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    department = relationship("Department", back_populates="services")
    requirements = relationship("ServiceRequirement", back_populates="service", cascade="all, delete-orphan")
    workflows = relationship("WorkflowDefinition", back_populates="service", cascade="all, delete-orphan")
    cases = relationship("Case", back_populates="service")

class ServiceRequirement(Base):
    __tablename__ = "service_requirements"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    service_id = Column(String(36), ForeignKey("services.id"), nullable=False)
    document_type_code = Column(String(64), nullable=False)
    document_name = Column(String(128), nullable=False)
    is_mandatory = Column(Boolean, default=True, nullable=False)
    allowed_extensions = Column(String(64), default=".pdf,.jpg,.jpeg,.png", nullable=False)
    max_size_kb = Column(Integer, default=5120, nullable=False)

    service = relationship("Service", back_populates="requirements")
    documents = relationship("Document", back_populates="requirement")

class WorkflowDefinition(Base):
    __tablename__ = "workflow_definitions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    service_id = Column(String(36), ForeignKey("services.id"), nullable=False)
    version = Column(Integer, default=1, nullable=False)
    initial_state = Column(String(64), default="SUBMITTED", nullable=False)
    definition_json = Column(JSON, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    service = relationship("Service", back_populates="workflows")

class Case(Base):
    __tablename__ = "cases"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    public_case_id = Column(String(32), unique=True, index=True, nullable=False)
    service_id = Column(String(36), ForeignKey("services.id"), nullable=False)
    workflow_version = Column(Integer, default=1, nullable=False)
    citizen_id = Column(String(36), ForeignKey("citizens.id"), nullable=False)
    department_id = Column(String(36), ForeignKey("departments.id"), nullable=False)
    jurisdiction_id = Column(String(36), ForeignKey("jurisdictions.id"), nullable=False)
    current_state = Column(String(64), nullable=False, default="SUBMITTED")
    version_id = Column(Integer, default=1, nullable=False) # Optimistic locking
    assigned_officer_id = Column(String(36), ForeignKey("officers.id"), nullable=True)
    form_data_json = Column(JSON, default=dict, nullable=False)
    resolution_remarks = Column(Text, nullable=True)
    submitted_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    citizen = relationship("Citizen", back_populates="cases")
    service = relationship("Service", back_populates="cases")
    department = relationship("Department", back_populates="cases")
    jurisdiction = relationship("Jurisdiction", back_populates="cases")
    assigned_officer = relationship("Officer", back_populates="assigned_cases")
    documents = relationship("Document", back_populates="case", cascade="all, delete-orphan")
    audit_events = relationship("AuditEvent", back_populates="case", order_by="AuditEvent.event_sequence", cascade="all, delete-orphan")
    notifications = relationship("NotificationOutbox", back_populates="case", cascade="all, delete-orphan")

class Document(Base):
    __tablename__ = "documents"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    case_id = Column(String(36), ForeignKey("cases.id"), nullable=False)
    requirement_id = Column(String(36), ForeignKey("service_requirements.id"), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(512), nullable=False)
    mime_type = Column(String(64), nullable=False)
    file_size_bytes = Column(Integer, nullable=False)
    status = Column(String(32), default="AVAILABLE", nullable=False) # QUARANTINED, SCAN_PASSED, AVAILABLE, VERIFIED, REPLACEMENT_REQUIRED, REPLACED
    version = Column(Integer, default=1, nullable=False)
    verification_notes = Column(Text, nullable=True)
    uploaded_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    case = relationship("Case", back_populates="documents")
    requirement = relationship("ServiceRequirement", back_populates="documents")

class AuditEvent(Base):
    __tablename__ = "audit_events"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    case_id = Column(String(36), ForeignKey("cases.id"), index=True, nullable=False)
    event_sequence = Column(Integer, nullable=False)
    actor_id = Column(String(36), nullable=False)
    actor_role = Column(String(32), nullable=False)
    action = Column(String(64), nullable=False)
    from_state = Column(String(64), nullable=False)
    to_state = Column(String(64), nullable=False)
    remarks = Column(Text, nullable=True)
    previous_event_hash = Column(String(64), nullable=False)
    event_hash = Column(String(64), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    case = relationship("Case", back_populates="audit_events")

class NotificationOutbox(Base):
    __tablename__ = "notification_outbox"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    case_id = Column(String(36), ForeignKey("cases.id"), nullable=False)
    recipient_user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    channel = Column(String(32), default="IN_APP", nullable=False)
    title = Column(String(128), nullable=False)
    message = Column(Text, nullable=False)
    status = Column(String(32), default="PENDING", nullable=False) # PENDING, PROCESSED, FAILED
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    processed_at = Column(DateTime, nullable=True)

    case = relationship("Case", back_populates="notifications")
    recipient = relationship("User", back_populates="notifications")

class AIInteraction(Base):
    __tablename__ = "ai_interactions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    session_id = Column(String(64), nullable=False)
    prompt = Column(Text, nullable=False)
    response_json = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
