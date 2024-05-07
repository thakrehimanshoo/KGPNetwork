
pip install -r requirements.txt


if [[ $CREATE_SUPERUSER ]]; then
    python KGPNetwork/manage.py createsuperuser --no-input
fi
