#Configuration & Setup
#We need to make sure the app knows about the new structure.
import os

class Config:
    SECRET_KEY = 'dev-key-secret' # Change this for production
    SQLALCHEMY_DATABASE_URI = 'sqlite:///hospital.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
