import pytest
import numpy as np

#example test (passes)
def test_Dist_kc90():
    from distributions import Dist_kc90
    dist=Dist_kc90()
    do_detailed_test(dist)

#example test (fails)
def test_Dist_yz4244():
    from distributions import Dist_yz4244
    dist=Dist_yz4244()
    do_detailed_test(dist)

# make a test for each distribution (as opposed to 1 big test)
# http://doc.pytest.org/en/latest/example/parametrize.html
import distributions
all_distributions_dict = dict([(name, cls) for name, cls in distributions.__dict__.items() if isinstance(cls, type)])
all_distributions_list = [(cls) for name, cls in distributions.__dict__.items() if isinstance(cls, type)]

@pytest.mark.parametrize("dist", all_distributions_list)
def test_this_dist(dist):
    do_detailed_test( dist() )


# the actual test code
def do_detailed_test(dist):
    cls = dist.__class__
    N_test = 100000
    #print('will try to generate for %s' %(cls.__name__))
    if dist.pdf(dist.x_min + .3*(dist.x_max-dist.x_min)) < 1E-3:
        print("may have a problem")
        
    rvs = dist.rvs(N_test)
    print(np.mean(rvs), dist.mean())

    sample_mean = np.mean(rvs)
    pred_mean = dist.mean()
    assert np.abs(sample_mean-pred_mean) < 5*np.std(rvs)/np.sqrt(N_test)

    #if np.abs(sample_mean-pred_mean)) > 5*np.std(rvs)/np.sqrt(N_test):
    #    print("means don't match for %s: %f vs. %f" %(cls.__name__, 
    #                                                np.mean(rvs), dist.mean()))

    sample_std = np.std(rvs)
    pred_std = dist.std()

    assert np.abs(sample_std-pred_std) < 5*np.std(rvs)/np.sqrt(np.sqrt(1.*N_test))
    # print("std devs. don't match for %s: %f vs. %f" %(cls.__name__, 
    #                                           np.std(rvs), dist.std()))

    assert np.abs(sample_std-pred_std) < 5*np.std(rvs)/np.sqrt(np.sqrt(1.*N_test))
    #    print("std devs. don't match for %s: %f vs. %f" %(cls.__name__, 
    #                                                np.std(rvs), dist.std()))

    assert np.abs(sample_std - dist.std()) / dist.std() < 0.1
    #    print("std devs. don't match for %s: %f vs. %f" %(cls.__name__, 
    #                                                np.std(rvs), dist.std()))

    xtest = np.linspace(dist.x_min,dist.x_max,100)
    binwidth = xtest[1]-xtest[0]
    assert np.any(dist.pdf(xtest)<0) == False
    #    print("pdf was negative in some places")

    # check normalization
    #print("cumsum = ", np.sum(dist.pdf(xtest))*binwidth)
    #assert np.abs( np.sum(dist.pdf(xtest))*binwidth-1.) < 0.1
    #    print("pdf was not normalized properly")


