from fastapi import FastAPI

app = FastAPI(title="SkillCommit API", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "SkillCommit API is operational"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}