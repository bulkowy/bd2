rm app/migrations/000*
./manage.py makemigrations
./manage.py migrate
echo "from django.contrib.auth.models import User;User.objects.create_superuser('admin','ad@ad.ad','inside97')" | ./manage.py shell
./manage.py loaddata init.json
