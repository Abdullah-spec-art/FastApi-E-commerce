from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://127.0.0.1:3000",  # React frontend
    "http://localhost:3000"   # React frontend alternate
]

def add_cors_middleware(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,  # React frontend
        allow_credentials=True,
        allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
        allow_headers=["*"],  # Allow all headers
    )
