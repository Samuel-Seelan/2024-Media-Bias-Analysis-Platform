import json
from collections import Counter
import re
import string
from textblob import TextBlob

# Custom exception for parsing errors
class ParsingException(Exception):
    """Exception raised for errors that occur during parsing."""
    def __init__(self, message="Error occurred during parsing", filename=None, line=None):
        self.message = message
        self.filename = filename
        self.line = line
        super().__init__(self.message)

# Function to preprocess text
def clean_text(text):
    """Convert text to lowercase, remove punctuation, and extra whitespace."""
    text = text.lower().translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Function to analyze sentiment of text
def get_sentiment_score(text):
    """Return the sentiment polarity score of the given text."""
    return TextBlob(text).sentiment.polarity

# Generic parser for plain text files
def generic_parser(filename):
    """Parse a plain text file to count words, average word length, and sentiment."""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            text = clean_text(file.read())
        words = text.split()
        wordcount = Counter(words)
        numwords = len(words)
        avg_word_length = sum(len(word) for word in words) / numwords
        sentiment_score = get_sentiment_score(text)

        return {
            'wordcount': wordcount,
            'numwords': numwords,
            'avg_word_length': avg_word_length,
            'sentiment_score': sentiment_score
        }

    except Exception as e:
        raise ParsingException(f"Error parsing file {filename}: {e}", filename=filename)

# Parser for JSON formatted text files
def json_parser(filename):
    """Parse a JSON text file to count words, average word length, and sentiment."""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
        text = clean_text(data.get('text', ''))  # Safely get the 'text' field
        return generic_parser(text)  # Reuse the generic parser for consistency

    except json.JSONDecodeError as e:
        raise ParsingException(f"Error parsing JSON file {filename}: {e}", filename=filename)
    except Exception as e:
        raise ParsingException(f"Error processing file {filename}: {e}", filename=filename)
