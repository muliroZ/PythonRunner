@echo off
title Instalador - PythonRunner
color 0A

echo =========================================
echo   Configurando o Ambiente do Jogo...
echo =========================================
echo.

echo [1/4] Baixando e instalando o Python 3.12...
winget install --id Python.Python.3.12 --exact --silent --accept-package-agreements --accept-source-agreements

echo.
echo [2/4] Baixando e instalando o gerenciador de pacotes uv...
powershell -ExecutionPolicy ByPass -Command "Invoke-RestMethod https://astral.sh/uv/install.ps1 | Invoke-Expression"

set "PATH=%USERPROFILE%\.cargo\bin;%PATH%"

echo.
echo [3/4] Construindo o ambiente e baixando dependencias do projeto...
uv sync

echo [4/4] Criando o atalho de inicializacao...
echo @echo off > jogar.bat
echo title PythonRunner >> jogar.bat
echo uv run main.py >> jogar.bat

echo.
echo ==========================================
echo   Instalacao concluida com sucesso!
echo ==========================================
echo Um novo arquivo chamado 'jogar.bat' foi gerado nesta pasta.
echo A partir de agora, basta dar um duplo clique nele para iniciar o jogo!
echo.
pause