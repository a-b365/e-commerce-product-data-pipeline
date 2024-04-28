E-commerce Product Data Pipeline

1. The "extract.py" uses beautiful soup to scrape the product data in amazon along with requests library. The scraped data is stored in a csv file.
2. The "transform.py" does necessary transformation such as filling and removing missing values, removing dollar symbols as well as standardize the product with respect to the category.
3. The "load.py" uses the cleaned data and load it to the mariadb. This includes creation of database, creation of tables and inserting values of csv file row by row.
