# Climate Cabinet - Tax Credit Bonus Map Widget

<img alt="Demo of widget functionality" src="./docs/docs/assets/widget_demo.gif" style="margin-bottom: 25px;"/>


A full-stack web application allowing local officials to search for tax credit bonuses newly-available under the Inflation Reduction Act (2020) within their state, county, municipality, municipal utility, or rural cooperative. At the time of writing, featured tax credit programs include the Alternative Fuel Refueling Property Credit, Direct Pay Clean Energy Investment Tax Credit, Direct Pay Clean Energy Production Tax Credit, Neighborhood Access and Equity Grant, and Solar for All. Program eligibilty is determined by the presence of a low-income, distressed, energy, and/or Justice 40 community within the jurisdiction, and tax credits can stack if a jurisdiction contains more than one of these "bonus" communities.

The application is not intended to be a standalone website, but a "widget" embedded as an iframe in Climate Cabinet Education's main WordPress site. Decoupling the widget from the site had the benefit of safer and more flexible development. Because the widget's logic and configuration could be updated independently, software engineers external to Climate Cabinet never required elevated permissions or access to core code bases. In addition, engineers were able to take advantage of popular, tried-and-tested JavaScript libraries when designing the front-end rather than work within the system of WordPress plugins.

## Features

Users can:

- Search for a geography by name by typing into an autocomplete box. After a configured debounce period, they will see a dropdown of search results or "No Results Found" based on their search phrase.

- Click on a search result and wait for the web app to process their request. Upon completion, the map zooms to the boundaries of the selected geography and shows the current geography and all of its bonus communities as Mapbox tileset layers. In addition, a summary of the geography, its bonus communities, and eligible programs, along with population counts, are displayed in the sidebar.

- Hover over geographies on the map to view their names.

- Select which tileset layer(s) to view at once by toggling checkboxes in the map control panel.

- Switch between political and satellite base maps using radio buttons in the map control panel.

- Open a full-screen view of the map by clicking on the expand button in the map's upper lefthand corner.


## Documentation

Detailed documentation on the application's datasets, architecture, and infrastructure may be found [**here**](https://climatecabinet.github.io/climate-cabinet-tax-credit-map/) in the repository's GitHub Pages site. The site can also be run locally in the web browser using the Python package `mkdocs`. Activate your virtual environment of choice, navigate to the `docs` directory, and then run:

```
pip install -r requirements.txt
mkdocs serve
```

## Local Development

To run the application locally for development and testing, follow the setup instructions and then execute one of several entrypoint commands described below.

### Dependencies

- Make
- Docker Desktop
- Mapbox

### Setup

1. **Download Environment Files.** Download the `.env.dev` and `.env.test` files from the configured **[Google Cloud Storage bucket location]("")** and then save them under the project's `pipeline` directory. Similarly, download the `.env` file from Cloud Storage and save it under the `dashboard` directory. These files are ignored by Git by default.

2. **Download Data Files.** Download the zipped data file from the same bucket and save it under the root of the project. Unzip the file to create a new `data` directory containing `raw`, `clean`, and `test` subfolders and delete any remaining zip artifacts. The entire `data` directory is also ignored by Git.

3. **Get Test Mapbox API Tokens.**  Create a separate, non-production Mapbox account if you don't already have one (e.g., a personal account).  Log into your account through a web browser and then generate a new secret token with the scopes "tilesets:read", "tilesets:write", and "tilesets:list". Copy your username and token into `.env.dev` and `.env.test` as `MAPBOX_USERNAME="username"` and `MAPBOX_API_TOKEN="secret token"`. Then copy your username and public token value (as listed on your user account page) and save them in your dashboard's `.env` file as `NEXT_PUBLIC_MAPBOX_USERNAME="username"` and `NEXT_PUBLIC_MAPBOX_ACCESS_TOKEN="public token"`, respectively.

4. **Install Make.** Install **[make](https://sites.ualberta.ca/dept/chemeng/AIX-43/share/man/info/C/a_doc_lib/aixprggd/genprogc/make.htm)** for your operating system. On macOS and Windows Subsystem for Linux, which runs on Ubuntu, `make` should be installed by default, which you can verify with `make --version`. If the package is not found, install `build-essential` (e.g., `sudo apt-get install build-essential`) and then reattempt to verify. If you are working on a Windows PC outside of WSL, follow the instructions **[here](https://gist.github.com/evanwill/0207876c3243bbb6863e65ec5dc3f058#make)**.

5. **Install Docker Desktop.**  Follow the instructions **[here](https://docs.docker.com/engine/install/)** to install the latest version of Docker Desktop for your operating system. (The project uses Docker Compose V2.) Then, confirm that Docker has been installed correctly by running `docker --version` in a terminal. Be careful to enable the appropriate distros in Docker Desktop if working in WSL.

### Entrypoints

The project's Makefile provides simple entrypoints for running the application locally as a Docker Compose application. A few simple pointers:

- All of the commands listed below **must be run under the root of the project**.

- Services can be shut down at any point by entering `CTRL-C` or, for services executing in the background, `CTRL-D`. This automatically shuts stops and destroys the active Docker containers.

- Data from the PostgreSQL databases are persisted in the Docker volumes "pgdata_small" and "pgdata_large", which are saved as folders under the project root and ignored by Git. Because the project's Docker containers are run as the root user, you will need to assign yourself ownership of the directories if you'd like to delete or modify it (e.g., `sudo chown -R <username> pgdata_small`).

- For all commands, pgAdmin is provided as a GUI for the PostgreSQL databases. To use pgAdmin, navigate to `localhost:443` in a web browser, select `servers` in the dropdown in the lefthand sidebar, click on the database you would like to inspect, and then log in with the password `postgres` when prompted. **[Browse tables and query the loaded data](https://www.pgadmin.org/docs/pgadmin4/latest/user_interface.html#user-interface)** using raw SQL statements.

#### Run Full-Stack Application

To run the web app locally for the first time, execute the following two commands in sequence:

```
make run-pipeline-execution
make run-dashboard
```

The first statement executes the Django pipeline while the second starts a Next.js development server and initializes a new Prisma ORM client with the existing database schema to enable direct queries against the database. After the ORM has been set up, you can navigate to `http://localhost:3000` in your browser to begin using the web app.

Subsequent invocations of `make run-pipeline-execution` are unnecessary after the database has been initialized the first time. To run the full-stack application later in the future, simply execute:

```
make run-dashboard
```

#### Run Database

```
make run-database
```

This command builds and runs the PostGIS database and pgAdmin GUI. It is helpful for examining the database and running queries without the overhead of additional Compose services.

#### Develop Pipeline

```
make run-pipeline-interactive
```

This command builds and runs the PostgreSQL databases, pgAdmin GUI, and Django pipeline. The pipeline is run as a live development server in the background, with an attached interactive terminal. Using the terminal, you can run commands and scripts as part of the development process. 

#### Test Pipeline

```
make test-pipeline
```

This command runs tests against the `load_geos` and `load_associations` Django management commands in the pipeline. The remaining tests have dependencies with Google Cloud Storage and Mapbox and must be configured and executed separately. 


## Credits

This project is a collaborative effort between **[Climate Cabinet Education](https://climatecabineteducation.org/)** and the **[University of Chicago Data Science Institute](https://11thhourproject.org/)**, with generous support from the **[11th Hour Project](https://11thhourproject.org/)**.
