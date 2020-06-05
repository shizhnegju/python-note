export default {
  methods: {
    hasEnvironmentAuth(environment) {
      if (this.$store.getters.roles.indexOf("admin") > -1) {
        return true;
      }
      return this.$store.getters.environments.indexOf(environment) > -1;
    },
    getDefaultEnv() {
      const getters = this.$store.getters;
      if (getters.roles.indexOf("admin") > -1) {
        return "all";
      }
      const { environments = [] } = getters;
      if (environments.length > 0) {
        return environments[0];
      } else {
        return "all";
      }
    }
  }
};
