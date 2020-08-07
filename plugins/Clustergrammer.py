def main(df):
    import requests
    import pandas as pd
    from io import BytesIO
    dataframe = prepare_df(df) # Define the path to the file you want to visualize.
    output = BytesIO()
    dataframe.to_csv(output, sep='\t', index=False)
    output.seek(0)

    upload_url = "https://amp.pharm.mssm.edu/clustergrammer/matrix_upload/" # Define the path to the visualizing sertver endpoint.
    response = requests.post(upload_url, files={'file': output})
    print(response.text)
    vis_link = response.text
    
    return vis_link

def prepare_df(df):
    import pandas as pd
    import copy
    import numpy as np
    dataframe = copy.deepcopy(df)

    # Append category title string before values for all cat columns.
    # dataframe[dataframe.columns[0:cat_amount]] = dataframe.columns[0:cat_amount] + \
    #     ': ' + dataframe[dataframe.columns[0:cat_amount]].astype(str)
    # Remove the category titles from first row.
    categories = list(df.select_dtypes(exclude=[np.number]).columns) # Get all columns that are non numerics
    value_columns = [x for x in list(df.columns) if x not in categories] # Get all columns that are not category columns
    print('categoris: ', value_columns)
    print("categories: ", categories)
    dataframe_reordered_columns = categories + value_columns
    print('dataframe_reordered_columns: ', dataframe_reordered_columns)
    dataframe = dataframe[dataframe_reordered_columns] # Put all categories column to the beginning of the dataframe.
    print(dataframe)
    if len(categories) > 0:
        for category in categories:
            print(category)
            dataframe[category] = dataframe[category].name + ': ' + dataframe[category].astype(str)
            dataframe = dataframe.rename(columns={category: ''})
    else:
        dataframe.columns[0] = dataframe.columns[0].name + ': ' + dataframe.columns[0].astype(str)
        dataframe = dataframe.rename(columns={dataframe.columns[0]: ''})
    print('here: ')
    print(dataframe)
    # Export the data frame as tab-seperated .txt.
    print('Output file has been generated and saved.')
    return dataframe