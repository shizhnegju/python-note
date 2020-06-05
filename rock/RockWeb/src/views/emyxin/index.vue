<template>
  <div class="app-container">
    <eHeader :query="query"/>
    <el-row :gutter="28">
      <el-col :span="span">
        <!--表格渲染-->
        <el-table
          v-loading="loading"
          :data="data"
          size="small"
          border
          style="width: 100%;"
        >
          <el-table-column label="序号" width="60" align="center">
            <template slot-scope="scope">
              <div>{{ scope.$index + 1 }}</div>
            </template>
          </el-table-column>
          <el-table-column prop="title" label="课程名称"/>
          <el-table-column prop="teacher" label="授课老师"/>
          <el-table-column prop="singner" label="签到人"/>
          <el-table-column prop="created_time" label="签到时间"/>
          <el-table-column prop="unid" label="唯一ID"/>
        </el-table>
        <!--分页组件-->
        <el-pagination
          :total="total"
          style="margin-top: 8px;"
          layout="total, prev, pager, next, sizes"
          @size-change="sizeChange"
          @current-change="pageChange"
        />
      </el-col>
    </el-row>
  </div>
</template>

<script>
  import checkPermission from "@/utils/permission";
  import initData from "@/mixins/initData";
  import {parseTime} from "@/utils/index";
  import eHeader from "./module/header";

  export default {
    components: {eHeader},
    mixins: [initData],
    data() {
      return {
        row_data: null,
        span: 24,
        show: false,
        is_permissions: false,
        table_show: true,
        Loading: false,
        sup_this: this,
        permission_list: [],
        menu_list: [],
        permissionIds: [],
        menuIds: [],
        defaultProps: {
          children: "children",
          label: "label"
        }
      };
    },
    async created() {
      this.$nextTick(() => {
        this.init();
      });
    },
    methods: {
      parseTime,
      checkPermission,
      beforeInit() {
        this.url = "/checkin/";
        const sort = "id";
        const query = this.query;
        const value = query.value;
        this.params = {page: this.page, size: this.size, ordering: sort};
        if (value) {
          this.params["search"] = value;
        }
        return true;
      },
    }
  };
</script>

<style>
  .el-card__header {
    font-size: 14px;
  }
</style>
