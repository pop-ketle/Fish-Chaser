# Fish-Chaser
FC: the app for chasing fish

This repository is a sequel to [iSea](https://github.com/pop-ketle/iSea)

## Directory Structure
```
.
├── README.md <- This
├── crawler <- Scraping script for datasets
│   ├── example.py
│   └── initialize_db.py
├── datasets <- datasets
│   ├── README.md
│   ├── images
│   │   ├── SQLite_icon.svg
│   │   └── data_ER.svg
│   └── raw <- raw datasets
│       ├── data.db <- SQLite DB
│       ├── fishery_data.csv
│       ├── satellite_images <- Satellite Images/YEAR/IMG_CLASS/{IMG_CLASS}_{yyyymmdd}0000.png
│       └── suion_data.csv
```

## Initialize
Download dataset from G-Drive  
https://drive.google.com/drive/folders/1M0aMYlUAgpzrzAYVEMkPrYeE9rJx6z91?usp=sharing

Place the downloaded dataset as shown above.


next step is later...

## DB Architecture
![ER図](./datasets/images/data_ER.svg)