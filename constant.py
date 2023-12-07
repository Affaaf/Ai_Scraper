
class Const:    
   
    PROMPT_TEMPLATE_TEXT = '''
    
    Objective: Extract relevant data against HTML content delimited by triple backticks.

    Data Format
    The output should be in JSON format with the following structure and keys:
    {
        "title": "The accurately extracted title of the page",
        "h1_headings": ["List of accurately extracted H1 headings"],
        "h2_headings": ["List of accurately extracted H2 headings"],
        "anchor_tags_data": [
            "href": "Accurate URL",
            "href": "Accurate URL",
            ...
        ]
    }
    
    Guidelines: 
    - Ensure precise extraction of text content from the title tag.
    - Accurately extract text content from h1 heading and h2 heading.
    - Enhance the accuracy of extracting content from href attributes in anchor ('a') tags. 
    - Do not return tags like (<a href="https://www.w3schools.com/html/">Visit our HTML tutorial</a>), return only the content from the mentioned tags.
    - Avoid returning HTML code; provide only the required data from tags.
    - Do not write and return any code in your response,you are expected to only give json response against relevant key value pairs. 
    - If there is no relevant data for a particular key (e.g., no H1 headings or no anchor tags), simply return "NOT FOUND" against the relavent key.

    
    Very Important Note: Do not return above provided sample Data format in your response; it is provided only for instructional purposes.

    Focus solely on extracting the mentioned data elements accurately and avoid including responsed not mentioned in the HTML file. Ensure each placeholder in the output is enclosed in open and close parentheses.
    '''  
    JSON_FILENAME = "scraped_file.json"
    LOGGER_FILENAME = "error.log"
    JSON_ERROR = "JSON decoding error:"
