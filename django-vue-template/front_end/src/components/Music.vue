<template>
    <div>

    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import {reqMusicList} from '../api/music'

export default defineComponent({
    setup () {
        reqMusicList(2).then((res)=>{
            console.log(res)
        })
        return {}
    }
})
</script>

<style scoped>

</style>