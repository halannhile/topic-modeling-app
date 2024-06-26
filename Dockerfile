FROM python:3.11

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "1_Your_Documents.py"]