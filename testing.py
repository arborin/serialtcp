# STRING EXAMPLE  30.03.2022 12:15:53 PG:11 TQ:0.03 Nm AN:1861 Grad ABBRUCH
#                 ['30.03.2022', '12:15:53', 'PG:11', 'TQ:0.03', 'Nm', 'AN:1861', 'Grad', 'ABBRUCH']
# STRING EXAMPLE  30.03.2022 12:15:49 PG:11 TQ:3.49 Nm AN:10 Grad IO
#                 ['30.03.2022', '12:15:49', 'PG:11', 'TQ:3.49', 'Nm', 'AN:10', 'Grad', 'IO']
            
# get keys and values will be next elements in list

l = "30.03.2022 12:15:53 PG:11 TQ:0.03 Nm AN:1861 Grad ABBRUCH"

update_vals = l.split(" ")

values = {}
values['Date'] = update_vals[0]
values['Time'] = update_vals[1]


for data in update_vals:
    if "PG:" in data:
        values['PG'] = data.split(":")[-1]
    elif "TQ:" in data:
        values['TQ'] = data.split(":")[-1]
    elif "AN:" in data:
        values['AN'] = data.split(":")[-1]
        
values['Comment'] = " ".join(update_vals[6:])

print(values)
        