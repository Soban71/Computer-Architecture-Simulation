class MemorySubsystem:
    def __init__(self, size):
        self.size = size
        self.memory = [0] * size

    def read_memory(self, address):
        if 0 <= address < self.size:
            return self.memory[address]
        else:
            raise ValueError("Invalid memory address")

    def write_memory(self, address, value):
        if 0 <= address < self.size:
            self.memory[address] = value
        else:
            raise ValueError("Invalid memory address")

    def load_initial_data(self, data):
        if len(data) <= self.size:
            self.memory[:len(data)] = data
        else:
            raise ValueError("Data size exceeds memory size")

memory = MemorySubsystem(size=100)

initial_data = [1, 2, 3, 10, 5]
memory.load_initial_data(initial_data)

value_at_address_3 = memory.read_memory(3)
print("Value at address 3:", value_at_address_3)

memory.write_memory(6, 15)
new_value_at_address_6 = memory.read_memory(6)
print("New value at address 6:", new_value_at_address_6)
