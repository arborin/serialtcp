l = ['09.03.2022', '10:22:58', 'PG:', '11', 'TQ:', '3.81', 'Nm', 'AN:', '1215', 'Grad', 'IO']

values = {"PG": '', "TQ": '', "AN": ''}

for key in values.keys():
    try:
        index = l.index(key+":")
        values[key] = l[index+1]
    except:
        print("key not found")



print(values)
