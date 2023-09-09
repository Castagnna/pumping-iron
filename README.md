# Pumping-iron
Web scraping and analysis of my body evolution results.

Acess the [App](https://pumping-iron.streamlit.app/)

## About
This project is splitted in two parts *pump* and *iron*.
```
├── pumping-iron 
│   ├── iron # reading mongo and plotting streamlit app.
│   ├── pump # web scraping my anthropometric data and inserting into mongodb atlas.
```

## Prepare your environment

Install venv:
```bash
sudo apt update

sudo apt upgrade

sudo apt install python3.10-venv
```

Activate the virtual environment and install requirements:
```bash
python3.10 -m venv pumpenv

source pumpenv/bin/activate

pip install -r requirements.txt
```

When you're done working with the virtual environment, you can deactivate it by running:
```bash
deactivate
```
## Run the scrapper

```bash
cd pump

scrapy crawl pump_spider
```

## Run the streamlit app locally

```bash
cd iron

streamlit run streamlit_app.py
```

### Local Streamlit's development stream

```bash
git checkout main

git pull

git checkout dev

git fetch origin main:main

git merge main

git push origin dev
```

Acess the [Dev App](https://pumping-iron-dev.streamlit.app/)