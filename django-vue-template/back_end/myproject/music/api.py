from typing import List
from ninja import NinjaAPI
from music.models import Music
from music.schme import MusicSchema, NotFoundSchema

api = NinjaAPI()


# 查询所有
@api.get("/musics", response=List[MusicSchema])
def musics(request):
    return Music.objects.all()


# 根据id查询
@api.get("/musics/{music_id}", response={200: MusicSchema, 404: NotFoundSchema})
def musics(request, music_id: int):
    try:
        music = Music.objects.get(pk=music_id)
        return music
    except Music.DoesNotExist as e:
        return 404, {"message": "Music does not exist"}


# 创建
@api.post("/musics", response={201: MusicSchema})
def create_music(request, music: MusicSchema):
    Music.objects.create(**music.dict())
    return music


# 更新数据
@api.put("musics/update/{music_id}", response={200: MusicSchema, 404: NotFoundSchema})
def change_music(request, music_id: int, data: MusicSchema):
    try:
        music = Music.objects.get(pk=music_id)
        for attribute, value in data.dict().items():
            setattr(music, attribute, value)
        music.save()
        return 200, music
    except Music.DoesNotExist as e:
        return 404, {"message": "Music does not exist"}


# 删除数据
@api.delete("/musics/{music_id}", response={200: None, 404: NotFoundSchema})
def delete_Music(request, music_id: int):
    try:
        music = Music.objects.get(pk=music_id)
        music.delete()
        return 200
    except Music.DoesNotExist as e:
        return 404, {"message": "Could not find Music"}
