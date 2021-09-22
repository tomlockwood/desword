python desword/main.py tests/example/ tests/tmp/ https://${CODESPACE_NAME}-8000.githubpreview.dev/
echo "https://${CODESPACE_NAME}-8000.githubpreview.dev/"
python -m http.server -d tests/tmp/ 8000
