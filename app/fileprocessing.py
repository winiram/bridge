import pandas as pd

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
        df = pd.read_excel(file_url)
    elif mimetype == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        df = pd.read_csv(file_url)
    return df
