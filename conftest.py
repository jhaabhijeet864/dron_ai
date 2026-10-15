"""
Root conftest.py - pytest configuration for Dron-AI test suite.

Ensures pytest discovers tests across all domain-specific test directories:
    - ml_engine/tests/    (ML engine & preprocessing tests)
    - app/tests/          (Flask API & integration tests)
"""

import sys
import os
import pytest

# Add project root to sys.path so all imports resolve correctly from any test directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture(scope="session", autouse=True)
def test_model_fixture(tmp_path_factory):
    """
    Session-level deterministic model fixture.
    Ensures valid ML model artifacts and checksum sidecars exist for testing,
    especially in fresh CI checkouts where *.pkl binary models are gitignored.
    """
    # If caller already specified ML_MODEL_DIR, respect it
    if "ML_MODEL_DIR" in os.environ and os.path.isdir(os.environ["ML_MODEL_DIR"]):
        yield
        return

    # Train a fast, deterministic model into a temporary test directory
    temp_dir = tmp_path_factory.mktemp("test_models")
    import numpy as np
    import pandas as pd
    from ml_engine.xgboost_model import PlacementPredictor

    np.random.seed(42)
    n_samples = 40
    synthetic_data = {
        "Student_ID": [f"ST{i:04d}" for i in range(n_samples)],
        "CGPA": np.random.uniform(2.0, 4.0, n_samples),
        "Attendance_Percentage": np.random.uniform(60, 100, n_samples),
        "Programming_Skill": np.random.randint(1, 11, n_samples),
        "Problem_Solving": np.random.randint(1, 11, n_samples),
        "Projects_Completed": np.random.randint(0, 8, n_samples),
        "Communication_Skills": np.random.randint(1, 11, n_samples),
        "Internships": np.random.randint(0, 4, n_samples),
        "Hackathons": np.random.randint(0, 5, n_samples),
        "GitHub_Profile": np.random.choice(["Yes", "No"], n_samples),
        "Major": np.random.choice(["Computer Science", "Information Technology", "AI"], n_samples),
        "Placement_Status": np.random.choice(["Placed", "Not Placed"], n_samples, p=[0.6, 0.4]),
    }
    csv_path = str(temp_dir / "test_students.csv")
    pd.DataFrame(synthetic_data).to_csv(csv_path, index=False)

    model_path = str(temp_dir / "xgboost_placement.pkl")
    predictor = PlacementPredictor(n_estimators=5, max_depth=2, n_jobs=1)
    predictor.train(csv_path, save_path=model_path)

    os.environ["ML_MODEL_DIR"] = str(temp_dir)
    try:
        yield
    finally:
        os.environ.pop("ML_MODEL_DIR", None)
