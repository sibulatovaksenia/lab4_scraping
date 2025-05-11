# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector
import re



class SaveToDatabasePipeline:
    def open_spider(self, spider):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="scrapy"
            )
            self.cursor = self.conn.cursor()
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS items (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255),
                    price VARCHAR(50),
                    url TEXT,
                    image TEXT,
                )
            ''')
            self.conn.commit()
            print("Database connection successful!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def process_item(self, item, spider):
        # Ensure cursor is properly initialized
        if not hasattr(self, 'cursor'):
            print("Error: Database cursor is not initialized.")
            return item


        try:
            # Insert item into the database
            self.cursor.execute('''
                INSERT INTO items (name, price, url, image)
                VALUES (%s, %s, %s, %s)
            ''', (
            item.get("name"), item.get("price"), item.get("url"), ",".join(item.get("image_urls", []))))
            self.conn.commit()
            print("Item saved to database!")
        except mysql.connector.Error as err:
            print(f"Error saving item to database: {err}")

        return item

    def close_spider(self, spider):
        if hasattr(self, 'conn'):
            self.conn.close()


class DataCleaningPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Clean name and price
        if adapter.get("name"):
            adapter["name"] = adapter["name"].strip()

        if adapter.get("price"):
            price = adapter["price"].strip()

            # Remove non-numeric characters (including the currency symbol) and convert to a float
            price = re.sub(r'[^\d.,]', '', price)  # Remove anything that is not a number or comma/period
            price = price.replace(",", "")  # Remove commas
            price = price.replace(".", "")  # Remove periods if present
            adapter["price"] = price

        return item
