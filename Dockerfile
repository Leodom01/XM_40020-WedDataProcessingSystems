FROM karmaresearch/wdps2

WORKDIR /assignment
# Copy the current directory contents into the container at /app
COPY . /assignment

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run app.py when the container launches
CMD ["python", "interactiveDemo.py"]