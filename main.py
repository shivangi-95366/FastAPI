from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base

# Initialize FastAPI app
app = FastAPI()

# Setup SQLite connection
engine = create_engine("sqlite:///ocr_data.db")
Session = sessionmaker(bind=engine)
Base = declarative_base()

# Define the table schema
class OCRSummary(Base):
    __tablename__ = 'ocr_summaries'
    id = Column(Integer, primary_key=True)
    image = Column(String(255), nullable=False)
    cleaned_text = Column(Text)
    summary_bart = Column(Text)
    summary_t5 = Column(Text)

# API route: Get summary by image file name
@app.get("/summary/{filename}")
def get_summary(filename: str):
    session = Session()
    result = session.query(OCRSummary).filter(OCRSummary.image == filename).first()
    session.close()

    if not result:
        raise HTTPException(status_code=404, detail="Image not found")

    return {
        "image": result.image,
        "cleaned_text": result.cleaned_text,
        "summary_bart": result.summary_bart,
        "summary_t5": result.summary_t5
    }
