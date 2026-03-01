#!/usr/bin/env bash

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Installing spaCy model..."
python -m spacy download en_core_web_sm

echo "Running Django setup..."
python manage.py collectstatic --noinput
python manage.py migrate