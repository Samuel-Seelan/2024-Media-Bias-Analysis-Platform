import os
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from textblob import TextBlob
import plotly.graph_objects as go

# Class to generate visualizations for text analysis
class VisualizationGenerator:
    def __init__(self, data, labels, file_paths):
        # Data dictionary containing word counts and other stats
        self.data = data
        # Dictionary mapping file paths to labels
        self.labels = labels
        # List of file paths to process
        self.file_paths = file_paths
        # Figure dimensions based on the number of files
        self.dimensions = (1, len(file_paths))

    # Method to get sentiment score for a given text
    def get_sentiment_score(self, text):
        # Using TextBlob to determine sentiment polarity
        return TextBlob(text).sentiment.polarity

    # Custom color function for the word cloud
    def color_func(self, word, **kwargs):
        # Get sentiment of word and color it based on sentiment
        sentiment = TextBlob(word).sentiment.polarity
        if sentiment > 0:
            return "yellow"  # Positive sentiment
        elif sentiment < 0:
            return "red"    # Negative sentiment
        else:
            return "#90ee90"  # Neutral sentiment (light green for better contrast)

    # Method to generate word clouds for each document
    def generate_word_clouds(self):
        fig, axs = plt.subplots(*self.dimensions, figsize=(15, 10))
        axs = axs.ravel()  # Flatten the axes array for easy iteration

        for i, file_path in enumerate(self.file_paths):
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            # Generate word cloud with custom color mapping
            wordcloud = WordCloud(width=400, height=300, background_color='white',
                                  max_font_size=60, color_func=self.color_func).generate(text)
            axs[i].imshow(wordcloud, interpolation='bilinear')
            axs[i].set_title(os.path.basename(file_path))
            axs[i].axis('off')  # Hide axes for better visualization

        fig.suptitle("Word Clouds for Text Documents", fontsize=16)
        plt.tight_layout()
        plt.show()

    # Method to generate a Sankey diagram
    def generate_sankey_diagram(self):
        node_labels = []
        source = []
        target = []
        values = []

        # Prepare data for Sankey diagram
        for file_path in self.file_paths:
            text_label = self.labels[file_path]
            node_labels.append(text_label)
            # Extract the most common words and their counts
            words = self.data[text_label]['wordcount'].most_common(n=8)
            for word, count in words:
                if word not in node_labels:
                    node_labels.append(word)
                source.append(node_labels.index(text_label))
                target.append(node_labels.index(word))
                values.append(count)

        # Create and show the Sankey diagram
        fig = go.Figure(data=[go.Sankey(
            node=dict(pad=15, thickness=20, line=dict(color='black', width=0.5), label=node_labels),
            link=dict(source=source, target=target, value=values)
        )])
        fig.update_layout(title_text='Text-to-Word Sankey Diagram', font_size=17)
        fig.show()

    # Method to generate sentiment analysis visualization
    def generate_sentiment_analysis(self):
        sentiment_scores = []
        # Calculate sentiment scores for each file
        for file_path in self.file_paths:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                score = self.get_sentiment_score(text)
                sentiment_scores.append(score)
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")
                sentiment_scores.append(0)  # Default score for errors

        # Normalize sentiment scores for color mapping and create scatter plot
        plt.style.use('Solarize_Light2')
        fig, ax = plt.subplots(figsize=(10, 6))
        scatter = ax.scatter(range(len(self.file_paths)), sentiment_scores, c=sentiment_scores,
                             cmap='RdYlGn', s=[abs(score) * 500 for score in sentiment_scores],
                             alpha=0.7, edgecolors='black')
        ax.set_xticks(range(len(self.file_paths)))
        ax.set_xticklabels([os.path.basename(fp) for fp in self.file_paths], rotation=45)
        ax.set_xlabel('Text Files')
        ax.set_ylabel('Sentiment Score')
        ax.set_title('Sentiment Analysis of Text Files')
        cbar = plt.colorbar(scatter, ax=ax, label='Sentiment Score')
        plt.tight_layout()
        plt.show()