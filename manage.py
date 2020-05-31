# -*- coding: utf-8 -*-
import os

from dotenv import load_dotenv

from app import create_app

# Load dotenv in the base root
root_app = os.path.abspath(os.path.dirname(__file__))
dotenv_path = os.path.join(root_app, '.env')
load_dotenv(dotenv_path=dotenv_path, override=True)

app = create_app()
