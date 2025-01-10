FROM python:3.10-slim

# Create a non-root user with UID 1000
RUN useradd -m -u 1000 user

# Switch to the new user
USER user

# Set the working directory to the user's home directory
WORKDIR /home/user/app

RUN sudo apt install gcc-11
RUN sudo apt install g++-11
# Copy requirements first to leverage Docker cache
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY --chown=user . .

# Expose the port the app runs on
EXPOSE 7860

# Ensure the PATH includes the user's local bin
ENV PATH=/home/user/.local/bin:$PATH

# Command to run the application using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
