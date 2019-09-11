"""sqlalchemy-mutable example with nested mutable objects

Instructions:
1. Import from sqlalchemy_mutable
2. Initialize a database column with MutableType
3. Add a query class attribute initialized with scoped_session object
4. Set mutable column to Mutable object
5. Flush or commit models before embedding in a Mutable object
"""

# Import from sqlalchemy_mutable
from sqlalchemy_mutable import MutableListType, Query

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///:memory:')
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
session = Session()
Base = declarative_base()

class MyModel(Base):
    __tablename__ = 'mymodel'
    id = Column(Integer, primary_key=True)
    
    mutable_list = Column(MutableListType) # Initialize with MutableType
    query = Query(Session) # Add a query class attribute
    
    def __init__(self):
        self.mutable_list = [] # Set mutable column to Mutable object


Base.metadata.create_all(engine)
x = MyModel()
y = MyModel()
session.add_all([x,y])

# Flush or commit a model before embedding it in a mutable object
session.flush([x,y])

x.mutable_list.append(y)
session.commit()
print('Mutable list is', x.mutable_list)
print('Successfully recovered y?', x.mutable_list[0] == y)

x.mutable_list.append([])
x.mutable_list[1].append(y)
session.commit()
print('Mutable list is', x.mutable_list)
print('Successfully recovered y?', x.mutable_list[1][0] == y)