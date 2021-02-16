import pandas as pd
import math
import scipy.stats as st

pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

# Reading dataset. In this dataset there is only one product "B007WTAJTO".
df_ = pd.read_csv("df_sub.csv")
df = df_.copy()
df.head(10)
df.tail(10)
df.info()
df.shape

# There are only 2 null values. It is negligible.
df.isnull().sum()

# Max overall is 5.0 point.
df["overall"].max()

# Raw Average of Ratings
df["overall"].mean()

# Calculate weighted average score by date. Define current_date as a reference point.
# day_diff is how many days have passed since reviewed then create 3 time frames based on this variable.
df['reviewTime'] = pd.to_datetime(df['reviewTime'], dayfirst=True)
current_date = pd.to_datetime('2014-12-08 0:0:0')
df["day_diff"] = (current_date - df['reviewTime']).dt.days

a = df["day_diff"].quantile(0.25)
b = df["day_diff"].quantile(0.50)
c = df["day_diff"].quantile(0.75)

# Calculate weighted average based on time frames for the product.
df.loc[df["day_diff"] <= a, "overall"].mean() * 28 / 100 + \
    df.loc[(df["day_diff"] > a) & (df["day_diff"] <= b), "overall"].mean() * 26 / 100 + \
    df.loc[(df["day_diff"] > b) & (df["day_diff"] <= c), "overall"].mean() * 24 / 100 + \
    df.loc[(df["day_diff"] > c), "overall"].mean() * 22 / 100

#########################################
# Pick most useful 20 review.

# Define 3 variables as helpful_yes, helpful_no and total vote.
df["helpful_yes"] = df[["helpful"]].applymap(lambda x: x.split(",")[0].strip('[')).astype(int)
df["helpful_total_vote"] = df[["helpful"]].applymap(lambda x: x.split(",")[1].strip(']')).astype(int)
df["helpful_no"] = df["helpful_total_vote"] - df["helpful_yes"]

df = df[["reviewerName", "overall", "summary", "helpful_yes", "helpful_no", "helpful_total_vote", "reviewTime"]]


# Define a function that calculates difference between positive and negative votes for each review(row).
def score_pos_neg_diff(pos, neg):
    return pos - neg


df["score_pos_neg_diff"] = df.apply(lambda x: score_pos_neg_diff(x["helpful_yes"], x["helpful_no"]), axis=1)


# Define a function that calculates ratio of positive votes for each review(row).
def score_average_rating(pos, neg):
    if pos - neg == 0:
        return 0
    return pos/(pos+neg)


df["score_average_rating"] = df.apply(lambda x: score_average_rating(x["helpful_yes"], x["helpful_no"]), axis=1)


# Define a function that calculate wilson lower bound score for each review(row).
def wilson_lower_bound(pos, neg, confidence=0.95):
    n = pos + neg
    if n == 0:
        return 0
    z = st.norm.ppf(1 - (1 - confidence) / 2)
    phat = 1.0 * pos / n
    return (phat + z * z / (2 * n) - z * math.sqrt((phat * (1 - phat) + z * z / (4 * n)) / n)) / (1 + z * z / n)


df["wilson_lower_bound"] = df.apply(lambda x: wilson_lower_bound(x["helpful_yes"], x["helpful_no"]), axis=1)

df.sort_values("wilson_lower_bound", ascending=False).head(20)

df.sort_values("score_average_rating", ascending=False).head(20)

df.sort_values("score_pos_neg_diff", ascending=False).head(20)


