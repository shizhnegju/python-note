export default {
  methods: {
    getDefaultEnv() {
      let environment = "all";
      const status = [];
      this.$store.state.user.rolesName.forEach(item => {
        if (item.indexOf("开发") > -1) {
          status.push("dev");
        } else if (item.indexOf("测试") > -1) {
          status.push("test");
        }
      });
      if (status.indexOf("dev") > -1 && status.indexOf("test") > -1) {
        environment = "all";
      } else if (status.indexOf("dev") > -1) {
        environment = "dev";
      } else if (status.indexOf("test") > -1) {
        environment = "test";
      } else {
        environment = "all";
      }
      return environment;
    }
  }
};
