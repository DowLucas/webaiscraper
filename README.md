# AI-Powered Web Scraping Tool

A Python-based web scraping tool that leverages AI (ChatGPT) to extract email addresses and identify potential clients based on input prompts.

## Features

- Automated web scraping with rate limiting and user agent rotation
- Email address extraction using regex patterns
- AI-powered content analysis using OpenAI's GPT-3.5
- Bulk scraping capabilities with progress tracking
- Results export to CSV
- Configurable through environment variables

## Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Internet connection

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
   Edit the `.env` file and add your OpenAI API key and other configurations.

## Configuration

The following environment variables can be configured in the `.env` file:

- `OPENAI_API_KEY`: Your OpenAI API key
- `MAX_REQUESTS_PER_SECOND`: Rate limit for web requests (default: 2)
- `TIMEOUT_SECONDS`: Request timeout in seconds (default: 30)
- `OUTPUT_DIR`: Directory for saving results (default: output)
- `CSV_FILENAME`: Name of the output CSV file (default: scraped_data.csv)

## Usage

1. Basic usage with example script:

   ```bash
   python example.py
   ```

2. Using the scraper in your own code:

   ```python
   from scraper import AIScraper

   # Initialize scraper
   scraper = AIScraper()

   # Define URLs to scrape
   urls = ["https://example.com/contact"]

   # Define AI analysis prompt
   prompt = """
   Please analyze this content and identify:
   1. The type of business
   2. Key contact persons
   3. Business opportunities
   4. Content tone and professionalism
   """

   # Perform scraping
   results = scraper.bulk_scrape(urls, prompt)
   ```

## Ethical Considerations

- Always check and respect websites' robots.txt files
- Follow rate limiting best practices
- Ensure compliance with websites' terms of service
- Handle personal data in accordance with privacy laws (GDPR, CCPA)
- Obtain necessary permissions before scraping private content

## Error Handling

The scraper includes built-in error handling for:

- Failed HTTP requests
- Rate limiting
- Timeout issues
- API errors
- Invalid URLs

## Output Format

The scraper outputs a CSV file containing:

- URL
- Extracted email addresses
- AI analysis results
- Success/failure status

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is for educational purposes only. Users are responsible for ensuring their use of the tool complies with applicable laws and website terms of service.
