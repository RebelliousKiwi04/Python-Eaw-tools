test = {
    func1 = function(self)
        print("Test")
        print(self.string)
    end,
    string = 'hi'
}


test:func1()
print("Finished")