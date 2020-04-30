from surprise import KNNBasic
from surprise import Dataset
from surprise import SVD
from surprise import SVDpp
from collections import defaultdict
import os
from surprise import Reader
import pymysql

def get_top_n(predictions, n=10):
    '''Return the top-N recommendation for each user from a set of predictions.

    Args:
        predictions(list of Prediction objects): The list of predictions, as
            returned by the test method of an algorithm.
        n(int): The number of recommendation to output for each user. Default
            is 10.

    Returns:
    A dict where keys are user (raw) ids and values are lists of tuples:
        [(raw item id, rating estimation), ...] of size n.
    '''

    # First map the predictions to each user.
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))

    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]

    return top_n


def store_predictions_to_sql(predictions):
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))

    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        counter = 0
        for rating in user_ratings:
            counter += 1
            if counter >= 400:
                print("%s is done" % uid)
                break
            userId_sql = "'" + uid + "'"
            movieId_sql = "'" + rating[0] + "'"
            sql = "INSERT INTO predictions(userId, movieId, rating) VALUES (%s, %s, %s)" \
                  % (userId_sql, movieId_sql, rating[1])
            # print(sql)
            try:
                cursor.execute(sql)
                db.commit()
            except:
                db.rollback()


def get_rank_n_for_one_user(predictions, target_uid, begin = 0, end = 40):
    # First map the predictions to target user.
    top_n = []
    for uid, iid, true_r, est, _ in predictions:
        if uid == target_uid:
            top_n.append((iid, est))

    # Then sort the predictions and retrieve movies.
    top_n.sort(key=lambda x: x[1], reverse=True)
    return top_n[begin:end]


fname = 'database_password.txt'
with open(fname, 'r') as f:
    lines = f.readlines()
    host_ip = lines[0].strip('\n')
    user = lines[1].strip('\n')
    password = lines[2].strip('\n')
    database_name = lines[3].strip('\n')

# Load the movielens-100k dataset
# data = Dataset.load_builtin('ml-100k')

# path to dataset file
# file_path = os.path.expanduser('~/.surprise_data/ml-100k/ml-100k/u.data')
file_path = os.path.join(os.getcwd(), 'ml-latest-small/ratings.data')


# As we're loading a custom dataset, we need to define a reader. In the
# movielens-100k dataset, each line has the following format:
# 'user item rating timestamp', separated by '\t' characters.
reader = Reader(line_format='user item rating timestamp', sep=',')

data = Dataset.load_from_file(file_path, reader=reader)

# Retrieve the trainset.
trainset = data.build_full_trainset()

# Build an algorithm, and train it.
algo = SVDpp()
algo.fit(trainset)

'''
uid = str(196)  # raw user id (as in the ratings file). They are **strings**!
iid = str(302)  # raw item id (as in the ratings file). They are **strings**!

# get a prediction for specific users and items.
pred = algo.predict(uid, iid, verbose=True)
# print(pred.est)
'''

# Than predict ratings for all pairs (u, i) that are NOT in the training set.
testset = trainset.build_anti_testset()
predictions = algo.test(testset)

# rank_n = get_rank_n_for_one_user(predictions, str(603))
# print(rank_n)

db = pymysql.connect(host_ip, user, password, database_name)
cursor = db.cursor()
store_predictions_to_sql(predictions)
db.close()

# top_n = get_top_n(predictions, n=10)
#
# # Print the recommended items for each user
# for uid, user_ratings in top_n.items():
#     print(uid, [iid for (iid, _) in user_ratings])