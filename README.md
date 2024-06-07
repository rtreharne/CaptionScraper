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
git clone https://github.com/rtreharne/subdown
cd subdown
```

### Step 3. Install requirements

Create a virtual environment and install requirements
```{bash}
python -m virtualenv .venv 
.\.venv\Scripts\activate
pip install -r requirements.txt
```

If you don't want to create a virtual environment
```{bash}
pip install -r requirements.txt
```

### Step 4. Create a `config.py` file (Optional)

If you're going to be running lots of reports it might be useful to create a `config.py` file containing your `CANVAS_URL` and `CANVAS_TOKEN`.

Do the following:

```{bash}
cp sample.config.py config.py
nano config.py
```

Update the `CANVAS_URL` and `CANVAS_TOKEN` variables. To create a new token, follow the guidance at:

https://community.canvaslms.com/t5/Admin-Guide/How-do-I-manage-API-access-tokens-as-an-admin/ta-p/89

### Step 5. Run `main.py`

```{bash}
python main.py
```















