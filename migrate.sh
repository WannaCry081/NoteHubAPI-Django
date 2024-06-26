echo "Running Database Migrations"
source venv/Scripts/activate

python manage.py makemigrations 
python manage.py migrate

if [ -n "$1" ] && [ $1 == "user" ]; then
    python manage.py createsuperuser
fi

if [ -n "$1" ] && [ "$1" == "run" ]; then 
    python manage.py runserver
fi

deactivate
exec "$@".