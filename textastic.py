
import matplotlib.pyplot as plt
import json
from collections import Counter, defaultdict
import string
import re
from textastic_parsers import generic_parser, ParsingException

# Main class that will handle text analysis.
class Textastic:

    def __init__(self):
        # Initialize the data dictionary to store analysis results for word count, total words, and average word length.
        self.data = {'wordcount': {}, 'numwords': {}, 'avg_word_length': {}}
        # Initialize stop words and labels dictionaries for later use.
        self.stop_words = set()
        self.labels = {}

    @staticmethod
    def clean_text(text):
        """Preprocess text: lowercase, remove punctuation, and extra whitespace."""
        text = text.lower().translate(str.maketrans('', '', string.punctuation))
        text = re.sub(r'\s+', ' ', text).strip()  
        return text

    def _default_parser(self, filename):
        """ A default text parser to process simple unformatted text files, now filters stop words."""
        with open(filename, 'r', encoding='utf-8') as file:  # Specify UTF-8 encoding for file handling
            text = self.clean_text(file.read())  # Clean the text
            # Tokenize the text and exclude stop words
            words = [word for word in text.split() if word not in self.stop_words]
            wordcount = Counter(words)  # Count the occurrences of each word
            numwords = len(words)  # Count the total number of words
            avg_word_length = sum(len(word) for word in words) / numwords if numwords > 0 else 0  

        
        return {
            'wordcount': wordcount,
            'numwords': numwords,
            'avg_word_length': avg_word_length,
        }

    def load_stop_words(self, stopfile):
        """Load a list of stop words from a file."""
        with open(stopfile, 'r') as file:
            # Clean and load stop words as a set for faster lookup
            self.stop_words = set(self.clean_text(file.read()).split())

    def load_text(self, filename, label=None, parser=None):
        """Load and analyze text, using the specified or default parser."""
        if label is None:
            label = os.path.basename(filename)  # Use filename as label if not provided
        self.labels[filename] = label
        if parser is None:
            parser = self._default_parser  # Use the default parser if none is specified
        try:
            # Parse the text and store the results
            results = parser(filename)
            if label not in self.data:
                self.data[label] = {'wordcount': {}, 'numwords': 0, 'avg_word_length': 0}
            self.data[label]['wordcount'] = results['wordcount']
            self.data[label]['numwords'] = results['numwords']
            self.data[label]['avg_word_length'] = results['avg_word_length']
        except ParsingException as e:
            print(f"Error loading file {filename}: {e}")  # Handle any parsing errors

    def compare_num_words(self):
        """Visualize the number of words in each text file using a bar chart."""
        labels = list(self.data['numwords'].keys())  # Extract the labels (text file names)
        values = [self.data['numwords'][label] for label in labels]  # Extract the corresponding word counts

        # Create a bar plot comparing the number of words across text files
        plt.figure(figsize=(10, 6))
        plt.bar(labels, values)
        plt.xlabel('Texts')
        plt.ylabel('Number of Words')
        plt.title('Number of Words in Each Text File')
        plt.xticks(rotation=45)
        plt.tight_layout()  
        plt.show()
