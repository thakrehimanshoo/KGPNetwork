
pip install -r requirements.txt


if [[ $CREATE_SUPERUSER ]]; then
    python manage.py createsuperuser --no-input
fi
