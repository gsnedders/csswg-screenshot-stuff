import csv
import os.path

def parse(fp):
    reader = csv.DictReader(fp, delimiter="\t")
    return reader

def is_visual(test):
    flags = test["flags"].split(",")
    if "script" in flags or test["references"]:
        return False
    return True

def is_screenshottable(test):
    flags = set(test["flags"].split(","))
    if {"interact", "animated", "ahem", "font", "http", "paged", "speech", "userstyle"}.intersection(flags):
        return False
    return True

def is_HTML(test):
    flags = test["flags"].split(",")
    return ("nonHTML" not in flags)

def build_path(testinfo_path, test):
    dirname = os.path.dirname(testinfo_path)
    if is_HTML(test):
        if os.path.exists(os.path.join(dirname, "html4")):
            return os.path.join("html4", test["id"] + ".htm")
        else:
            return os.path.join("html", test["id"] + ".htm")
    else:
        return os.path.join("xhtml1", test["id"] + ".xht")

def main(filename):
    dirname = os.path.dirname(filename)
    with open(filename, "r") as fp:
        reader = parse(fp)
        with open(os.path.join(dirname, "reftest.list"), "w") as wfp:
            for test in reader:
                if is_visual(test) and is_screenshottable(test):
                    path = build_path(filename, test)
                    wfp.write("!= %(test)s %(test)s\n" % {"test": path})

if __name__ == "__main__":
    import sys
    main(sys.argv[1])
