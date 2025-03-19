# CaptionScraper

Author: Dr. Robert Treharne, School of Life Sciences, University of Liverpool

Idea: Prof. Alan Radford, School of Veterinary Science, University of Liverpool

Version: V1.0

https://www.canvaswizards.org.uk

This tool will:

+ Allow you to scrape all of the captions out of ALL Panopto videos associated with a Canvas course
+ Save them all in a sortable .tsv file



## Usage

### Step 1. Clone this repository

```{bash}
git clone https://github.com/rtreharne/CaptionScraper
cd subdown
```

### Step 3. Install requirements

Create a virtual environment and install requirements
```{bash}
python -m venv .venv 
source /.venv/bin/activate
pip install -r requirements.txt
```

If you don't want to create a virtual environment
```{bash}
pip install -r requirements.txt
```

### Step 5. Run `main.py`

```{bash}
python main.py
```















