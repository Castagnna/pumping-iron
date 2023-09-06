# Pumping-iron
Web scraping and analysis of my body evolution results.

Acess the [App](https://pumping-iron.streamlit.app/)

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
