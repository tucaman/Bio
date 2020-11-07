from scipy import stats

mvnorm = stats.multivariate_normal(mean=[0, 0], cov=[[1., 0.5],
                                                     [0.5, 1.]])
# Generate random samples from multivariate normal with correlation .5
x = mvnorm.rvs(100000)

# Now use what we learned above to "uniformify" the marignals:
norm = stats.norm()
x_unif = norm.cdf(x)
