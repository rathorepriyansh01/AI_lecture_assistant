from backend.services.audio_service import AudioService

lecture_id = input("Lecture ID : ")

service = AudioService()

metadata = service.process(lecture_id)

print()

print("=" * 60)

print("AUDIO EXTRACTED")

print("=" * 60)

print(metadata["files"]["audio_path"])

print(metadata["statistics"]["audio_duration"])