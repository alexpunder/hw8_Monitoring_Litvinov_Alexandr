from time import sleep

import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from evidently import Report
from evidently.ui.workspace import RemoteWorkspace
from evidently.presets import DataDriftPreset, DataSummaryPreset

np.random.seed(42)

iris = load_iris(as_frame=True)
df = iris.frame

reference_data, current_good = train_test_split(
    df,
    test_size=0.4,
    random_state=42,
)

current_bad = df.iloc[50:100].copy()


current_bad["sepal length (cm)"] = (
    current_bad["sepal length (cm)"] * 2.5
    + np.random.normal(0, 0.5, current_bad.shape[0])
)
current_bad["sepal width (cm)"] = np.random.normal(2.0, 0.2, current_bad.shape[0])

ws = RemoteWorkspace("http://localhost:8090/")

project = ws.create_project(
    name="ml_service",
    description="drift",
)

project.save()

def create_and_save_report(ref_data, cur_data):
    report = Report(
        metrics=[
            DataDriftPreset(drift_share=0.5, method="psi"),
            DataSummaryPreset(),
        ],
    )

    snapshot = report.run(reference_data=ref_data, current_data=cur_data)
    ws._add_run(project.id, snapshot)


create_and_save_report(reference_data, current_good.sample(30))

sleep(3)

create_and_save_report(reference_data, current_bad)

sleep(3)

print("Отчеты по адресу: http://localhost:8090")
