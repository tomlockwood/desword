python desword/cli.py tests/example/ tmp/ https://${CODESPACE_NAME}-8000.githubpreview.dev/
echo "https://${CODESPACE_NAME}-8000.githubpreview.dev/"
python -m http.server -d tmp/ 8000
