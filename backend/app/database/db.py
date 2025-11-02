"""
Database connection setup for SQL Server
Auto-retry với 2 options: SQLEXPRESS và default instance
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

# Database credentials từ .env
DB_USER = os.getenv("DB_USER", "sa")
DB_PASSWORD = os.getenv("DB_PASSWORD", "12345")
DB_NAME = os.getenv("DB_NAME", "Hackathon")

# SQL Server connection strings (thử 2 options)
CONNECTION_STRINGS = [
    # Option 1: SQLEXPRESS instance (thường dùng)
    f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@localhost\\SQLEXPRESS/{DB_NAME}?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes",
    # Option 2: Default instance
    f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@localhost/{DB_NAME}?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes",
    # Option 3: Thử với driver cũ hơn
    f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@localhost\\SQLEXPRESS/{DB_NAME}?driver=SQL+Server&TrustServerCertificate=yes",
    f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@localhost/{DB_NAME}?driver=SQL+Server&TrustServerCertificate=yes",
]

engine = None
SessionLocal = None


def get_engine():
    """Get or create database engine with auto-retry"""
    global engine, SessionLocal
    
    if engine is not None:
        return engine
    
    # Thử từng connection string
    for conn_str in CONNECTION_STRINGS:
        try:
            engine = create_engine(
                conn_str,
                pool_pre_ping=True,  # Auto reconnect
                pool_size=5,
                max_overflow=10,
                echo=False  # Set True để debug SQL queries
            )
            
            # Test connection
            with engine.connect() as conn:
                conn.execute("SELECT 1")
            
            print(f"✅ Database connected successfully!")
            print(f"Connection string: {conn_str.split('@')[0]}@...")
            
            # Create session factory
            SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
            
            return engine
            
        except Exception as e:
            print(f"❌ Connection failed with: {conn_str.split('@')[0]}@...")
            print(f"   Error: {str(e)}")
            continue
    
    # Nếu tất cả đều fail
    raise Exception(
        "Cannot connect to SQL Server. Please check:\n"
        "1. SQL Server is running\n"
        "2. Database 'Hackathon' exists\n"
        "3. User 'sa' has permission\n"
        "4. SQL Server authentication is enabled"
    )


def get_db():
    """Dependency để lấy database session"""
    engine = get_engine()
    if SessionLocal is None:
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database - tạo tables nếu chưa có"""
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created/verified")

