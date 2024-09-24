

from textastic import Textastic
from visualization import VisualizationGenerator


def main():
    # Instantiate the Textastic class for text processing
    tt = Textastic()
    # Load a set of common stopwords
    tt.load_stop_words('stopwords.txt')

    # Define your list of file paths
    file_paths = [
        'China 1.txt',
        'China 2.txt',
        'China 3.txt',
        'US 1.txt',
        'US 2.txt',
        'US 3.txt'
    ]

    # Load multiple text files into the system and assign each a label
    labels = [
        'Article 1 - China',
        'Article 2 - China',
        'Article 3 - China',
        'Article 1 - U.S',
        'Article 2 - U.S',
        'Article 3 - U.S'
    ]

    for filepath, label in zip(file_paths, labels):
        tt.load_text(filepath, label)

    # Now, print out the processed information for each file
    for label in labels:
        print(f"{label}:")
        print(f"Word Count: {tt.data[label]['wordcount']}")
        print(f"Number of Words: {tt.data[label]['numwords']}")
        print(f"Average Word Length: {tt.data[label]['avg_word_length']}\n")

    # Instantiate the VisualizationGenerator with the loaded data
    visualization_generator = VisualizationGenerator(tt.data, tt.labels, file_paths)
    # Generate a Sankey diagram based on the loaded data
    visualization_generator.generate_sankey_diagram()
    # Perform sentiment analysis on the text data and visualize it
    visualization_generator.generate_sentiment_analysis()
    # Generate word clouds for each of the loaded text files
    visualization_generator.generate_word_clouds()



if __name__ == '__main__':
    main()
