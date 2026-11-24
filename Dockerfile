FROM python:3.14-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN useradd -m -u 1000 user && chown -R user:user /app
USER user
ENV HOME=/home/user
EXPOSE 7860
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=7860", "--browser.gatherUsageStats=false", "--theme.base=light", "--theme.primaryColor=#37644B", "--theme.backgroundColor=#F7F8F6", "--theme.secondaryBackgroundColor=#F0F3EE", "--theme.textColor=#202923"]
