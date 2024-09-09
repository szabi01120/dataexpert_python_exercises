import pandas as pd
import numpy as np
import urllib.robotparser

def crawlSite(site_url):
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url("https://www.etsy.com/robots.txt")
    rp.read()
    rp.crawl_delay("*")

    test_crawl_url = site_url

    can_crawl_listings = rp.can_fetch("*", test_crawl_url)
    return print("We can crawl? {0}\n".format(can_crawl_listings))

def etsyListing():
    df = pd.read_csv('../datasets/etsy-mens-t-shirts-11-15-2017.csv')
    etsyUrl = "https://www.etsy.com/listing/478395857/big-little-shirt-big-little-sorority"
    
    # most traffic, views on tshirt
    max_views_product = df.set_index('seller_name')['views'].idxmax()
    max_views = df.set_index('product_title')['views'].max()
    print("Most views:", max_views_product, "with", max_views, "views\n")
    
    # describe the data
    print("Etsy describe:\n", df.describe().round(3))

    # check if we can crawl etsy
    crawlSite(etsyUrl)
    
def playStoreListing():
    df = pd.read_csv('../datasets/google-play-store-11-2018.csv')
    gpUrl = "https://play.google.com/store/apps/details?id=com.wildnotion.poetscorner"
    
    print("Google play describe:\n", df.describe().round(3))
    
    print("Most downloadad categories:")
    most_downloaded = df.groupby('genre')['min_installs'].sum().head(5)
    print(most_downloaded, "\n")
    
    print("Least downloadad categories: ")
    least_downloaded = df.groupby('genre')['min_installs'].sum()
    print(least_downloaded.sort_values(ascending=True).head(5), "\n")
    
    # check if we can crawl google play
    crawlSite(gpUrl)
    
    # offers iap and is free
    print("Offers in-app purchases and is free:")
    result_df = df[(df['offers_iap'] == True) & (df['price'] == 0)]
    print(result_df[['title', 'price', 'offers_iap']])
    
    # avg rating of apps that offer iap
    avg_rating = df[df['offers_iap'] == True]['score'].mean().round(3)
    print("\nAverage rating of apps that offer in-app purchases:", avg_rating)
    
    # app with lowest rating
    lowest_rating_name = df[df['score'] > 0].set_index('title')['score'].idxmin()
    lowest_rating = df[df['score'] > 0].set_index('title')['score'].min()
    print("\nLowest rating:", lowest_rating_name, "with", lowest_rating, "rating")
    
    # star rating percentage comparison by genre
    star_ratings = df.groupby('genre')[['rating_one_star', 'rating_two_star', 'rating_three_star', 'rating_four_star', 'rating_five_star']].sum()
    star_ratings_percentage = star_ratings.div(star_ratings.sum(axis=1), axis=0).mul(100).round(2)
    star_ratings_percentage.sort_values(by='rating_five_star', ascending=False, inplace=True)
    
    print("\nStar rating percentage comparison by genre:\n", star_ratings_percentage.head(5))
    
    # ad count
    ad_count = df[df['ad_supported'] == False].groupby('genre')['ad_supported'].count()
    ad_count.sort_values(ascending=False, inplace=True)
    print("\nGenres not having advertisements:")
    print(ad_count.head(5).to_string(header=False))

def main():
    etsyListing()
    playStoreListing()
    
if __name__ == '__main__':
    main()