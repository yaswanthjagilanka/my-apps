class NainaInput:

    def __init__(self, user, data, type_data):
        self.user = user
        self.data = data
        self.type_data = type_data

    def input_engine(self):
        pass

    def input_text(self):
        pass

    def input_audio(self):
        #####convert to text#####
        #####user identification#####
        pass

    def input_video(self):
        pass

    def input_image(self):
        pass


class NainaOutput:

    def __init__(self, user, data, type_data):
        self.user = user
        self.data = data
        self.type = type_data

    def output_engine(self):
        pass

    def output_text(self):
        pass

    def output_audio(self):
        pass

    def output_video(self):
        pass

    def output_image(self):
        pass
