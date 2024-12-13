from fastapi import FastAPI, File, UploadFile
import cv2
import numpy as np
from mediapipe import solutions

app = FastAPI()

@app.post("/analyze/")
async def analyze_image(file: UploadFile = File(...)):
    image = np.frombuffer(await file.read(), np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    if image is None:
        return {"error": "Não foi possível processar a imagem."}

    with solutions.face_mesh.FaceMesh(static_image_mode=True) as face_mesh:
        results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        if not results.multi_face_landmarks:
            return {"error": "Nenhuma face detectada."}

        landmarks_data = []
        for face_landmarks in results.multi_face_landmarks:
            for landmark in face_landmarks.landmark:
                landmarks_data.append({"x": landmark.x, "y": landmark.y, "z": landmark.z})

        return {"landmarks": landmarks_data}
