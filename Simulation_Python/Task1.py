class CPU:
    def __init__(self, num_registers):
        self.registers = [0] * num_registers
        self.program_counter = 0
        self.halted = False

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

    def execute_instruction(self, instruction):
        opcode, *operands = instruction.split()
        if opcode == "LOAD":
            register, value = map(int, operands)
            self.registers[register] = value
        elif opcode == "ADD":
            register1, register2, destination = map(int, operands)
            self.registers[destination] = self.registers[register1] + self.registers[register2]
        elif opcode == "STORE":
            register, address = map(int, operands)
            memory[address] = self.registers[register]
        elif opcode == "HALT":
            self.halted = True

program = [
    "LOAD 0 10",
    "LOAD 1 60",
    "ADD 0 1 2",
    "STORE 2 30",
    "HALT",
]

memory = [0] * 100


cpu = CPU(num_registers=3)


while not cpu.halted:
    instruction = cpu.fetch_instruction(program)
    if instruction:
        cpu.execute_instruction(instruction)

# Display final state
print("Final CPU Registers:", cpu.registers)
print("Final Memory:", memory)
