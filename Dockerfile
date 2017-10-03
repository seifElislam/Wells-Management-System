From python:2.7
USER root
RUN mkdir -p /workspace/app/
WORKDIR /workspace/app/
COPY . /workspace/app/
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["python","manage.py", "runserver","0.0.0.0:8000"]