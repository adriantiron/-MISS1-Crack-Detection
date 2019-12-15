import aspectlib as al


@al.Aspect(bind=True)
def db_decorator(cutpoint, *args, **kwargs):
    with open("db_logger.txt", "a+") as f:
        f.write("`%s` got called for user = `%s`" % (cutpoint.__name__, args[0]))
        result = yield
        if result == 1:
            string = "Success"
        else:
            string = "Failure"

        f.write(" ... and the result is: %s \n" % (string,))


@al.Aspect(bind=True)
def fe_decorator(cutpoint, *args, **kwargs):
    with open("fe_logger.txt", "a+") as f:
        f.write("`%s` got called" % (cutpoint.__name__,))
        result = yield
        if result == 1:
            string = "Success"
        else:
            string = "Failure"

        f.write(" ... and the result is: %s \n" % (string,))


@al.Aspect(bind=True)
def nn_decorator(cutpoint, *args, **kwargs):
    with open("nn_logger.txt", "a+") as f:
        f.write("`%s` got called" % (cutpoint.__name__,))
        result = yield
        f.write(" ... and the result is: %s \n" % (result,))
