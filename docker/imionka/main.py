import random

with open("imionka.txt", "r") as f:
    imionka = f.readlines()
    for i in range(len(imionka)):
        imionka[i] = imionka[i].strip()

with open("nazwiska.txt", "r") as f:
    nazwiska = f.readlines()
    for n in range(len(nazwiska)):
        nazwiska[i] = nazwiska[i].strip()

random.shuffle(imionka)
random.shuffle(nazwiska)

for i in range(400):
    print(imionka[i] + " " + nazwiska[i])

 