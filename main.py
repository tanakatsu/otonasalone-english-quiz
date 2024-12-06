import os
from pathlib import Path
from lib.otonasalone import OtonaSalone, Article
from lib.ocr import OCR
from lib.line import LineClient
from lib.sql_client import SqlClient, DB_NAME


def mark_article_as_processed(article: Article) -> None:
    sql_client = SqlClient()
    sql_client.insert(article.id)


def select_new_articles(articles: list[Article]) -> list[Article]:
    sql_client = SqlClient()

    filtered_articles = []
    for article in articles:
        df = sql_client.select_by_article_id(article.id)
        if df.empty:
            filtered_articles.append(article)
    return filtered_articles


def build_message(article: Article, text: str) -> str:
    msg = f"{article.title}\n↓\n↓\n↓\n{text}\n\n{article.url}"
    return msg


def main():
    if not Path(DB_NAME).exists():
        raise ValueError("ERROR: You must create database in advance.")

    otonasalone = OtonaSalone()
    ocr_processor = OCR()
    line_client = LineClient()
    line_target_user_id = os.environ.get("LINE_TARGET_USER_ID", None)

    articles = otonasalone.get_articles()
    new_articles = select_new_articles(articles)
    print(f"Found {len(new_articles)} articles.")

    input_base64_images = [otonasalone.get_encoded_image(article.url)
                           for article in new_articles]
    texts = ocr_processor.get_texts(input_base64_images)
    for article, text in zip(new_articles, texts):
        print(f"{article.title}\n{text}\n")

    for article, text in zip(new_articles, texts):
        answer_message = build_message(article, text)
        # print(message)
        line_client.send_message(answer_message, line_target_user_id)
        mark_article_as_processed(article)


if __name__ == "__main__":
    main()
