def silently_attempt(fn, *args, **kwargs):
    try:
        fn(*args, **kwargs)
    except:
        ...