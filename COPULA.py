import numpy as np
import pandas as pd
from scipy import stats
from matplotlib import pyplot as plt
import seaborn as sns

#  ---------------------------------------------------------------------------------------------------------------------
# An intuitive, visual guide to copulas
# https://twiecki.io/blog/2018/05/03/copulas/

# (...)
# Above we only specified the distributions for the individual variables, irrespective of the other one (i.e.
# the marginals). In reality we are dealing with a joint distribution of both of these together.
#
# Copulas to the rescue.
# (...)
#
# What are copulas in English?
# Copulas allow us to decompose a joint probability distribution into their marginals (which by definition have no
# correlation) and a function which couples (hence the name) them together and thus allows us to specify the correlation
# seperately. THE COPULA IS THAT COUPLING FUNCTION.
#
# Transforming random variables
# Let's start by sampling uniformly distributed values between 0 and 1:
x = stats.uniform(0, 1).rvs(10000)
sns.distplot(x, kde=False, norm_hist=True);
# Next, we want to transform these samples so that instead of uniform they are now normally distributed. The transform
# that does this is the INVERSE OF THE CUMULATIVE DENSITY FUNCTION (CDF) of the normal distribution (which we can get
# in scipy.stats with ppf):
norm = stats.distributions.norm()
x_trans = norm.ppf(x)
sns.distplot(x_trans)
# alternatively use matplotlib:
# plt.style.use('ggplot')
# plt.hist(x_trans, bins='sturges', density=True)
# plt.show()

# If we plot both of them together we can get an intuition for what the inverse CDF looks like and how it works:
h = sns.jointplot(x_trans,x, stat_func=None)
h.set_axis_labels('transformed', 'original', fontsize=16);

# We can do this for arbitrary (univariate) probability distributions, like the Beta:
beta = stats.distributions.beta(a=10, b=3)
x_trans = beta.ppf(x)
h = sns.jointplot(x_trans, x,stat_func=None)
h.set_axis_labels('transformed', 'orignal', fontsize=16);
# Or a Gumbel:
gumbel = stats.distributions.gumbel_l()
x_trans = gumbel.ppf(x)
h = sns.jointplot(x_trans, x, stat_func=None)
h.set_axis_labels('transformed','original', fontsize=16);
str.upper('inverse of the cumulative density function (CDF)')

# IN ORDER TO DO THE OPPOSITE TRANSFORMATION FROM AN ARBITRARY DISTRIBUTION TO THE UNIFORM(0, 1) we just apply the
# inverse of the inverse CDF -- the CDF:
x_trans = gumbel.rvs(size=10000)
x_trans_trans = gumbel.cdf(x_trans)
h = sns.jointplot(x_trans, x_trans_trans, stat_func=None)
h.set_axis_labels('original', 'transformed', fontsize=16);

# OK, so we know how to transform from any distribution to uniform and back. In math-speak this is called the
# PROBABILITY INTEGRAL TRANSFORM.

# Adding correlation with Gaussian copulas
# How does this help us with our problem of creating a custom joint probability distribution? We're actually almost
# done already. We know how to convert anything uniformly distributed to an arbitrary probability distribution.
# So that means we need to generate uniformly distributed data with the correlations we want. How do we do that?
# We simulate from a multivariate Gaussian with the specific correlation structure, transform so that the marginals are
# uniform, and then transform the uniform marginals to whatever we like.
#
# CREATE SAMPLES FROM A CORRELATED MULTIVARIATE NORMAL:
mvnorm = stats.multivariate_normal(mean=[0, 0], cov=[[1., 0.5],
                                                     [0.5, 1.]])
# Generate random samples from multivariate normal with correlation .5
x = mvnorm.rvs(100000)
h = sns.jointplot(x[:, 0], x[:, 1], kind='kde', stat_func=None);
h.set_axis_labels('X1', 'X2', fontsize=16);

# NOW USE WHAT WE LEARNED ABOVE TO "UNIFORMIFY" THE MARIGNALS:
norm = stats.norm()
x_unif = norm.cdf(x)
h = sns.jointplot(x_unif[:, 0], x_unif[:, 1], kind='hex', stat_func=None)
h.set_axis_labels('Y1', 'Y2', fontsize=16);

# This joint plot above is usually how (2D) copulas are visualized.
#
# NOW WE JUST TRANSFORM THE MARGINALS AGAIN TO WHAT WE WANT (GUMBEL AND BETA):
m1 = stats.gumbel_l()
m2 = stats.beta(a=10, b=2)
x1_trans = m1.ppf(x_unif[:, 0])
x2_trans = m2.ppf(x_unif[:, 1])
h = sns.jointplot(x1_trans, x2_trans, kind='kde', xlim=(-6, 2), ylim=(.6, 1.0), stat_func=None);
h.set_axis_labels('Maximum river level', 'Probablity of flooding', fontsize=16);

# CONTRAST THAT WITH THE JOINT DISTRIBUTION WITHOUT CORRELATIONS:
x1 = m1.rvs(10000)
x2 = m2.rvs(10000)
h = sns.jointplot(x1, x2, kind='kde', xlim=(-6, 2), ylim=(.6, 1.0), stat_func=None);
h.set_axis_labels('Maximum river level', 'Probablity of flooding',  fontsize=16);

# So there we go, by using the uniform distribution as our lingua franca we can easily induce correlations and flexibly
# construct complex probability distributions. THIS ALL DIRECTLY EXTENDS TO HIGHER DIMENSIONAL DISTRIBUTIONS AS WELL.

# Above we used a multivariate normal which gave rise to the Gaussian copula. However, we can use other, more complex
# copulas as well. For example, we might want to assume the correlation is non-symmetric which is useful in quant finance
# where correlations become very strong during market crashes and returns are very negative.
#
# In fact, Gaussian copulas are said to have played a key role in the 2007-2008 Financial Crisis as tail-correlations
# were severely underestimated. If you've seen The Big Short, the default rates of individual mortgages (among other
# things) inside CDOs (see this scene from the movie as a refresher) are correlated -- if one mortgage fails, the
# likelihood of another failing is increased. In the early 2000s, the banks only knew how to model the marginals of the
# default rates. This infamous paper by Li then suggested to use copulas to model the correlations between those
# marginals. Rating agencies relied on this model heavily, severly underestimating risk and giving false ratings.
# The rest, as they say, is history.
#
# Read this paper for an excellent description of Gaussian copulas and the Financial Crisis which argues that different
# copula choices would not have made a difference but instead the assumed correlation was way too low.