from google_api.google_api_client import overwrite_rows
from mysql_client.sql_client import sql_worker
import datetime
import time

spreadsheet_id = '1fnLuniqzygD_zW1CGRmU9XGaBnm14wRmc6vUHWy-PbQ'

query = 'SELECT template_file, CONCAT("https://tkrobotng.meltwater.net/tkrobotNG/index.asp?file=", REPLACE(template_file, ".cfg", ""), "&view=current&page=2") as template_link, ssi.sourceid, name, url, category, country, language, active, last_updated, CONCAT("https://tkrobotng.meltwater.net/tkrobotNG/index.asp?id=", ssi.sourceid, "&view=current&page=2") as source_link  FROM (SELECT sourceid, extra_info as template_file FROM source_extra_info WHERE type="inherit") as sei JOIN (SELECT sourceid, name, url, category, country, language FROM source_simplified_info WHERE sourceid IN (SELECT sourceid FROM source_extra_info WHERE type="inherit")) as ssi ON sei.sourceid=ssi.sourceid JOIN (SELECT sourceid, MAX(update_time) as last_updated FROM source_update_history WHERE sourceid IN (SELECT sourceid FROM source_extra_info WHERE type="inherit") GROUP BY 1) as suh ON sei.sourceid=suh.sourceid JOIN (SELECT sourceid, extra_info as active FROM source_extra_info WHERE type="activated" AND sourceid IN (SELECT sourceid as template_file FROM source_extra_info WHERE type="inherit")) as act ON act.sourceid=suh.sourceid ORDER BY 1'


if __name__ == '__main__':
    t1 = time.time()
    print('Fetching table...')
    map = sql_worker(query)
    t2 = time.time()
    print('Completed fetching table.\nExecution time: {} sec.'.format(t2 - t1))
    print(len(map))

    overwrite_rows(spreadsheet_id, 'data!A2:K{}'.format(len(map)+1), map)

    print('source_template_map updated.\nLink: https://docs.google.com/spreadsheets/d/{}'.format(spreadsheet_id))
