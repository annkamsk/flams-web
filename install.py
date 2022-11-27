from flams.databases.setup import MODIFICATIONS, update_db_for_modifications


def setup_databases():
    for modification in MODIFICATIONS.keys():
        update_db_for_modifications([modification])


if __name__ == "__main__":
    setup_databases()
