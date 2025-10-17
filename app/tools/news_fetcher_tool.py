class NewsFetcherTool:
    def run(self, topic: str) -> str:
        """
        Returns a static news article for testing purposes.
        """
        print(f"--- MOCKED: Fetching news about '{topic}' ---")
        return """
        New York, NY - In a surprising turn of events, tech giant InnovateCorp 
        announced today the release of its groundbreaking new product, the 'Quantum Leap' processor. 
        CEO Jane Doe claims this technology will revolutionize the computing industry.
        """
