
###################################################################################################
# I test this function, because in the lab spec, it says nonlocal is for parent frame, so I want to
# make sure that parent frame not only means one layer of parent above, but can mean any layers of
# parent above, for example, in the below code, x is looked up two layers of parent frame above.
####################################################################################################
def a(x):
    def b(y):
        def c(z):
            nonlocal x
            x = x + y + z
            return x
        return c
    return b

