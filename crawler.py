import time, re, json, os
import selenium.webdriver
from selenium.webdriver.common.keys import Keys
from google.cloud import bigquery
import logging


def get_company(company_string):
    """
    Returns the company name from each user profile summary. 
    company_string: for each user profile summary, a broken down list of words in the summary.
    """
    for index, word in enumerate(company_string):
        if word in ['Founder', 'Co-founder', 'CEO', 'founder'] :
            company = ' '.join(company_string[index:])
            
            if '.' in company:
                stop_pos = [m.start(0) for m in re.finditer(r'\.', company)][0]
            else:
                stop_pos = len(company)  
            
            return company[:stop_pos]


def get_founder_company(query_list):
    """
    Returns a dictionary that matches founder names with their companies.
    query_list: a list of user profile strings.
    """
    sample_db = {}
    for name in query_list:
        name_com = name.replace('\n', ' ').split(', ')
        if len(name_com) > 1:
            sample_db[name_com[0]] = get_company(name_com[1].split(" "))
    return sample_db


def write_to_json(json_file, raw_list):
    """
    Write a raw list of dictionary to json file. 
    Input:
    json_file: the path of new json file.
    raw_list: the name of the list to be transformed to json.
    """
    with open(json_file, 'w') as f:
        for line in f:
            f.writelines(json.dumps(line) + '\n')


def send_to_bq(svc_key, table_id, schema_list, file_name, dataset_id, table_name):
    """
    Initiate bq client, gathers table schema, create a table, config bq job, and finally sends json file to bq table.
    """
    client = bigquery.Client.from_service_account_json(svc_key)
    table_id = table_id

    schema = schema_list

    table = bigquery.Table(table_id, schema=schema)
    table = client.create_table(table)

    file_name = file_name
    dataset_id = dataset_id
    table_name = table_name

    dataset_ref = client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_name)

    schema_file_name = 'schema_temp.json'
    os.system(f"generate-schema --keep_nulls < {file_name} > {schema_file_name}")

    schema = open(schema_file_name, 'r').read()
    job_config = bigquery.LoadJobConfig()
    job_config.source_format = 'NEWLINE_DELIMITED_JSON'
    job_config.autodetect = True
    job_config.write_disposition = "WRITE_APPEND"
    job_config.schema_update_options = 'ALLOW_FIELD_ADDITION'
    job_config.ignore_unknown_values = True

    with open(file_name, 'rb') as source_file:
        job = client.load_table_from_file(
            source_file,
            table_ref,
            job_config=job_config)  
            
    try:
        job.result() 
    except: 
        log.info(job.errors)
        job.result()


if __name__ == '__main__':
    # initiate a chromedriver session
    driver = selenium.webdriver.Chrome('/Users/vicky/Dev/chromedriver')
    driver.get("https://www.quora.com/search?q=founder&type=profile")
    print(driver.window_handles)

    # automate the scroll down action to handle infinite scroll
    for i in range(1, 100):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)

    # find QueryResultsList which contains all profile summaries
    element = driver.find_elements_by_class_name("QueryResultsList")
    query_list = element[0].text.split("Profile:")
    get_founder_company(query_list)

    write_to_json(json_file = 'company_quora.json', raw_list = get_founder_company(query_list))

    send_to_bq(
        svc_key =  "/Users/vicky/Dev/seraph_etl.json",
        table_id = "pure-silicon-196123.seraph_v1.company_quora",
        schema_list = [
                bigquery.SchemaField("founder_name", "STRING", mode="Nullable"),
                bigquery.SchemaField("company_name", "STRING", mode="Nullable"),
            ],
        file_name = 'company_quora.json',
        dataset_id = 'seraph_v1',
        table_name = 'company_quora'
    )