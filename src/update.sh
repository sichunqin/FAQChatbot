echo "At $(date), begin to crawl data" > crawl.log
python3 data/update.py>> crawl.log
