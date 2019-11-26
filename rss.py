#!usr/bin/python3

from feedgen.feed import FeedGenerator as feed

a = feed()
a.id('Test')
a.title('Unknown')
a.description('Hello world!')
a.link(href='http://ipv4.pingwu.me/rss.xml')

b = a.add_entry()
b.id('test content')
b.title('this is a test')
b.link(href='http://github.com/wpwupingwp')

a.rss_file('rss.xml')
