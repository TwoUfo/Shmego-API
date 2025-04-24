import os

from dotenv import load_dotenv
from waitress import serve

from app import create_app

load_dotenv()
host = os.getenv("HOST")
port = os.getenv("PORT")

app = create_app()

if __name__ == "__main__":
    serve(app, host=host, port=port)
