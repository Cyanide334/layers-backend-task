from typing import List
import re
import random

def generate_tags(title: str, brand: str) -> List[str]:
    """
    Generate tags from the title, excluding the brand name.
    Args:
        title: The product title
        brand: The brand name
    Returns:
        List of tags derived from the title
    """
    # Convert to lowercase and remove special characters
    clean_title = re.sub(r'[^\w\s]', '', title.lower())
    clean_brand = re.sub(r'[^\w\s]', '', brand.lower())
    
    # Split into words
    title_words = clean_title.split()
    brand_words = clean_brand.split()
    
    # Remove brand words from title words
    tags = [word for word in title_words if word not in brand_words]
    
    # Remove duplicates while preserving order
    unique_tags = []
    for tag in tags:
        if tag not in unique_tags:
            unique_tags.append(tag)
    
    return unique_tags

def generate_category_id(last_tag: str) -> int:
    """
    Generate a category ID based on the last tag.
    Args:
        last_tag: The last tag from the product's tags
    Returns:
        A category ID between 0 and 999
    """
    # Use the hash of the last tag to generate a consistent category ID
    return abs(hash(last_tag)) % 1000

def generate_mock_price(brand: str, tags: List[str]) -> float:
    """
    Generate a mock price based on brand, tags, and number of tags.
    Args:
        brand: The brand name
        tags: List of product tags
    Returns:
        A price calculated using the following weights:
        - 30% brand score (1-10)
        - 60% last tag score (1-10)
        - 10% number of tags
    """
    if not tags:
        return 9.99  # Default price if no tags

    # Set random seed based on brand for consistent scoring
    random.seed(hash(brand))
    
    # Generate brand score (1-10)
    brand_score = random.randint(1, 10)
    
    # Generate last tag score (1-10)
    random.seed(hash(tags[-1]))
    last_tag_score = random.randint(1, 10)
    
    # Number of tags score (1-10, capped at 10)
    num_tags_score = min(len(tags), 10)
    
    # Calculate weighted score (all in cents)
    base_price = 999  # $9.99 in cents
    weighted_score = (
        (brand_score * 30) +      # 30% weight
        (last_tag_score * 60) +   # 60% weight
        (num_tags_score * 10)     # 10% weight
    )
    
    # Calculate final price
    final_price = base_price + weighted_score
    
    # Reset random seed
    random.seed()
    
    # Return price in dollars
    return round(final_price / 100, 2) 