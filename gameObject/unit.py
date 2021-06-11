
class Unit:
    def __init__(self, xml_entry, file):
        self.entry = xml_entry
        self.fileLocation = file
        self.aicp = self.get_aicp()
        self.name = self.get_name()
        self.category_masks = self.get_category_masks()
        self.variant = self.set_variant()
        self.type = self.entry.tag
    def get_aicp(self) -> int:
        for item in self.entry:
            if item.tag == 'AI_Combat_Power':
                print(item.text)
                return int(item.text)
        return 0
    def get_name(self) -> str:
        return self.entry.get('Name')
    def get_category_masks(self):
        for item in self.entry:
            if item.tag == 'CategoryMask':
                outputList = []
                for text in item.text.split():
                    newText = text.replace('|','')
                    if len(newText) > 3:
                        outputList.append(newText)
                        print(newText)
                return outputList
    def set_variant(self):
        for item in self.entry:
            if item.tag == 'Variant_Of_Existing_Type':
                return item.text
        return None
    