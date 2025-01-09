import numpy as np 

print('Version 1')
code = input('Please enter a code to break: ')
code = np.array(list(code),dtype=int)
#rule 1
characters = len(code)
if characters != 9:
    print('Decoy Message: Not a nine-digit number.') 
    #rule 2
else: sum1 = np.sum(code)
if sum1%2 == 0:
    print('Decoy Message: Sum is even.')
  #rule 3   
rescue_day = (int(code[2]) * int(code[1])) - int(code[0])
if rescue_day not in [1, 2, 3, 4, 5, 6, 7]:
      print("Decoy Message: Invalid rescue day.")
#rule 4
else: rendezvous_point = int(code[2])**int(code[1])
if rendezvous_point % 3 == 0:
      rendezvous_point = int(code[5]) - int(code[4])
else:
      rendezvous_point = int(code[4]) - int(code[5])
if rendezvous_point not in [1, 2, 3, 4, 5, 6, 7]:
      print("Decoy Message: Invalid rendezvous point.")
rendezvous_locations = {1: "bridge", 2: "library", 3: "river crossing", 4: "airport", 5: "bus terminal", 6: "hospital", 7: "railway station"}
rescue_days = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday", 7: "Sunday"}
print("Decoy Message: Rescued on " + rescue_days[rescue_day] + " at the " + rendezvous_locations[rendezvous_point])
   
('day = ',code[2]*code[1]-code[0])
power = np.power(code[2],code[1])
if power%3 == 0:
    place = code[5]-code[4]
else:
    place = code[4]-code[5]
('place = ',place)
