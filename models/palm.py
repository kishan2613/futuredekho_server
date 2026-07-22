from sqlalchemy import Column,Integer,String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from database import Base

class Palm(Base):
    __tablename__ = "palms"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    image_url = Column(String)

    palm_data = Column(
        JSONB,
        nullable=False
    )