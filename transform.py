import csv
import pandas as pd
import numpy as np

def fill_missing(group):
   min_value = group.min()
   return group.fillna(min_value)

def standardize(df):
    
   group_a = df.index[
         (df['category'] == "Electronics|Computers & Accessories|Computers & Tablets|Laptops|Traditional Laptops") | 
         (df['category'] == "Electronics|Camera & Photo|Digital Cameras|Point & Shoot Digital Cameras")|
         (df['category'] == "Electronics|Camera & Photo|Digital Cameras|Mirrorless Cameras")|
         (df['category'] == "Electronics|Camera & Photo|Digital Cameras|DSLR Cameras")].to_list()

   group_b = df.index[
         (df['category'] == "CDs & Vinyl|Classic Rock|Album-Oriented Rock (AOR)") | 
         (df['category'] == "CDs & Vinyl|Rock")|
         (df['category'] == "CDs & Vinyl|Pop")|
         (df['category'] == "CDs & Vinyl|Rock|Hard Rock")|
         (df['category'] == "CDs & Vinyl|Pop|Oldies|Baroque Pop")|
         (df['category'] == "Books|Arts & Photography|Music")|
         (df['category'] == "CDs & Vinyl|Rock|Progressive|Progressive Rock")|
         (df['category'] == "CDs & Vinyl|Rock|Rock Guitarists|Guitar Gods")|                                       
         (df['category'] == "CDs & Vinyl|Children's Music|Lullabies")|
         (df['category'] == "CDs & Vinyl|Classic Rock|Southern Rock")|
         (df['category'] == "Electronics|Home Audio|Speakers|Subwoofers")].to_list()

   group_c = df.index[
         (df['category'] == "Clothing, Shoes & Jewelry|Men|Clothing|Shirts|T-Shirts") |
         (df['category'] == "Sports & Outdoors|Fan Shop|Clothing|Jerseys") |
         (df['category'] == "Clothing, Shoes & Jewelry|Men|Clothing|Underwear|Undershirts") | 
         (df['category'] == "Clothing, Shoes & Jewelry|Men|Clothing|Active|Active Shirts & Tees|T-Shirts")|
         (df['category'] == "Clothing, Shoes & Jewelry|Novelty & More|Clothing|Novelty|Men|Shirts|T-Shirts")|
         (df['category'] == "Clothing, Shoes & Jewelry|Sport Specific Clothing|Soccer & Futsal|Men|Jerseys")|
         (df['category'] == "Clothing, Shoes & Jewelry|Men|Clothing|Active|Active Shirts & Tees")|
         (df['category'] == "Clothing, Shoes & Jewelry|Men|Clothing|Shirts|Polos")|
         (df['category'] == "Clothing, Shoes & Jewelry|Men|Clothing|Shirts|Button-Down Shirts")|
         (df['category'] == "Clothing, Shoes & Jewelry|Women|Clothing|Tops, Tees & Blouses|T-Shirts")|
         (df['category'] == "Clothing, Shoes & Jewelry|Boys|Clothing|Active|Active Shirts & Tees")|
         (df['category'] == "Clothing, Shoes & Jewelry|Sport Specific Clothing|Softball|Women|Pants")|
         (df['category'] == "Clothing, Shoes & Jewelry|Sport Specific Clothing|Baseball|Boys|Pants")|
         (df['category'] == "Clothing, Shoes & Jewelry|Sport Specific Clothing|Baseball|Men|Pants")|
         (df['category'] == "Clothing, Shoes & Jewelry|Sport Specific Clothing|Baseball|Men|Jerseys")|
         (df['category'] == "Clothing, Shoes & Jewelry|Sport Specific Clothing|Soccer & Futsal|Boys|Jerseys")|
         (df['category'] == "Clothing, Shoes & Jewelry|Men|Clothing|Active|Track & Active Jackets")|
         (df['category'] == "Clothing, Shoes & Jewelry|Novelty & More|Clothing|Novelty")|
         (df['category'] == "Clothing, Shoes & Jewelry|Men|Clothing|Swim|Rash Guard Shirts")].to_list()
   
   return (group_a,group_b,group_c)
    

if __name__  == "__main__":
    
   df = pd.read_csv("products.csv",sep="\t",escapechar="\\")

   #If price is NaN then remove the whole row
   df = df.dropna(subset=["price"])

   df.drop_duplicates(inplace=True)

   #If available is Nan fill with "Not Available"
   df["available"].fillna(value="Not Available", inplace=True)

   #If description is NaN fill with "No Description"
   df["description"] = df["description"].fillna(value="No Description")

   #If description is NaN fill with "No Description"
   df["category"] = df["category"].fillna(value="No Category")

   #Remove the dollar sign from price and convert to numeric
   extr = df["price"].str.replace("$","")
   df["price"] = pd.to_numeric(extr)
    
   #Remove comma from review_count
   extr = df["review_count"].str.replace(",","")
   df["review_count"] = pd.to_numeric(extr)

   df = df.reset_index(drop=True)
   df["p_id"] = df.index

   group_a, group_b, group_c = standardize(df)
   
   df.loc[group_a,"category"] = "Electronics"
   df.loc[group_b,"category"] = "Entertainment"
   df.loc[group_c,"category"] = "Clothing"

   df["rating"] = df.groupby("category")["rating"].transform(fill_missing)
   df["review_count"] = df.groupby("category")["rating"].transform(fill_missing)
   df["review_count"] = df["review_count"].astype(np.int64)

   print(df.info())

   #df.to_csv('cleaned.csv',escapechar="\\",quoting=csv.QUOTE_NONE,encoding="utf-8",index=False,sep="\t")
