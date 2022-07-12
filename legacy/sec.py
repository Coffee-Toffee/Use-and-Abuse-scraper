# Just a little script to take one file, and make it into a small file for testing
# Not much, but it's honest work
source = open("sites_0_5.txt", "r")
dest = open("sites.txt", "w")
count = 0
for line in source:
    if count > 100:
        break
    count += 1
    dest.write(line)
souce.close()
dest.close()
