from .database import db
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column

class BaseModel(db.Model):
    """Base class for all models that map to database tables

    Provides common functionality for all models, such as timestamps and serialization and deseralization e.t.c
    Models that inherit from this class will integrate with the ORM and represent a table in the Database.
    Subclasses should define their own fields and relationships using mapped columns.

    Attributes:
        id:int
            primary key
        created_at: datetime
            timestamp when the record was created
        update_at: datetime
            timestamp when the record was last updated 
    """
    # tells sqlAlchemy it should not create a database table for this class
    __abstract__ = True 

    id:Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


    def __init__(self):
        self.created_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)

    def to_dict(self):
        """converts a model instance into a dictionary of its attributes
        
        Returns:
            dict: A dictionary representation of the model with the
        """
        instance_dict = { key: val for (key, val) in self.__dict__.items() if key != '_sa_instance_state'}
        if 'password' in instance_dict:
            instance_dict.pop('password', None)
        return instance_dict
    
    def update_object_from_dict(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)