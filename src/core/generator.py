from typing import List, Dict
from src.core.aggregator import NewsAggregator
from src.core.llm import LLMWrapper

class PostGenerator:
    def __init__(self):
        self.aggregator = NewsAggregator()
        self.llm = LLMWrapper()
    
    async def generate_posts(
        self,
        sources: List[str],
        platforms: List[str]
    ) -> Dict[str, str]:
        """
        Generate social media posts for multiple platforms
        
        Args:
            sources: List of news sources
            platforms: List of target platforms (e.g., ['linkedin', 'twitter'])
            
        Returns:
            Dict mapping platform to generated post content
        """
        # Fetch news items
        news_items = await self.aggregator.fetch_news(sources)
        
        # Generate posts for each platform
        posts = {}
        for platform in platforms:
            post_content = await self.llm.generate_post(news_items, platform)
            posts[platform] = post_content
        
        return posts
    
    def validate_post(self, post: str, platform: str) -> bool:
        """
        Validate post content for platform-specific requirements
        
        Args:
            post: Generated post content
            platform: Target platform
            
        Returns:
            bool: Whether post meets platform requirements
        """
        if platform == 'twitter':
            # Check Twitter character limit
            return len(post) <= 280
        
        elif platform == 'linkedin':
            # Check LinkedIn character limit
            return len(post) <= 3000
        
        return True 