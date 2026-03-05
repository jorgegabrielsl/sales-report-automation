import pandas as pd
from database import get_connection
from email_sender import send_email


def extract_data():

    connection = get_connection()

    query = """
    SELECT
        customer_id,
        SUM(amount) AS total_sales
    FROM payment
    GROUP BY customer_id
    """

    df = pd.read_sql(query, connection)

    connection.close()

    return df


def transform_data(df):

    df["average_ticket"] = df["total_sales"] / 5

    return df


def save_report(df):

    file_path = "sales_report.xlsx"

    df.to_excel(file_path, index=False)

    return file_path


def main():

    data = extract_data()

    data = transform_data(data)

    report = save_report(data)

    send_email(
        destination="example@email.com",
        attachments=[report]
    )


if __name__ == "__main__":
    main()
