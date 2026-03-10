from src.main import *
import pytest, json

def test_run_tasks(tmp_path):
    """Test that all task sources return valid Task objects"""

    data = [
        {
            "id": 1,
            "payload": {
            "order_id": 5501,
            "amount": 1200
            }
        },
        {
            "id": 2,
            "payload": {
            "order_id": 5502,
            "amount": 450
            }
        },
        {
            "id": 3,
            "payload": {
            "order_id": 5503,
            "amount": 3100
            }
        }
    ]

    dir = tmp_path/"data".mkdir()
    file = dir/"data.json"
    
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f)

    sources =[GeneratorTaskSource(), ApiTaskSource(), FileTaskSource(file)]

    for source in sources:
        tasks = run_tasks(source)
        assert all(isinstance(task, Task) for task in tasks)


def test_wrong_source():
    """Test run_tasks with invalid source"""

    with pytest.raises(TypeError) as err:
        run_tasks("invalid_source")
    assert "does not match contract TaskSource" in str(err.value)

def test_file_task_source_not_found():
    """Test FileTaskSource with non-existent file"""

    source = FileTaskSource("missing.json")

    with pytest.raises(ValueError) as err:
        source.get_tasks()
    
    assert "Error" in str(err.value)
