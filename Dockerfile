# Container image that runs your code
FROM python:3

# Make a working dir
RUN mkdir /terraform-code

# Copy script
COPY dependagen.py /dependagen.py

# Run it
ENTRYPOINT ["python3", "/dependagen.py"]
