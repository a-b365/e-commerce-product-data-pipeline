import re
import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse,parse_qs

def get_hrefs(soup):

    tags = soup.find_all("a",attrs={"class":"a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"})
    hrefs = [tag["href"] for tag in tags if tag is not None]
    return hrefs

def get_title(soup):
    
    try:
        title = soup.find("span", attrs={"id":"productTitle"}).string.strip()

    except AttributeError:
        title = ""
    
    return title

def get_review_count(soup):
    
	try:
		review_count = soup.find("span", attrs={"id":"acrCustomerReviewText"}).string.replace(" ratings","").strip()
		
	except AttributeError:
		review_count = ""	

	return review_count

def get_rating(soup):

    try:
        rating = soup.find("div",attrs={"id":"averageCustomerReviews"})
        rating = rating.find("span", attrs={"class":"a-size-base a-color-base"}).string.strip()
    
    except AttributeError:
        rating = ""
            
    return rating


def get_price(soup):

    try:
        price = soup.find("div",attrs={"id":"corePriceDisplay_desktop_feature_div"})
        price = price.find("span", attrs={"class":"aok-offscreen"}).string.strip()
        
    except AttributeError:
        try:
            price = soup.find("div", attrs={"id":"corePrice_desktop"})
            price = price.find("span",attrs={"class":"a-offscreen"}).string.strip()

        except AttributeError:
            price = ""

    price = price.split(" ")[0]
    price = price.replace(",","")

    return price


def get_availabile(soup):

    try:
        available = soup.find("div", attrs={"id":"availability"})
        available = available.find("span").string.strip()
        #available = re.findall(r"\d+",available)
        
        # try:
        #     available = str(available[0])

        # except IndexError:
        #     available = ""

    except AttributeError:
        available = ""

    return available

def get_description(soup):
     
    try:
        description = soup.find("div", attrs={"id":"productDescription"})
        description = description.find_all("span")
        description = [d.string.strip() for d in description]
        description = "#".join(description)

    except AttributeError:
        description = ""

    return description

def get_category(soup):
     
    try:
        category = soup.find("div", attrs={"id":"wayfinding-breadcrumbs_feature_div"})
        category = category.find_all("a", attrs={"class": "a-link-normal a-color-tertiary"})
        category = [c.string.strip() for c in category]
        category = "|".join(category)
        
    except:
         category = ""
    
    return category

def write_csv(links):

    with open("products.csv", mode="w", newline="", encoding="utf-8") as csv_file:
        fieldnames = ["title","rating","price","available","review_count","description","category"]
        csv_writer = csv.writer(csv_file, delimiter="\t", quoting=csv.QUOTE_NONE, escapechar="\\")
        csv_writer.writerow(fieldnames)          
        for i in links:
            response = requests.get(i,headers=HEADERS)
            soup = BeautifulSoup(response.content,"lxml")
            csv_writer.writerow([get_title(soup),get_rating(soup),get_price(soup),get_availabile(soup),
                                 get_review_count(soup),get_description(soup),get_category(soup)])
     

if __name__ == "__main__":

    base_url = "https://www.amazon.com"

    HEADERS = (
            {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept-Language": "en-US, en;q=0.5"}
            )

    url = "https://www.amazon.com/s"

    params = [

        {'k': ['gaming laptops'], 
        'rh': ['n:565108'], 
        'ds': ['v1:eGYE7WjkLK1R0DipJ/2urKZSiLwl10Wew6xAnrl+AsY'],
        'crid': ['3B7GKFR3AXBM3'], 
        'qid': ['1714239554'], 
        'rnid': ['2941120011'], 
        'sprefix': [',aps,320'], 
        'ref': ['sr_nr_n_1']
        },

        {'k': ['expensive cameras'],
        'i': ['photo'], 
        'rh': ['n:172282,n:502394,n:281052'], 
        'ds': ['v1:o2OA14m1NZnQmyX1I1VTI4JXjSvbNeFfmPSrkKBz+bQ'], 
        'crid': ['3KDVL444F6GPQ'], 
        'qid': ['1714244318'], 
        'rnid': ['172282'], 
        'sprefix': ['expensive cameras,photo,354'], 
        'ref': ['sr_nr_n_4']
        },
    
        {'k': ['rock music cds'], 
        'rh': ['n:5174,n:40'], 
        'ds': ['v1:/TqQSU7YqKZUgV0JzG4WCweQsz1SAX6Cl+Sup1oRqrA'], 
        'crid': ['6T24IXKYJ4X8'], 'qid': ['1714239778'], 
        'rnid': ['2941120011'], 
        'sprefix': ['rock music cds,aps,1155'], 
        'ref': ['sr_nr_n_2']
        },

        {'k': ['woofers'], 
         'rh': ['n:172282,n:172568'], 
         'ds': ['v1:yX58pMeZiyVI16LjV0Va/BDE9qLtPpKjRbcgm7ASpL8'], 
         'crid': ['6I1WYA7ZRBYU'], 
         'qid': ['1714278992'], 
         'rnid': ['2941120011'], 
         'sprefix': ['woofers,aps,342'], 
         'ref': ['sr_nr_n_3']
        },

        {'k': ['premier league jersey'], 
        'rh': ['n:3203999011'], 
        'ds': ['v1:kMhtD+s5/NYgr4xktH6m+6sEhFSBptqzAfYjoKP5npU'], 
        'crid': ['1JV5TJIM9E9TN'], 
        'qid': ['1714279564'], 
        'rnid': ['2941120011'], 
        'sprefix': ['premier league jerse,aps,413'], 
        'ref': ['sr_nr_n_1']
        },

        {'k': ['mens fashion'], 
         'rh': ['n:1040658,n:1045624'], 
         'ds': ['v1:QWhaCZMEE0KkOz4v9eAIzHKCWLZrD0on2+4tY7di4iU'], 
         'crid': ['3V7XSTNRSE9JH'], 
         'qid': ['1714280085'], 
         'rnid': ['2941120011'], 
         'sprefix': ['mens fashio,aps,345'], 
         'ref': ['sr_nr_n_3']
        }
    ]


    responses = [ requests.get(url,headers=HEADERS,params=param) for param in params ]

    # parsed_url = urlparse(url)
    # query_params = parse_qs(parsed_url.query)
    # print(query_params)
    
    links = []

    for response in responses:
        soup = BeautifulSoup(response.content,"lxml")
        links += get_hrefs(soup)
    
    links = [base_url + link for link in links]

    write_csv(links)



