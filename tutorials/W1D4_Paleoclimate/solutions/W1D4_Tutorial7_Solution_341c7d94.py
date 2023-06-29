
# perform significance test with 30 surrogates
d18O_wwz_sig = d18O_wwz.signif_test(number = 30)

# plot the results
d18O_wwz_sig.plot(xlabel='Period [kyrs]')