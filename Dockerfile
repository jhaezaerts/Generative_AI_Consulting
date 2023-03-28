FROM python:3.10-slim
COPY . /Generative AI Consulting/
WORKDIR /Generative AI Consulting/
RUN pip install -r requirements.txt
EXPOSE 80
RUN mkdir ~/.streamlit
RUN cp config.toml ~/.streamlit/config.toml
RUN cp credentials.toml ~/.streamlit/credentials.toml
WORKDIR /Generative AI Consulting/
ENTRYPOINT ["streamlit", "run"]
CMD ["app.py"]