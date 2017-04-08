#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urlparse
import sqlite3
import random
import string

def get_url(pontification):
    cursor.execute("SELECT count(*) FROM urls where pontification = ?", (pontification,))
    if cursor.fetchone()[0] == 0:
        return "https://pontification.solutions"
    else:
        cursor.execute("SELECT url FROM urls where pontification = ?", (pontification,))
        return cursor.fetchone()[0]

def get_or_create_pontification(url, length):
    cursor.execute("SELECT count(*) FROM urls where url = ? and len = ?", (url, length))
    if cursor.fetchone()[0] == 0:
        pontification = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(length - len(known_url)))
        pontification = known_url + pontification

        cursor.execute("INSERT INTO urls(url, len, pontification) VALUES (?, ?, ?)", (url, length, pontification))
        db.commit()
        return pontification

    else:
        cursor.execute("SELECT pontification FROM urls where url = ? and len = ?", (url, length))
        return cursor.fetchone()[0]

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()

    # hit /?url=ENCODEDURL&len=LENGTHOFLINK to get a pontificated url
    # hit /STRING to get redirected
    def do_GET(self):
        qs = {}
        path = self.path
        if '?' in path:
            self._set_headers()
            path, tmp = path.split('?', 1)
            qs = urlparse.parse_qs(tmp)

            if not 'url' in qs or not 'len' in qs:
                self.wfile.write("Failed to generate pontificated link - have you checked what you've entered?")
                return
            try:
                url = str(qs['url'][0]).lower()
                print url
                if not url.startswith('https://'):
                    if not url.startswith('http://'):
                        url = "http://" + url
                print url
                length = int(qs['len'][0])
            except:
                self.wfile.write("Failed to generate pontificated link - have you checked what you've entered?")
                return

            if length > 500 or length < 40:
                self.wfile.write("Failed to generate pontificated link - have you checked what you've entered?")
                return

            self.wfile.write(get_or_create_pontification(url, length))
        else:
            self.send_response(302)
            self.send_header("Location", get_url(known_url + path[3:]))
            self.end_headers()
            self.wfile.write("")



def run(server_class=HTTPServer, handler_class=S, port=5000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv
    known_url = "https://pontification.solutions/l/"
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
