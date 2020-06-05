<template>
  <div class="head-container">
    <!-- 导出 -->
    <el-button
      v-if="checkPermission(['admin'])"
      :loading="downloadLoading"
      size="mini"
      class="filter-item"
      type="primary"
      icon="el-icon-download"
      @click="download"
    >导出
    </el-button>
  </div>
</template>

<script>
  import checkPermission from "@/utils/permission"; // 权限判断函数
  import {parseTime} from "@/utils/index";
  // 查询条件
  export default {
    props: {
      query: {
        type: Object,
        required: true
      }
    },
    data() {
      return {
        downloadLoading: false
      };
    },
    methods: {
      checkPermission,
      toQuery() {
        this.$parent.page = 1;
        this.$parent.init();
      },
      download() {
        this.downloadLoading = true;
        import("@/vendor/Export2Excel").then(excel => {
          const tHeader = ["课程名称", "授课老师", "签到人", "签到时间", "唯一ID"];
          const filterVal = ["title", "teacher", "singner", "created_time", "unid"];
          const data = this.formatJson(filterVal, this.$parent.data);
          excel.export_json_to_excel({
            header: tHeader,
            data,
            filename: "table-list"
          });
          this.downloadLoading = false;
        });
      },
      formatJson(filterVal, jsonData) {
        return jsonData.map(v =>
          filterVal.map(j => {
            if (j === "createTime") {
              return parseTime(v[j]);
            } else {
              return v[j];
            }
          })
        );
      }
    }
  };
</script>
