from scraper import AIScraper

def main():
    # Initialize the scraper
    scraper = AIScraper()
    
    # Example natural language search query
    search_query = "tech startups in Stockholm, Sweden"
    
    # Define your AI analysis prompt
    ai_prompt = """
    Please analyze this content and identify:
    1. The type of business or organization
    2. Key contact persons and their roles
    3. Job opportunities and requirements
    4. Company culture and values
    5. Contact information and application process
    
    Format your response in text format using markdown formatting.
    """
    
    print(f"\nSearching for: {search_query}")
    print("This will search the web and analyze the top 5 results...")
    
    # Perform the search and analysis
    results_df = scraper.search_and_analyze(search_query, ai_prompt, max_results=5)
    
    # Display results
    if not results_df.empty:
        print("\nAnalysis Results:")
        for _, row in results_df.iterrows():
            print(f"\nURL: {row['url']}")
            print(f"Emails found: {row['emails']}")
            print(f"Analysis:\n{row['ai_analysis']}")
            print("-" * 80)
    else:
        print("No results found.")

if __name__ == "__main__":
    main() 