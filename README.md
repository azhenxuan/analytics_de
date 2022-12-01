# Data Engineering (Mediawiki) - Introduction
- Spin up a SQL-esque database holding tables of Mediawiki pages' metadata and links
    - with periodic replacements from SQL dumps on MediaWiki (1st, 20th of every month)
- Build two GET API endpoints to expose for querying/testing
    - caching for endpoint (returning the most outdated page given a specified category) to be done with an in-memory store 
- automate periodic collection of Mediawiki SQL dumps to refresh database tables with 
- Ensure reproducibility of this application between different devices

## Proposed Solution 
- Flask for endpoint service, MySQL as RDBMS to store tables of data in, Redis as in-memory store for caching purposes.
- Bash & Python scripts to handle data transformations and ORM to databases since they are simple to handle and code out
- Automation done with crontab - ease of setup
- Three containers are spun up - Flask, MySQL and Redis that work with each other to provide the end service.

## Folder Structure
```
analytics_de/
├── code/
│   ├── .env
│   ├── app.py
│   ├── automate_script.sh
│   ├── Dockerfile
│   ├── queries.py
│   ├── repopulate_cache.py
│   ├── requirements.txt
│   └── start.sh
├── db_data_dumps/
│   ├── simplewiki-{latest_date_of_dump}*-categorylinks.sql
│   ├── simplewiki-{latest_date_of_dump}-page.sql
│   ├── simplewiki-{latest_date_of_dump}-pagelinks.sql
│   └── simplewiki-populate-tables-and-cleanup.sql
├── docker-compose.yaml
└── README.md
```

### Files 
- `app.py`: Flask app serving endpoints 
- `automate_script.sh`: downloads current day's SQL dumps and processes them into MySQL.
- `Dockerfile`: ran on startup within Flask container
- `queries.py`: Fixed string that are imported and reused in other scripts with configurable parameters
- `repopulate_cache.py`: on execution, repopulates the `Redis` cache with the most outdated page query results.
- `requirements.txt`: installing necessary Python libraries to serve the endpoints
- `start.sh`: initializing script when Flask container is spun up - runs Flask app; initially populates the cache; and sets up cron job for the 1st and 20th of each month

- `docker-compose.yaml` - config file that eases setup with `docker-compose` 
- `simplewiki-populate-tables-and-cleanup.sql`: creates the two necessary tables (`metadata` and `links`) and removes the three initially dumped tables (`page`, `pagelinks`, `categorylinks` from the database.


## Installation/Initialization
### Setting up containers
Change directory into `analytics_de` before running the command below:
```
docker-compose up
```
This spins up all three instances via `docker-compose.yaml` and seeding of the database is done via the mounted volume `db_data_dumps` onto `/docker-entrypoint-initdb.d/`

### `start.sh`
The bash script ensures that Flask is initialized and the Redis cache is also populated with the most outdated page for the top 10 categories with most pages.

The cron job for automating the download and subsequent processing of the SQL dumps every 1st and 20th of each month.

## Pointers to take note 
- Considered combining both tables together to denormalize for ease of queries.
    - However, numerous links between pages will result in a table with exponentially increased number of rows
- A simple assumption is made for question 2b - without accounting for the distribution of target pages, each source category's page count is tabulated purely based on the number of categories each page is linked to.
    - This is taken as reference for the top 10 categories with most pages
- Randomly removed ~75% of the `pagelinks` & `categorylinks` SQL dumps on bootup to reduce runtime on creation & population of tables. Subsequent runs using cronjob results in full .SQL dumps being processed
- Cronjob is utilized for an easy rerun of jobs
- Docker for easier reproducible results and operating on Linux (since I am stuck on a Windows machine unfortunately :( )
- Python scripts for executing data transformation & flask related operations, bash scripts for obtaining the regualar SQL dumps on mediawiki
    - .env files to keep variables used repeatedly
- Things that I could have done better:
    - Maybe caching in Redis was abit of an overkill, maybe given a different kind of end point to be serviced/processed, it might have been a smarter choice to reduce bloat
    - first time spinning up services using Docker, so I spent alot of time dealing with trial and error - fiddling between different images and trying to connect to different services.


## License

[MIT](https://choosealicense.com/licenses/mit/)