release: python manage.py migrate --no-input && python manage.py importar_dados_iniciais
web: gunicorn divprom.wsgi --log-file -