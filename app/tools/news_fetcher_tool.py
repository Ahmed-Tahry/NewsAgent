from newsapi import NewsApiClient
from config import NEWS_API_KEY

class NewsFetcherTool:
    def __init__(self):
        """
        Initializes the News Fetcher Tool with the NewsAPI client.
        """
        if NEWS_API_KEY == "YOUR_NEWS_API_KEY_HERE" or not NEWS_API_KEY:
            print("WARNING: NewsAPI key not found. Please set it in config.py.")
            self.api_client = None
        else:
            self.api_client = NewsApiClient(api_key=NEWS_API_KEY)
        print("NewsFetcherTool initialized.")

    def run(self, topic: str) -> str:
        """
        Fetches the top news article on a given topic from NewsAPI.

        Args:
            topic (str): The topic to search for news articles.

        Returns:
            str: The content of the top news article, or an error message.
        """
        if not self.api_client:
            return "Error: NewsAPI client is not configured. Please add your API key to config.py."

        try:
            # Fetch top headlines for the topic
            top_headlines = self.api_client.get_top_headlines(
                q=topic,
                language='en'
            )
            
            if top_headlines['status'] == 'ok' and top_headlines['articles']:
                # Return the content of the first article
                first_article = top_headlines['articles'][0]
                title = first_article.get('title', 'No Title')
                content = first_article.get('content', 'No content available.')
                return f"Title: {title}\n\n{content}"
            else:
                return f"Could not find any top news articles for '{topic}'."

        except Exception as e:
            return f"An error occurred while fetching news: {e}"
