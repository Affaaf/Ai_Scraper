# HTML Scraping with OpenAI

This script utilizes the OpenAI API to extract relevant data from HTML content. The extracted data includes H1 and H2 headings, the title, and URLs from anchor tags. The scraped data is then saved to a JSON file.


## Prerequisites

- Python 3.x
- Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/your-repository.git
    cd your-repository
    ```

2. Create a virtual environment:

    ```bash
    python -m venv venv
    ```

3. Activate the virtual environment:

    - On Windows:

        ```bash
        venv\Scripts\activate
        ```

    - On macOS/Linux:

        ```bash
        source venv/bin/activate
        ```

4. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

5. Create a `.env` file and add your OpenAI API keys:

    ```env
    SECRET_KEY=your-secret-key
    ORG_KEY=your-organization-key
    ```

## Usage

Run the script from the command line, providing the target URL as an argument:

```bash
python main.py --url https://www.example.com
