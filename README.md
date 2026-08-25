# Customer Review Intelligence System

A **Streamlit-based Customer Review Intelligence System** that analyzes customer reviews and classifies them into **Positive, Neutral, or Negative** sentiment. The application helps users understand customer feedback quickly through automated sentiment analysis.

## Features

* Analyze individual customer reviews
* Upload and analyze reviews using a CSV file
* Classify reviews into:

  * Positive
  * Neutral
  * Negative
* Display sentiment results clearly
* View analyzed reviews in a dataframe
* Simple and user-friendly Streamlit interface
* Automatically process multiple customer reviews

## Technologies Used

* **Python** – Application development
* **Streamlit** – Web application interface
* **Pandas** – Data processing and CSV handling
* **TextBlob** – Sentiment analysis

## How It Works

1. The user enters customer reviews or uploads a CSV file.
2. The application processes the review text.
3. TextBlob calculates the sentiment polarity.
4. The system classifies each review as Positive, Neutral, or Negative.
5. The analyzed results are displayed in the application.

## Project Structure

```text
review-intelligence-system/
│
├── app.py
├── requirements.txt
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/review-intelligence-system.git
```

Move into the project folder:

```bash
cd review-intelligence-system
```

Install the required libraries:

```bash
pip install -r requirements.txt
```

## Run the Application

Start the Streamlit application using:

```bash
streamlit run app.py
```

The application will open in your browser.

## Requirements

The `requirements.txt` file contains the required Python libraries:

```text
streamlit
pandas
textblob
```

## Example Use Cases

This system can be used for:

* Customer feedback analysis
* Product review analysis
* Service quality analysis
* Identifying positive and negative customer experiences
* Understanding overall customer sentiment

## Future Improvements

* Add interactive sentiment charts and visualizations
* Use advanced NLP or machine learning models for improved sentiment accuracy
* Add keyword and topic analysis
* Add review filtering and search functionality
* Add overall sentiment summary and insights
* Support more advanced customer feedback analytics

## Project Goal

The goal of this project is to demonstrate how **Python, Natural Language Processing (NLP), and Streamlit** can be combined to build a simple customer review analysis application.

## Author

**Harini Gobinathan**

B.Tech Student | Aspiring Data Analyst
