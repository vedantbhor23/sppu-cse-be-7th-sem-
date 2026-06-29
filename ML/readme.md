# Titanic Survival Prediction System

## Overview

This project predicts whether a passenger survived the Titanic disaster using a Machine Learning model. The trained Random Forest model is integrated into a graphical user interface for real-time predictions.

## Features

- Random Forest Classification
- Model Training
- GUI Prediction Interface
- Pre-trained Model Loading
- User Input Validation

## Technologies Used

- Python
- Scikit-learn
- Pandas
- NumPy
- Tkinter
- Joblib

## Project Structure

```
ML/
│
├── Train_model.py
├── Titanic_app.py
├── titanic_model.pkl
├── train.csv
├── requirements.txt
└── README.md
```

## Installation

```bash
pip install -r requirements.txt
```

## Train Model

```bash
python Train_model.py
```

## Run Application

```bash
python Titanic_app.py
```

## Dataset

Titanic Passenger Dataset

Features include:

- Passenger Class
- Gender
- Age
- Fare
- Number of Siblings/Spouses
- Number of Parents/Children
- Embarked Port

## Future Enhancements

- Multiple ML models
- Accuracy comparison
- Web application deployment
- Explainable AI integration