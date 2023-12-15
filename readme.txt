Surfter:
Use AI to analyze user generated query results for accuracy, bias, motivation and logic, then produce a webpage with delightful and easily consumable Hyperanalysis and infographics.

One must create a virtural environment and install the required modules in requirements.txt
Then use these equiv HAX to make your hurt less:
DjangoServer:
Start-Process cmd -ArgumentList "/k cd /d D:\code\surfter && venv\Scripts\activate && title DjangoServer && python manage.py runserver"
RabbitMQ:
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.12-management
Celery:
Start-Process cmd -ArgumentList "/k cd /d D:\code\surfter && venv\Scripts\activate && title CeleryServer && celery -A Surfter worker -P solo --loglevel=DEBUG"
Flower:
Start-Process cmd -ArgumentList "/k cd /d D:\code\surfter && venv\Scripts\activate && title FlowerServer && celery -A Surfter flower"
Goto localhost, 127.0.0.1:8000
Surft



TODO: Create a tierd user layer with modest ad content for free members, with top teir able to send custom queries up the stack. --- In Progress

TODO: Do another AI summary of the summeries for the infographic and hyperanalysis. 

TODO: Create logic that removes gpt request for articles that fail souptext. Either keep image or step over before rendering.

TODO: If HTML filename exists in the archive, need to evaluate then stomp or skip 

Examples:
laion 5b, ground news, metacritic, Anthropic AI.

Milestones have been stubbed out:
https://github.com/BlueSpike20/Surfter/milestones

