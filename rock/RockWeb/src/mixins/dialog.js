export default {
  data() {
    return {
      dialogOption: {
        view: null,
        title: "",
        visible: false,
        width: ""
      }
    };
  },
  methods: {
    showDynamicDialog(view, title, width = "480px") {
      this.dialogOption.view = view;
      this.dialogOption.title = title;
      this.dialogOption.visible = true;
      this.dialogOption.width = width;
    },
    closeDynamicDialog() {
      this.dialogOption.view = null;
      this.dialogOption.title = "";
      this.dialogOption.visible = false;
      this.dialogOption.width = "";
    }
  }
};
