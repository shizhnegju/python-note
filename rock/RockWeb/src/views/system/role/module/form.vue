<template>
  <el-dialog
    :append-to-body="true"
    :visible.sync="dialog"
    :title="isAdd ? '新增角色' : '编辑角色'"
    width="500px"
  >
    <el-form ref="form" :model="form" :rules="rules" size="small" label-width="66px">
      <el-form-item label="名称" prop="name">
        <el-input v-model="form.name" style="width: 370px;" />
      </el-form-item>
      <el-form-item label="描述">
        <el-input v-model="form.desc" style="width: 370px;" rows="5" type="textarea" />
      </el-form-item>
    </el-form>
    <div slot="footer" class="dialog-footer">
      <el-button type="text" @click="cancel">取消</el-button>
      <el-button :loading="loading" type="primary" @click="doSubmit">确认</el-button>
    </div>
  </el-dialog>
</template>

<script>
import { add, save as edit } from "@/api/role";
import { getKey } from "@/api/dict";
export default {
  props: {
    isAdd: {
      type: Boolean,
      required: true
    },
    sup_this: {
      type: Object,
      default: null
    },
  },
  data() {
    return {
      loading: false,
      dialog: false,
      form: { name: "", desc: "", environment: [] },
      rules: {
        name: [{ required: true, message: "请输入名称", trigger: "blur" }]
      }
    };
  },
  methods: {
    cancel() {
      this.resetForm();
    },
    doSubmit() {
      this.$refs["form"].validate(valid => {
        if (valid) {
          this.loading = true;
          if (this.isAdd) {
            this.doAdd();
          } else this.doEdit();
        } else {
          return false;
        }
      });
    },
    doAdd() {
      add(this.form)
        .then(res => {
          this.resetForm();
          this.$message({
            showClose: true,
            type: "success",
            message: "添加成功!",
            duration: 2500
          });
          this.loading = false;
          this.$parent.$parent.init();
        })
        .catch(err => {
          this.loading = false;
          console.log(err);
        });
    },
    doEdit() {
      const data = Object.assign({}, this.form);
      delete data.permissions;
      delete data.menus;
      edit(this.form.id, data)
        .then(res => {
          this.resetForm();
          this.$message({
            showClose: true,
            type: "success",
            message: "修改成功!",
            duration: 2500
          });
          this.loading = false;
          this.sup_this.init();
        })
        .catch(err => {
          this.loading = false;
          console.log(err);
        });
    },
    resetForm() {
      this.dialog = false;
      this.$refs["form"].resetFields();
      this.form = { name: "", desc: ""};
    }
  }
};
</script>

<style scoped>
</style>
