"""
Database connection setup for SQL Server
Auto-retry với 2 options: SQLEXPRESS và default instance
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from app.utils.logger import logger

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
            from sqlalchemy import text
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            # Create session factory
            SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
            logger.info("Database connected successfully!")
            
            return engine
            
        except Exception as e:
            # Log warning nhưng tiếp tục thử connection string tiếp theo
            logger.debug(f"Connection attempt failed: {str(e)[:100]}")
            continue
    
    # Nếu tất cả đều fail - return None thay vì raise exception
    # Server vẫn chạy được, chỉ history features không hoạt động
    logger.warning("All database connection attempts failed. History features will be disabled.")
    return None


def get_db():
    """Dependency để lấy database session"""
    engine = get_engine()
    if engine is None or SessionLocal is None:
        # Nếu không có DB, raise HTTPException
        from fastapi import HTTPException
        raise HTTPException(
            status_code=503,
            detail="Database not available. Please check SQL Server connection."
        )
    
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
    if engine is None:
        return  # Không có DB, skip initialization
    
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created/verified")
    except Exception as e:
        # Log error nhưng không fail
        logger.warning(f"Failed to create database tables: {str(e)}")

