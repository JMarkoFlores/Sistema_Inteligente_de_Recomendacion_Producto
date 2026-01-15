"""Ejecutar con: streamlit run run.py"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if os.path.exists('app.py'):
    import app
else:
    from app.main import main
    main()