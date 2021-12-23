from lms import VideoItem, CompositeLearningItem, Quiz, ProgrammingAssigment


def test_composite_work():
    video_item_1 = VideoItem(name="Compoite Design Pattern",length=20)
    video_item_2 = VideoItem(name="Compoite Design Pattern v.2",length=10)
    lesson_composite = CompositeLearningItem(name="lesson on composite")
    lesson_composite.add(video_item_1)
    lesson_composite.add(video_item_2)
    expected_composite_study_tite = (20 * 1.5 + 10 * 1.5)
    assert expected_composite_study_tite == lesson_composite.estimate_study_time()

    video_item_3 = VideoItem(name="Adapter Design Pattern",length=20)
    quiz = Quiz(name="Adapter Design Pattern Quiz", questions=["a", "b", "c"])
    lesson_adapter = CompositeLearningItem(name="lesson on adapter", learning_items=[video_item_3, quiz])
    expected_adapter_study_tite = (20 * 1.5 + 5 * 3)
    assert expected_adapter_study_tite == lesson_adapter.estimate_study_time()

    module_design_pattern = CompositeLearningItem(name="Design Pattern", learning_items=[lesson_composite, lesson_adapter])
    module_design_pattern. add(
        ProgrammingAssigment(name="Factory Method Programming Assignment", language="python")
    )
    expected_module_design = expected_composite_study_tite + expected_adapter_study_tite + 120
    assert expected_module_design == module_design_pattern.estimate_study_time()

