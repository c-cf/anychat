from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Enum, Text, JSON, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class StatusEnum(enum.Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    ARCHIVED = "ARCHIVED"

class RoleEnum(enum.Enum):
    USER = "USER"
    ASSISTANT = "ASSISTANT"

class PermissionTypeEnum(enum.Enum):
    READ = "READ"
    WRITE = "WRITE"
    ADMIN = "ADMIN"

class CopyUser(Base):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

class Role(Base):
    __tablename__ = 'roles'
    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, nullable=False)

class Permission(Base):
    __tablename__ = 'permissions'
    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)

class RolePermission(Base):
    __tablename__ = 'role_permissions'
    role_id = Column(UUID(as_uuid=True), ForeignKey('roles.id'), primary_key=True)
    permission_id = Column(UUID(as_uuid=True), ForeignKey('permissions.id'), primary_key=True)

class UserRole(Base):
    __tablename__ = 'user_roles'
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True)
    role_id = Column(UUID(as_uuid=True), ForeignKey('roles.id'), primary_key=True)

class CopyDocument(Base):
    __tablename__ = 'documents'
    id = Column(UUID(as_uuid=True), primary_key=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    document_metadata = Column(JSON)
    version = Column(Integer, nullable=False)
    status = Column(Enum(StatusEnum), nullable=False)
    creator_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

class DocumentChunk(Base):
    __tablename__ = 'document_chunks'
    id = Column(UUID(as_uuid=True), primary_key=True)
    document_id = Column(UUID(as_uuid=True), ForeignKey('documents.id'))
    content = Column(Text, nullable=False)
    chunk_index = Column(Integer, nullable=False)
    embedding_id = Column(String)
    chunk_metadata = Column(JSON)

class DocumentTag(Base):
    __tablename__ = 'document_tags'
    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String, nullable=False)

class DocumentVersion(Base):
    __tablename__ = 'document_versions'
    id = Column(UUID(as_uuid=True), primary_key=True)
    document_id = Column(UUID(as_uuid=True), ForeignKey('documents.id'))
    content = Column(Text, nullable=False)
    version_metadata = Column(JSON)
    version = Column(Integer, nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    created_at = Column(DateTime, nullable=False)

class DocumentPermission(Base):
    __tablename__ = 'document_permissions'
    document_id = Column(UUID(as_uuid=True), ForeignKey('documents.id'), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True)
    permission_type = Column(Enum(PermissionTypeEnum), nullable=False)

class CopyChatSession(Base):
    __tablename__ = 'chat_sessions'
    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    title = Column(String)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

class ChatMessage(Base):
    __tablename__ = 'chat_messages'
    id = Column(UUID(as_uuid=True), primary_key=True)
    session_id = Column(UUID(as_uuid=True), ForeignKey('chat_sessions.id'))
    content = Column(Text, nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)
    created_at = Column(DateTime, nullable=False)

class ChatSourceReference(Base):
    __tablename__ = 'chat_source_references'
    message_id = Column(UUID(as_uuid=True), ForeignKey('chat_messages.id'), primary_key=True)
    document_id = Column(UUID(as_uuid=True), ForeignKey('documents.id'))
    chunk_id = Column(UUID(as_uuid=True), ForeignKey('document_chunks.id'))
    relevance_score = Column(Float)

class CopyQueryLog(Base):
    __tablename__ = 'query_logs'
    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    session_id = Column(UUID(as_uuid=True), ForeignKey('chat_sessions.id'))
    query = Column(Text, nullable=False)
    response_id = Column(UUID(as_uuid=True))
    latency_ms = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)

class FeedbackLog(Base):
    __tablename__ = 'feedback_logs'
    id = Column(UUID(as_uuid=True), primary_key=True)
    message_id = Column(UUID(as_uuid=True), ForeignKey('chat_messages.id'))
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    rating = Column(Integer, nullable=False)
    comment = Column(Text)
    created_at = Column(DateTime, nullable=False)
