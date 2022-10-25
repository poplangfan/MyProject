// 获取音乐列表的接口
import service from "./request"
// /api/musics
export function reqMusicList(music_id: number) {
    return service({url: `/musics/${music_id}`, method: `get`})
}