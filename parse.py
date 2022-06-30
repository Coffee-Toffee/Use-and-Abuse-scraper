def parse_first(string):
    return(string.strip("{\'")[:len(string)-5])
    
def parse_second(lists):
    l = lists.split("[")
    a = l[1].replace("\\", "")
    b = l[2].replace("\\", "")
    a=a.strip()
    b=b.strip()
    a = a.strip("}")
    a = a.strip(")")
    a = a.strip("]")
    a = a.strip("'")

    b = b.strip("}")
    b = b.strip(")")
    b = b.strip("]")
    b = b.strip("'")

    a=a.split(",")
    b=b.split(",")
    l = []
    for i in range(min(len(a), len(b))):
        l.append((a[i], b[i]))
    return(l)


with open("dict_0_2.txt", "r") as file:
    lines = file.readlines()
    line_gen = (line.split("(") if line != "\n" else None for line in lines)
    for i in line_gen:
        if i is not None:
            j = parse_second(i[1])
            for k in j:
                print(parse_first(i[0]), k)
