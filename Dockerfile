FROM python:3.13.3

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV SERVICE_NAME=catalog-service
ENV PORT=5000

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Fixed missing spaces in useradd
RUN useradd --create-home --shell /usr/sbin/nologin appuser

# Fixed missing space after COPY
COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 5000

# Fixed missing spaces in waitress flags
CMD ["sh", "-c", "exec waitress-serve --host=0.0.0.0 --port=${PORT:-5000} app:app"]