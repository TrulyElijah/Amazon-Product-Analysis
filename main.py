
import matplotlib.pyplot as plt
from datetime import datetime

def extract_data(path):
    """
    returns a list of dictionaries with data from tsv file
    """
    with open(path,'r') as f:
        lines = f.readlines()

    #create a list of disctionaries
    data = []
    for line in lines[1:]:
        line = line.strip().split('\t')
        
        #append dictionary to the list
        #keys are the column names
        data.append({
            'marketplace': line[0],
            'customer_id': line[1],
            'review_id': line[2],
            'product_id': line[3],
            'product_parent': line[4],
            'product_title': line[5],
            'product_category': line[6],
            'star_rating': line[7],
            'helpful_votes': line[8],
            'total_votes': line[9],
            'vine': line[10],
            'verified_purchase': line[11],
            'review_headline': line[12],
            'review_body': line[13],
            'review_date': line[14]
        })

    return data

def get_rating_count(data):
    """
    returns a dictionary with star ratings as key and number of reviews as value
    """
    count = {}
    #count number of review for each rating
    for d in data:
        rating = d['star_rating']
    
        if rating in count:
            count[rating] += 1
        else:
            count[rating] = 1

    #sort the dictionary by rating
    sorted_count = dict(sorted(count.items()))

    return sorted_count

def get_category_rating_count(data):
    """
    returns a dictionary with product category as key and number of reviews as value
    """
    count = {}
    #count number of review for each category
    for d in data:
        category = d['product_category']
        if category in count:
            count[category] += 1
        else:
            count[category] = 1
    
    #sort the dictionary by number of reviews
    sorted_count = dict(sorted(count.items(),key=lambda item: item[1]))
    
    return sorted_count  

def get_average_category_rating(data):
    """
    returns a dictionary with product category as key and average rating as value
    """
    category_ratings= {}
    
    for d in data:
        category = d['product_category']
        rating = d['star_rating']

        if category not in category_ratings:
            category_ratings[category] = [] #add list to the dictionary
        else:
            category_ratings[category].append(int(rating))   #append rating to the list

    #calculate average rating for each category
    category_avg_ratings = {}
    for category in category_ratings:
        ratings = category_ratings[category]
        avg_rating = round((sum(ratings)/len(ratings)),2)   #round the average rating to 2 decimal places
        
        category_avg_ratings[category] = avg_rating

    #sort the dictoinary by average rating
    sorted_avg_ratings = dict(sorted(category_avg_ratings.items(),key=lambda item: item[1]))

    return sorted_avg_ratings


def get_average_rating_over_time(data):
    """
    returns a dictionary with review date as key and average rating as value
    """
    review_dates = {}
    
    for d in data:
        date = d['review_date']
        rating = d['star_rating']

        dt = datetime.strptime(date,'%Y-%m-%d')

        year = dt.year  #extract year from date
       
        if year not in review_dates:
            review_dates[year] = [] #add list to the dictionary
        else:
            review_dates[year].append(int(rating))   #append rating to the list

    #calculate average rating for each date
    avg_ratings = {}
    for year in review_dates:
        ratings = review_dates[year]
        if len(ratings) != 0:
            avg_rating = round((sum(ratings)/len(ratings)),2)   #round the average rating to 2 decimal places
        
            avg_ratings[year] = avg_rating

    #sort the dictoinary by date
    sorted_avg_ratings = dict(sorted(avg_ratings.items()))

    return sorted_avg_ratings
    
def plot_rating_distribution(count):

    plt.figure(figsize=(12,6))
    plt.bar(count.keys(),count.values())
    plt.xlabel('Star Rating')
    plt.ylabel('Number of Reviews(in millions)')
    plt.title('Distribution of Star Ratings')

    plt.show()


def plot_category_distribution(count):
    
    plt.figure(figsize=(12,6))

    plt.xticks(rotation=90)
  
    plt.bar(count.keys(),count.values())
    plt.xlabel('Product Category')
    plt.ylabel('Number of Reviews(in millions)')
    plt.title('Distribution of Category Ratings')

    plt.show()

def plot_category_avg_rating(avg_category_ratings):
    plt.figure(figsize=(12,6))

    plt.xticks(rotation=90)
  
    plt.bar(avg_category_ratings.keys(),avg_category_ratings.values())
    plt.xlabel('Product Category')
    plt.ylabel('Average Ratings(1-5)')
    plt.title('Average Ratings of Product Categories')

    plt.show()

def plot_avg_rating_over_time(avg_ratings_over_time):
    plt.figure(figsize=(12,6))

    plt.xticks(list(avg_ratings_over_time.keys()),rotation=90)
  
    plt.plot(avg_ratings_over_time.keys(),avg_ratings_over_time.values())
    plt.xlabel('Year')
    plt.ylabel('Average Ratings(1-5)')
    plt.title('Average Ratings Over Time')

    plt.show()

def main():

    data = extract_data("amazon_reviews_multilingual_US_v1_00.tsv")

    print(f"Number of Records: {len(data)}")

    rating_count = get_rating_count(data)
    print(f"Number of Reviews Per Rating:\n {rating_count}")
    plot_rating_distribution(rating_count)

    category_rating_count = get_category_rating_count(data)
    print(f"Number of Reviews Per Category:\n {category_rating_count}")
    plot_category_distribution(category_rating_count)

    avg_category_ratings = get_average_category_rating(data)
    print(f"Average Rating Per Category:\n {avg_category_ratings}\n")
    print("Analysis: Based on the average ratings by category, Health and Personal Care has the lowest average rating at 3.83, while Grocery holds the highest average rating at 4.65.")
    plot_category_avg_rating(avg_category_ratings)


    avg_rating_over_time = get_average_rating_over_time(data)
    print(f"Average Rating Per Year:\n {avg_rating_over_time}\n")
    print("Analysis: Examining the average ratings by year, we observe a general decline from 1995 to 2004, followed by a slight increase between 2004 and 2007. The ratings then decline again from 2007 to 2011, before rising steadily through 2015.")
    plot_avg_rating_over_time(avg_rating_over_time)

main()