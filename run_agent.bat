@echo off
ECHO ===============================================
ECHO INICIANDO O AGENTE DE NOTICIAS...
ECHO HORA: %TIME%
ECHO DATA: %DATE%
ECHO ===============================================

REM Este comando garante que o script rode a partir da pasta correta.
cd /d "%~dp0"

REM --- CONFIGURE AQUI ---
REM Verifique se este caminho para o Python "de verdade" esta 100% correto!
set PYTHON_EXE_PATH="C:\Users\Whinicius\AppData\Local\Programs\Python\Python313\python.exe"

REM Nome do script que queremos executar.
set SCRIPT_TO_RUN="main.py"
REM --------------------

ECHO.
ECHO Executando o script Python agora...
ECHO Comando a ser executado: %PYTHON_EXE_PATH% %SCRIPT_TO_RUN%
ECHO.

REM Executa o script e salva a saida normal em 'log_output.txt' e os erros em 'log_erros.txt'.
%PYTHON_EXE_PATH% %SCRIPT_TO_RUN% > log_output.txt 2> log_erros.txt

ECHO.
ECHO ===============================================
ECHO EXECUCAO CONCLUIDA.
ECHO Verifique os arquivos log_output.txt e log_erros.txt para detalhes.
ECHO.
ECHO Pressione qualquer tecla para fechar esta janela...
ECHO ===============================================
PAUSE