### Rating Product and Sorting Reviews

The purpose of this project is to calculate weighted average of product and sorting most useful reviews.

While calculating the weighted average of the product, each score was weighted according to the time interval it was given.

3 different functions were used to choose the most useful reviews. The first one makes a ranking according to the 
difference of positive and negative votes given to the review. The second ranks according to the ratio of positive 
votes to total votes. The last one sorts by wilson lower bound.

The first function does not produce a proportional result, so sorting is not very meaningful. 
For example, a review has 100 positive and 98 negative votes. Another review has 2 positive and 0 negative votes. 
In this case, the two observations get the same score, but the social proof of the first observation is negative. 
The second observation, on the other hand, does not have enough votes to create social proof. 
The two reviews are not in the same category, and it would be unreasonable for them to get the same score.

The second function produces a proportional result for sorting. However, among the reviews with the same ratio 
and different total number of votes, the higher the number of votes is more valuable. Because it has been approved by 
more people. But the function cannot evaluate this criterion. It also creates problems with observations that have zero 
negative votes with only a few positive votes. Because they settle high even though they do not deserve it.

In the third function, Wilson Lower Bound sets a lower bound with a mathematical equation to eliminate the uncertainty 
of a small number of observations. In this way, it produces the most meaningful results by eliminating the errors of 
the above functions.





