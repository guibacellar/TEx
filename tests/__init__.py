import os

data_dir: str = os.path.join(os.getcwd(), "data")
db_file: str = os.path.join(data_dir, 'local.db')

if not os.path.exists(data_dir):
    os.mkdir(data_dir)

if os.path.exists(db_file):
    os.remove(db_file)
