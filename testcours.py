varlist = []

varlist.append(0)
varlist.append(1)
varlist.append(0)
varlist.append(1)
varlist.append(1)
varlist.append(0)
varlist.append(1)
varlist.append(0)
varlist.append(0)


for travel_in_tab in varlist:
    print(travel_in_tab)

n = int(input("Entrez un entier:"))

if varlist[n]== 0:
    print("Noir")
else: 
    print ("Blanc")
    
last_color = "None"
color_counter = 0 
color_index = -1
is_swapping= False

for index_in_tab in range (len(varlist)):
    if last_color=="None":
        last_color = varlist[index_in_tab]
else:
    if last_color != varlist[index_in_tab]:
        if (not is_swapping):
            color_index = index_in_tab
        color_counter += 1
        is_swapping = True
    else:
        for swapping_pawn in range (color_counter):
            varlist[color_index]= last_color
print(varlist)