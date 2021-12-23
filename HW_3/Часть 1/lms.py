from abc import ABC, abstractclassmethod

class LearningItem(ABC):
    def __init__(self, name):
        self.name = name
    @abstractclassmethod
    def estimate_study_time(self):
        raise NotImplementedError

class VideoItem(LearningItem):
    def __init__(self, name, length):
        super().__init__(name)
        self.length = length
    
    def estimate_study_time(self):
        return 1.5 * self.length


class Quiz(LearningItem):
    def __init__(self, name, questions):
        super().__init__(name)
        self.questions = questions
    
    def estimate_study_time(self):
        return 5 * len(self.questions)


class ProgrammingAssigment(LearningItem):
    def __init__(self, name, language):
        super().__init__(name)
        self.language = language
    
    def estimate_study_time(self):
        return 120

class CompositeLearningItem(LearningItem):
    def __init__(self, name, learning_items=None):
        super().__init__(name)
        self.learning_items = []
        self.learning_items.extend(learning_items or [])

    def add(self, learning_item):
        self.learning_items.append(learning_item)

    def estimate_study_time(self):
        for learning_item in self.learning_items:
            print (learning_item)

        study_time = sum(
            learning_item.estimate_study_time()
            for learning_item in self.learning_items
        )
        return study_time

def main():
    pass
    #course = ??()
    #course.add(...)
    video_item_1 = VideoItem(name="Compoite Design Pattern",length=20)
    video_item_2 = VideoItem(name="Compoite Design Pattern v.2",length=10)
    lesson_composite = CompositeLearningItem(name="lesson on composite")
    lesson_composite.add(video_item_1)
    lesson_composite.add(video_item_2)

    video_item_3 = VideoItem(name="Adapter Design Pattern",length=20)
    quiz = Quiz(name="Adapter Design Pattern Quiz", questions=["a", "b", "c"])
    lesson_adapter = CompositeLearningItem(name="lesson on adapter", learning_items=[video_item_3, quiz])

    module_design_pattern = CompositeLearningItem(name="Design Pattern", learning_items=[lesson_composite, lesson_adapter])
    module_design_pattern. add(
        ProgrammingAssigment(name="Factory Method Programming Assignment", language="python")
    )
