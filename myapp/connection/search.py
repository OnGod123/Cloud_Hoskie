from pymongo import MongoClient
from datetime import date

def search_persons(criteria):
    """
    Perform a non-strict search on the MongoDB collection with OR conditions for age, weight, and height.

    Args:
    - criteria (dict): Dictionary containing search parameters.

    Returns:
    - List[dict]: A list of matching documents from MongoDB.
    """
    # Step 1: Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')  # Replace with your MongoDB URI
    db = client['mydatabase']  # Replace with your MongoDB database name
    collection = db['person']  # Replace with your MongoDB collection name

    # Step 2: Build the MongoDB query
    query = {}

    if criteria.get('race'):
        query['race'] = criteria['race']
    if criteria.get('sexual_orientation'):
        query['sexual_orientation'] = criteria['sexual_orientation']
    if criteria.get('skin_color'):
        query['skin_color'] = criteria['skin_color']

    # Build $or conditions for age, weight, and height ranges
    or_conditions = []
    if criteria.get('min_age') and criteria.get('max_age'):
        min_birth_date = criteria['min_age']
        max_birth_date = criteria['max_age']
        or_conditions.append({'birth_date': {'$gte': max_birth_date, '$lte': min_birth_date}})
    if criteria.get('min_weight') and criteria.get('max_weight'):
        or_conditions.append({'weight': {'$gte': criteria['min_weight'], '$lte': criteria['max_weight']}})
    if criteria.get('min_height') and criteria.get('max_height'):
        or_conditions.append({'height': {'$gte': criteria['min_height'], '$lte': criteria['max_height']}})

    # Add $or to the query if any range conditions are provided
    if or_conditions:
        query['$or'] = or_conditions

    # Step 3: Query the MongoDB collection
    results = list(collection.find(query))

    return results
