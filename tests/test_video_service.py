from backend.services.video_service import VideoService

service = VideoService()

video = input("Enter Video Path : ")

metadata = service.create_lecture(video)

print()

print("=" * 60)

print("LECTURE CREATED")

print("=" * 60)

for key, value in metadata.items():

    print(f"{key} : {value}")