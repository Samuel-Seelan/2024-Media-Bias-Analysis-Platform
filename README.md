# April-2024-Media-Bias-Analysis
Media Based Sentiment Analysis Platform


textastic_app.py - 

This is the main script that processes a series of text files and generates various visualizations to analyze the content. It leverages two primary classes, Textastic and VisualizationGenerator, to handle text processing and visualization, respectively. 


textastic.py - 

This file is designed to load and process textual data from various files, apply preprocessing steps such as removing stop words and punctuation, and then visualize the results using bar charts.


textastic_parsers.py - 

This file is designed for parsing and analyzing text data from both plain text and JSON files. It performs key text-processing tasks such as word counting, calculating average word length, and analyzing sentiment. It also includes error-handling mechanisms for parsing failures.

visualization.py -

This  file is designed to create various visualizations for text analysis, including word clouds, a Sankey diagram, and sentiment analysis.

China/U.S. text files-

These text files are snippets extracted from articles from CCTV, CGTN, China.org, BBC, CNN, and the New York Times about the Chinese and U.S. semiconductor war. 
These files are used as an example to test the platform. Using these text files we can determine the most common words and overall sentiments in order to compare and contrast the bias between the two countries about the Chinese and U.S. semiconductor war. 


stopwords.txt - 

Words in this file are filtered out as these words are common and non-informative.

