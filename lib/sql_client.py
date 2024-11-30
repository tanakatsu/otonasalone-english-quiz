import sqlite3
import pandas as pd

DB_NAME = 'articles.db'


class SqlClient:
    TABLE_NAME = "articles"

    def __init__(self, db_name: str = DB_NAME):
        self.db_name = db_name

    def insert(self, article_id: int) -> None:
        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()
        cur.execute(f"INSERT INTO {self.TABLE_NAME}(article_id) VALUES(?)", (article_id,))

        conn.commit()
        cur.close()
        conn.close()

    def select_by_article_id(self, article_id: int) -> pd.DataFrame:
        conn = sqlite3.connect(self.db_name)
        df = pd.read_sql(f"SELECT * FROM {self.TABLE_NAME} where article_id = ?", conn,
                         params=(article_id,))
        return df
