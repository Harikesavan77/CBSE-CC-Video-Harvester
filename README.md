# CBSE-CC-Video-Harvester

A Python script that fetches YouTube videos licensed under Creative Commons (CC BY) for CBSE curriculum subjects History and Geography across Grades 6 to 10, and exports the results as both a CSV and Excel file.

# Approach
The script uses the YouTube Data API v3 to programmatically search for and verify CC-licensed educational videos. Rather than manually browsing YouTube, the entire discovery and verification process is automated — querying the API, filtering by license, deduplicating results, and writing structured output files.
The API key is kept out of the codebase using a .env file loaded via python-dotenv, making the project safe to share publicly.

# How Videos Were Discovered
For each combination of grade (6–10) and subject (History, Geography), the script submits a search query in the format "CBSE Class {grade} {subject}" to the YouTube Data API v3 search.list endpoint. The videoLicense=creativeCommon parameter is passed directly in the API call to pre-filter results to Creative Commons videos only, returning up to 50 results per query — the maximum the API allows in a single call.
This produces 10 queries in total (5 grades × 2 subjects), each costing 100 API quota units, for a total of approximately 1,010 units — well within the 10,000 unit daily limit.

# How Licenses Were Verified
The videoLicense=creativeCommon filter in the search call provides an initial filter, but this alone is not treated as sufficient. For every video returned by the search, the script makes a secondary call to the videos.list endpoint to fetch the full video metadata and explicitly checks that video["status"]["license"] == "creativeCommon" before including it in the dataset. This two-step approach ensures no incorrectly licensed video is included in the output.
A seen_ids set is maintained throughout the run to deduplicate videos that may appear across multiple queries.

# Output
The script produces two files:

* cbse_cc_videos.csv — UTF-8 encoded CSV with columns: Grade, Subject, Video Title, Video Link, License
* cbse_cc_videos.xlsx — Excel version of the same dataset

# How to Run

* pip install google-api-python-client pandas openpyxl python-dotenv

* Create a .env file in the project folder:
  YOUTUBE_API_KEY=your_api_key_here

* bash python app.py
