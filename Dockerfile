# Use the Python 3.9 image
FROM python:3.9-slim-buster



# Set the working directory to /Ezshop/TypingAssistant
WORKDIR /Ezshop/ctas

# Copy the current directory contents into the container at /Ezshop/ctas
COPY requirements.txt requirements.txt 

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0


#Pip command without proxy setting

RUN pip install -r requirements.txt

# Expose port 4030
EXPOSE 4030

COPY . .

CMD ["python","app.py","flask"]