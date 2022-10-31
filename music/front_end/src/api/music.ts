// 获取音乐列表的接口
import request from "./request"
// /api/musics
export function reqMusicList() {
    return request({url: `/musics`, method: `get`})
}

// 查询单个
export function reqMusicListOne(id:number) {
    return request({url: `/musics/${id}`, method: `get`})
}

// 删除
export function reqDeleteMusic(id:number) {
    return request({url: `/musics/${id}`, method: `delete`})
}

// 增加或者修改
export function reqAddOrUpdateMusic(music:any, index:number){
    if (index != 0){
        return request({url:`musics/update/${index}`, method:'put', data:music})
    }else{
      //新增品牌
      return request({ url: '/musics', method: 'post', data: music });  
    }
}