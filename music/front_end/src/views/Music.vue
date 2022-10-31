<template>
  <div class="container">
    <h1 align="center">{{ "音乐列表" }}</h1>
    <br />
    <div align="center">
      <input type="text" v-model="music_id"> &nbsp;
      <button @click="getOne">查询</button> &nbsp;
      <button @click="showDialog">增加</button>
    </div>
    <!-- 表格 -->
    <el-table :data="music_list" style="width: 100%">
      <el-table-column prop="title" label="标题" width="" />
      <el-table-column prop="artist" label="作者" width="" />
      <el-table-column prop="duration" label="时长" width="100" />
      <el-table-column prop="last_play" label="最后播放时间" width="" />
      <el-table-column align="right">
        <template #default="scope">
          <el-button size="small" @click="handleEdit(scope.$index, scope.row)">Edit</el-button>
          <el-button size="small" type="danger" @click="handleDelete(scope.$index, scope.row)">Delete
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    <!-- 表单 -->
    <el-dialog v-model="dialogFormVisible" title="添加/修改品牌">
      <el-form :model="form">
        <el-form-item label="标题" :label-width="formLabelWidth">
          <el-input v-model="form.title" autocomplete="off" />
        </el-form-item>
        <el-form-item label="作者" :label-width="formLabelWidth">
          <el-input v-model="form.artist" autocomplete="off" />
        </el-form-item>
        <el-form-item label="时长" :label-width="formLabelWidth">
          <el-input v-model="form.duration" autocomplete="off" />
        </el-form-item>
        <el-form-item label="最后播放时间" :label-width="formLabelWidth">
          <el-input v-model="form.last_play" autocomplete="off" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogFormVisible = false">Cancel</el-button>
          <el-button type="primary" @click="addOrUpdateMusic"> Confirm</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts">
import { reactive, defineComponent, onMounted, toRefs, ref } from 'vue'
import { reqMusicList, reqDeleteMusic, reqAddOrUpdateMusic, reqMusicListOne } from '../api/music'
import { ElMessage, } from 'element-plus'

export default defineComponent({
  setup() {
    // 状态数据
    const state = reactive({
      music_list: [],
      index: 0,
      music_id:'',
      form: {
        title: '',
        artist: '',
        duration: '',
        last_play: ''
      }
    })

    // 函数相关的一些变量
    const dialogFormVisible = ref(false);
    const formLabelWidth = '140px';

    // 增加或者修改
    const addOrUpdateMusic = () => {
      dialogFormVisible.value = false;
      reqAddOrUpdateMusic(state.form, state.index).then(res => {
        if (res.status == 201) {
          ElMessage({ type: "success", message: "添加成功" });
          getList();
        } else if (res.status == 200) {
          ElMessage({ type: "success", message: "修改成功" });
          getList();
          // 初始化为0
          state.index = 0
        } else {
          ElMessage({ type: "error", message: "操作失败" });
        }
      })
    };

    // 删除
    const handleDelete = (index: number, row: any) => {
      reqDeleteMusic(index + 1).then(res => {
        if (res.status == 200) {
          ElMessage({ type: "success", message: "删除成功" });
          // 重新加载列表
          getList()
        }
      })
    };
    // 查询所有
    const getList = () => {
      reqMusicList().then(res => {
        console.log(res)
        state.music_list = res.data;
      })
    };
    // 查询单个
    const getOne = () => {
            if (state.music_id != '0') {
                reqMusicListOne(parseInt(state.music_id)).then(res => {
                    state.music_list = res.data;
                })
            } else {
                ElMessage({ type: "error", message: "id异常" });
            }

        };

    //自定义的一些其它函数
    const handleEdit = (index: number, row: any) => {
      state.index = index + 1;
      dialogFormVisible.value = true;
      state.form = {
        title: '',
        artist: '',
        duration: '',
        last_play: ''
      }
    };
    const showDialog = () => {
      dialogFormVisible.value = true;
      state.index = 0;
      state.form = {
        title: '',
        artist: '',
        duration: '',
        last_play: ''
      }
    }

    // 初始挂载，自带
    onMounted(() => {
      getList();
    });

    // 返回数据
    return {
      ...toRefs(state),
      formLabelWidth,
      dialogFormVisible,
      handleEdit,
      handleDelete,
      showDialog,
      addOrUpdateMusic,
      getOne
    }
  }
})
</script>

<style scoped>

</style>