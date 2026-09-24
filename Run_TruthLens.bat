@echo off
title TruthLens: AI News Credibility Scorer
echo ============================================================================
echo           TRUTHLENS: REAL-TIME NEWS CREDIBILITY VERIFICATION
echo                  50%% Project Milestone Web Application
echo ============================================================================
echo.
echo [*] Launching Streamlit Web Dashboard...
echo [*] Opening in your web browser: http://localhost:8501
echo.
cd /d "%~dp0"
python -m streamlit run app.py
pause
