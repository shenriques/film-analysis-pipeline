import os 
import pandas as pd
import logging

# logging
logging.basicConfig(
    filename='logs/data_profiling.log',
    level=logging.INFO,
    format='%(levelname)s @ %(asctime)s: %(message)s'
) 

data_dir = '../data'
output = 'outputs/data_summary.md'

# loads CSVs into dataframes
def load_data(filename):
    try:
        df = pd.read_csv(filename, low_memory=False) # automatic d types might be wrong hence False
        logging.info(f'File: {filename} loaded successfully. Total rows, colums: {df.shape}')
        return df
    except Exception as e:
        logging.info(f'ERROR: {filename} failed to load due to {e}')
        return None

# creates a markdown summary of the csv 
def generate_summary(df, filename):

    # stats
    rows, columns = df.shape
    missing_val_count = df.isnull().sum()
    missing_percentage = (missing_val_count / len(df)) * 100 
    missing_summary = missing_val_count[missing_val_count > 0] # all columns with missing values

    # markdown header for each file
    md_summary = f"\n\n## Summary for: {filename}\n\n"
    md_summary += f"- Rows: {rows}\n"
    md_summary += f"- Columns: {columns}\n\n"

    # section 1: missing values
    if not missing_summary.empty:
        md_summary += "### Missing Values \n"
        md_summary += "| Column | Missing Count | Missing % |\n"
        md_summary += "|--------|--------------|-----------|\n"
        for col in missing_summary.index:
            md_summary += f"| {col} | {missing_val_count[col]} | {missing_percentage[col]:.2f}% |\n"
        md_summary += "\n"

    # section 2: sample data
    sample = df.sample(min(2, len(df))) # in case dataset is really small 
    md_summary += "### Sample Rows\n"
    md_summary += sample.to_markdown(index=False) + "\n\n"

    # section3: column overview 
    md_summary += "### Column Overview\n"
    md_summary += "| Column | Type | Unique Values | Top Value |\n"
    md_summary += "|--------|------|--------------|-----------|\n"

    for col in df.columns:
        most_common_val = df[col].mode()[0] if not df[col].mode().empty else 'N/A'
        unique_vals = df[col].nunique()
        md_summary += f"| {col} | {df[col].dtype} | {unique_vals} | {most_common_val} |\n"

    return md_summary

def main():

    data_summary = "# Data Summary \n\n"

    for data_file in os.listdir(data_dir):
        if data_file.endswith('.csv'):
            file_path = os.path.join(data_dir, data_file)
            df = load_data(file_path)

            if df is not None: # check there is data
                generate_summary(df, data_file)
                data_summary += generate_summary(df, data_file)

    with open(output, 'w') as file:
        file.write(data_summary)

    logging.info(f'Finished data profiling, view {output}')

if __name__ == "__main__":
    main()