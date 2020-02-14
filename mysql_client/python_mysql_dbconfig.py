from configparser import ConfigParser


def read_db_config(filename, section):
    #reads config.ini and returns it as dictionary for python_mysql_connect.property

    parser = ConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]

    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))

    return db
