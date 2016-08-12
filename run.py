# -*- coding: utf-8 -*-
#!./venv/Scripts/python.exe run.py
#  alias r='./venv/Scripts/python.exe run.py'
#  .\venv\Scripts\activate
from app import app
if __name__=='__main__':
	app.run(debug=True,host='0.0.0.0')