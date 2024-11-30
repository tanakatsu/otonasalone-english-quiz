import sqlite3
from lib.sql_client import DB_NAME


def main():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        'CREATE TABLE articles(id INTEGER PRIMARY KEY AUTOINCREMENT, article_id INTEGER)'
    )
    cur.execute(
        'CREATE INDEX article_id_index on articles(article_id)'
    )

    conn.commit()
    conn.close()
    print("Created database.")


if __name__ == "__main__":
    main()
