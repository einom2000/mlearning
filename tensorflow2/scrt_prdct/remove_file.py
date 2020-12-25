import os


def remove(targetdir, endswith="@", startwith="@"):
    for fname in os.listdir(targetdir):
        if fname.endswith(endswith):
            os.remove(os.path.join(targetdir, fname))
        elif fname.startswith(startwith):
            os.remove(os.path.join(targetdir, fname))
