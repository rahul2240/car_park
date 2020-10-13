import sys
import Car
import argparse

if sys.version_info[0] == 2:
    input = raw_input

class ParkingLot:
    def __init__(self):
        self.capacity = 0
        self.parkingId = 0
        self.totalOccupiedSpace = 0
    
    def createParkingLot(self, capacity):
        self.slots = [-1] * capacity
        self.capacity = capacity
        return self.capacity

    def getUnoccupiedSlot(self):
        for i in range(len(self.slots)):
            if self.slots[i] == -1:
                return i

    def parkCar(self, regno, age, size=1):
        if self.totalOccupiedSpace < self.capacity:
            id = self.getUnoccupiedSlot()
            size = 1
            self.slots[id] = Car.Car(regno, age, size)
            self.parkingId = self.parkingId + 1
            self.totalOccupiedSpace = self.totalOccupiedSpace + size
            return id + 1
        else:
            return -1
    
    def leave(self, parkingId, size=1):
        if self.totalOccupiedSpace > 0 and self.slots[parkingId - 1] != -1:
            regno = self.slots[parkingId - 1].regno
            age = self.slots[parkingId - 1].age
            self.slots[parkingId - 1] = -1
            self.totalOccupiedSpace = self.totalOccupiedSpace - size
            return (regno, age)
        else:
            return (-1, -1)

    def getRegNoFromAge(self, age):
        registration_numbers = []

        for i in self.slots:
            if i != -1 and i.age == age:
                registration_numbers.append(i.regno)
        
        return registration_numbers

    def getSlotNoFromRegNo(self, regno):
        
        for i in range(len(self.slots)):
            if self.slots[i].regno == regno:
                return i + 1
        
        return -1
    
    def getSlotNoFromAge(self, age):
        slotNumbers = []

        for i in range(len(self.slots)):
            if self.slots[i] == -1:
                continue
            if self.slots[i].age == age:
                slotNumbers.append(str(i+1))
        
        return slotNumbers
    
    def read_input(self, line):
        if line.startswith('Create_parking_lot'):
            capacity = int(line.split(' ')[1])
            capa = self.createParkingLot(capacity)
            print('Created parking of '+str(capa)+' slots')

        elif line.startswith('Park'):
            regno = line.split(' ')[1]
            age = line.split(' ')[3]
            slot_booked = self.parkCar(regno,age)
            if slot_booked == -1:
                print("Parking Full")
            else:
                print('Car with vehicle registration number “' + str(regno) + '” has been parked at slot number ' + str(slot_booked))

        elif line.startswith('Leave'):
            leave_slotid = int(line.split(' ')[1])
            car_info = self.leave(leave_slotid)
            if car_info[0] != -1:
                print('Slot number {} vacated, the car with vehicle registration number “{}” left the space, the driver of the car was of age {}'.format(leave_slotid, car_info[0], car_info[1]))

        elif line.startswith('Vehicle_registration_number_for_driver_of_age'):
            age = line.split(' ')[1]
            regnos = self.getRegNoFromAge(age)
            print(', '.join(regnos))

        elif line.startswith('Slot_numbers_for_driver_of_age'):
            age = line.split(' ')[1]
            slotnos = self.getSlotNoFromAge(age)
            print(', '.join(slotnos))

        elif line.startswith('Slot_number_for_car_with_number'):
            regno = line.split(' ')[1]
            slotno = self.getSlotNoFromRegNo(regno)
            if slotno == -1:
                print("Not found")
            else:
                print(slotno)
        elif line.startswith('exit'):
            exit(0)

def main():

	parkinglot = ParkingLot()
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', action="store", required=False, dest='src_file', help="Input File")
	args = parser.parse_args()
	
	if args.src_file:
		with open(args.src_file) as f:
			for line in f:
				line = line.rstrip('\n')
				parkinglot.read_input(line)
	else:
			while True:
				line = input("$ ")
				parkinglot.read_input(line)

if __name__ == '__main__':
	main()