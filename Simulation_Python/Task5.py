class BusSystem:
    def __init__(self):
        self.connected_devices = []

    def connect(self, device):
        self.connected_devices.append(device)

    def transfer_data(self, source, destination, data):
        if source in self.connected_devices and destination in self.connected_devices:
            print(f"Transferring data from {source.__class__.__name__} to {destination.__class__.__name__}: {data}")
            destination.receive_data(data)
        else:
            print("Error: Source or destination not connected to the bus.")


class CPU:
    def __init__(self, num_registers, bus_system):
        self.registers = [0] * num_registers
        self.program_counter = 0
        self.halted = False
        self.bus_system = bus_system

    def read_register(self, register):
        return self.registers[register]

    def write_register(self, register, value):
        self.registers[register] = value

    def fetch_instruction(self, program):
        if self.program_counter < len(program):
            instruction = program[self.program_counter]
            self.program_counter += 1
            return instruction
        else:
            return None

    def execute_instruction(self, instruction, memory, io_device):
        opcode, *operands = instruction.split()
        if opcode == "LOAD":
            register, value = map(int, operands)
            self.registers[register] = value
        elif opcode == "ADD":
            register1, register2, destination = map(int, operands)
            self.registers[destination] = self.registers[register1] + self.registers[register2]
        elif opcode == "STORE":
            register, address = map(int, operands)
            memory.write_memory(address, self.registers[register])
        elif opcode == "READ_IO":
            register = int(operands[0])
            data_from_io = io_device.read_data()
            if data_from_io is not None:
                self.registers[register] = data_from_io
        elif opcode == "WRITE_IO":
            register = int(operands[0])
            io_data = self.registers[register]
            io_device.receive_data(io_data)
        elif opcode == "PRINT":
            register = int(operands[0])
            print(f"Print from CPU: {self.registers[register]}")
        elif opcode == "HALT":
            self.halted = True

    def send_data(self, data, destination):
        self.bus_system.transfer_data(self, destination, data)


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

    def receive_data(self, data):
        print(f"Memory received data: {data}")
        address, value = data
        self.write_memory(address, value)


class IODevice:
    def __init__(self):
        self.data = None

    def read_data(self):
        return self.data

    def receive_data(self, data):
        print(f"IO Device received data: {data}")
        self.data = data


def load_instructions(program, cpu, memory):
    memory.load_initial_data(program)


def run_simulation(cpu, memory, io_device, bus_system, num_cycles):
    for cycle in range(num_cycles):
        print(f"\nCycle {cycle + 1}")
        instruction = cpu.fetch_instruction(memory.read_memory(cpu.program_counter))
        if instruction is not None:
            print(f"Executing instruction: {instruction}")
            cpu.execute_instruction(instruction, memory, io_device)
            print(f"CPU Registers: {cpu.registers}")
            print(f"Memory State: {memory.memory}")
            print(f"IO Device State: {io_device.data}")
            print(f"Program Counter: {cpu.program_counter}")
            if cpu.halted:
                print("CPU halted.")
                break


bus_system = BusSystem()
cpu = CPU(num_registers=4, bus_system=bus_system)
memory = MemorySubsystem(size=100)
io_device = IODevice()

bus_system.connect(cpu)
bus_system.connect(memory)
bus_system.connect(io_device)

program = [
    "LOAD 0 10",
    "ADD 0 1 2",
    "STORE 2 5",
    "READ_IO 3",
    "WRITE_IO 3",
    "PRINT 2",
    "HALT"
]

load_instructions(program, cpu, memory)

run_simulation(cpu, memory, io_device, bus_system, num_cycles=5)
