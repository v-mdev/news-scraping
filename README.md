# News Orchestration
This project manages and automates news data workflows. It collects news article titles and classifies them into categories using embeddings and vector search.

## Project Overview

This repository provides all the code and configuration to:

- Ingest news data from multiple sources.
- Process and clean collected news articles.
- Orchestrate workflows using Prefect.
- Run and monitor data pipelines locally.


## Features

- Automated news data ingestion and processing.
- Integration with Prefect for workflow management.
- Local and programmatic execution of flows.

## Installation

Clone the repository and install the package locally:

```bash
git clone https://github.com/your-username/news-orchestration.git
cd news-orchestration
pip install .
```

## Usage

Run flows using the Prefect CLI:

```bash
prefect deployment run 'pipeline/news_scraping'
```

You can also customize or create new flows by editing the Python modules in the repository.

## License
This project is distributed under the MIT License.
