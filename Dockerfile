FROM python:3.12.5

WORKDIR /stack-ai/

COPY . .

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

CMD ["fastapi", "run", "src/main.py", "--port", "7777"]