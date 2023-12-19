echo Starting DjangoServer...
Start-Process cmd -ArgumentList "/k cd /d D:\code\surfter && venv\Scripts\activate && title DjangoServer && python manage.py runserver"
echo DjangoServer started.

echo Starting CeleryServer...
Start-Process cmd -ArgumentList "/k cd /d D:\code\surfter && venv\Scripts\activate && title CeleryServer && celery -A Surfter worker -P solo --loglevel=DEBUG"
echo CeleryServer started.

echo Starting FlowerServer...
Start-Process cmd -ArgumentList "/k cd /d D:\code\surfter && venv\Scripts\activate && title FlowerServer && celery -A Surfter flower"
echo FlowerServer started.

echo Starting RabbitMQ...
docker run --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.12-management
echo RabbitMQ started.

echo All servers started successfully.
