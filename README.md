# bid2win
## Introduction
The goal of this project is to competatively bid on customers in a simulated real-time bidding environment. Some historic data on past successful bids is available.

## General Approach
The requirements of this project are in general
1. An artificially intelligent agent that examines information about users and then places bids accordingly.

2. A software framework that abstracts the web API and allows the AI Agent to simply obtain the user information it needs and then place bids on that user, without having to worry about the details of the data.

#### Artificial Intelligence
Since historic data is available about a number of past users and the revenue from their purchases, some **Machine Learning** is possible. This can allow to look at the demographic data for a given user and predict an expected revenue for that user. That data is lacking a critical piece of information, however: the amount of the bid placed in order to win that user. In addition to this, we have a simulated "opponent" bidding against us, so there is an adversarial component to the problem. Since the adversary does not change tactics over time, we can simply treat it as part of the environment and incorporate some form of **Reinforcement Learning** to observe results of bids placed at runtime and change its behavior to try and maximise the reward (net profit).

For this project, all decision making on bid amount is handled by the various Bidder classes. These classes do make use of Machine Learning as part of their decision process, but generally use some other strategy as well that varies bid amount at runtime based on some strategy.

#### Data Framework
The nature of data obtained from the Web API is inherently transient... we are given a user's data **exactly once** and never again. Our AI may need access to those past records, for example, if it makes use of a Nearest Neighbors algorithm. In addition, we need to be able to conveniently look up the user_id for which we want to place a bid.

For these reasons, our code that abstracts the Web API and JSON payloads will have a total of three primary tasks:
1. Communicate with the servers via the Web API
2. Maintain a repository of the data that has been either recieved or sent via that API.
3. Expose the repository of data in a robust and meaningful way.

These tasks are all handled for our project by the Querent class (noun | que-rent | One who consults an authority, astrologer or source of information).

## Bid Placing Agents

#### AnnealingAgent
(Used for the first 2,500 bids)

The strategy for this bidder is to start bidding very low on all users, and increase bids as time goes on. Bidding stops when either a) we start winning bids for this type of user, or b) we reach our threshhold above which we think this kind of user will just not be profitable.
    
The amount by which we raise the bid each time goes down over time, allowing the algorithm to settle into a steady pattern of bidding. This is a technique known as "**simulated annealing**."

This approach treats the problem of the "adversarial bid" like finding the minimum of an unknown function. Since the adversary may bid drastically lower on some demographics than others, we are actually looking at multiple functions, each of which has its own minimum. The twist is that some of our inputs are continuous, and we don't know what values of those inputs should be treated as "one category" for optimization purposes, except to guess that categories are probably contiguous. If that is the case, then we can gain our insight on how the adversary will bid by looking at our past bids on similar users, and adjusting accordingly.

In this case, the AnnealingAgent uses a **Nearest Neighbors** unsupervised algorithm to identify a list of past bids on similar users. It analyses those bids and decides if it should bid higher than those past bids (because most of them are lost bids), or if it should continue bidding a similar amount. In this way the bidder can settle on bidding around $.90 for one category of users because that is enough, while still continuing to raise the bid on another type of demographic until it reaches $1.50.

Many choices of hyperparameter are available in the class constructor to adjust the behavior of the algorithm