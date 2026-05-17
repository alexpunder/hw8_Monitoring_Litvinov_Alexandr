from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.queue import Kafka
from diagrams.programming.language import Python
from diagrams.aws.storage import S3
from diagrams.onprem.client import User


with Diagram("ML-system for Virtual Product Placement", show=False, direction="LR"):

    user = User("Отправляем запрос")

    with Cluster("Слой хранения данных"):
        storage = S3("Хранилище\n(видео, лого, модель)")

    with Cluster("Используем потоки данных (stream) и Kappa архитектуру: брокер + воркеры"):
        
        broker = Kafka("Брокер")
        
        with Cluster("Воркеры с логикой обработки"):
            detector = Python("YOLO -\nнаходим человека")
            placer = Python("Наложение логотипа\nбренда")

    user >> Edge(label="Запрос на обработку") >> broker
    broker >> Edge(label="Кадры для обработки") >> detector

    detector >> placer

    detector << Edge(label="Чтение видео", style="dashed") << storage
    placer << Edge(label="Чтение логотипов", style="dashed") << storage
    placer >> Edge(label="Сохранение кадров") >> storage

    storage >> Edge(label="Готовый результат") >> user
