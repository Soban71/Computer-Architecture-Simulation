class IODevice:
    def __init__(self):
        self.data = None

    def read_data(self):
        if self.data is not None:
            data_to_return = self.data
            self.data = None 
            return data_to_return
        else:
            return None

io_device = IODevice()

io_device.data = "Hello, I/O Device checking example"

read_data_result = io_device.read_data()

print("Data read from I/O Device:", read_data_result)
