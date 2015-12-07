import base64
import hashlib
import re
import sqlite3

unexpected_fail = re.compile(r'^REFTEST TEST-UNEXPECTED-FAIL \| ([^\|]+) \|')
image = re.compile(r'^REFTEST   IMAGE: ')

def get_results(fp):
    for line in fp:
        m = unexpected_fail.match(line)
        if m:
            url = m.group(1)
            line2 = next(fp)
            if line2.startswith('REFTEST   IMAGE: '):
                imagedata = line2[39:].rstrip()
                rawdata = base64.b64decode(imagedata)
                print url
                yield (url, rawdata)

def main():
    with open('reftest.log', 'r') as fp:
        conn = sqlite3.connect('css-tests.db')
        for url, rawdata in get_results(fp):
            h = hashlib.sha512(rawdata).digest()
            print "inserting..."
            conn.execute('INSERT INTO screenshots VALUES (?, ?, ?)', (url, buffer(rawdata), buffer(h)))
        conn.commit()
        conn.close()

if __name__ == "__main__":
    main()
