f=open("backup_h2.txt","r",encoding="utf-8")
f2=open("testh2.txt","a",encoding="utf-8")
for x in f.readlines():
    for y in range(len(x)):
        if x[y]==";":
            f2.write("\n")
        else:
            f2.write(x[y])



f=open("testh2.txt","r",encoding="utf-8")
f2=open("testh22.txt","a",encoding="utf-8")
for x in f.readlines():
    for y in range(len(x)):
        if x[y]=="'":
            if x[y+1]=="," or x[y-2]==",":
                f2.write('"')
            elif x[y-1]=="[" or x[y+1]=="]":
                f2.write('"')
            else:
                f2.write(x[y])

        else:
            f2.write(x[y])
