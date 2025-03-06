from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
import shutil
import os

# Initialize FastAPI
app = FastAPI()

# Directory to store uploaded images
UPLOAD_FOLDER = "uploaded_images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create folder if it doesn't exist

# Endpoint to upload an image
@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    # Save the uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename, "url": f"http://127.0.0.1:8000/images/{file.filename}"}

# Endpoint to view the uploaded image
@app.get("/images/{filename}")
async def get_image(filename: str):
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    if os.path.exists(file_path):
        return FileResponse(file_path)
    return JSONResponse(content={"error": "File not found"}, status_code=404)

# Endpoint to list all uploaded images
@app.get("/list-images/")
async def list_uploaded_images():
    files = os.listdir(UPLOAD_FOLDER)
    image_urls = [f"http://127.0.0.1:8000/images/{file}" for file in files]
    return {"uploaded_images": image_urls}

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
