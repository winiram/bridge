import pandas as pd
from urllib.request import urlopen

def validate(df):
    """ Validate a data frame. Return an dict with a 'success' boolean and an 'error' message.
    """
    for header in df.columns.values:
        if "Unnamed:" in header:
            print("Invalid file uploaded, missing headers.")
            return {"success":False, "error":"Invalid file uploaded, missing headers."}
    return {"success":True}

def load(file_url, mimetype):
    """ Load file into pandas dataframe."""
    if mimetype == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" or mimetype == "application/vnd.ms-excel":
        # Problem, this makes too many requests on the server
        data_url = file_url
#        xld = urlopen(data_url).read()
        #xlds = StringIO.StringIO(xld)
        df = pd.read_excel(urlopen(data_url), sheetname=0)
    elif mimetype == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        df = pd.read_csv(file_url)
    return df
