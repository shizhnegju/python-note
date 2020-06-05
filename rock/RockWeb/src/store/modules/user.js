import { login, getInfo } from "@/api/login";
import { getToken, setToken, removeToken, getTicket, setTicket, removeTicket } from "@/utils/auth";
import { parseTime } from "@/utils/index";

const user = {
  state: {
    token: getToken(),
    ticket: "",
    id: "",
    name: "",
    username: "",
    email: "",
    avatar: "",
    createTime: "",
    roles: [],
    rolesName: [],
    environments: []
  },

  mutations: {
    SET_TOKEN: (state, token) => {
      state.token = token;
    },
    SET_TICKET: (state, ticket) => {
      state.ticket = ticket;
    },
    SET_ID: (state, id) => {
      state.id = id;
    },
    SET_NAME: (state, name) => {
      state.name = name;
    },
    SET_USERNAME: (state, username) => {
      state.username = username;
    },
    SET_AVATAR: (state, avatar) => {
      state.avatar = avatar;
    },
    SET_ROLES: (state, roles) => {
      state.roles = roles;
    },
    SET_ROLES_NAME: (state, rolesName) => {
      state.rolesName = rolesName;
    },
    SET_ENVIRONMENTS: (state, environments) => {
      state.environments = environments;
    },
    SET_CREATE_TIME: (state, createTime) => {
      state.createTime = createTime;
    },
    SET_EMAIL: (state, email) => {
      state.email = email;
    }
  },

  actions: {
    // 登录
    Login({ commit }, userInfo) {
      const username = userInfo.username;
      const password = userInfo.password;
      const rememberMe = userInfo.rememberMe;
      return new Promise((resolve, reject) => {
        login(username, password)
          .then(res => {
            setToken(res.detail.token, rememberMe);
            commit("SET_TOKEN", res.detail.token);
            resolve();
          })
          .catch(error => {
            reject(error);
          });
      });
    },

    // 获取用户信息
    GetInfo({ commit }) {
      return new Promise((resolve, reject) => {
        getInfo()
          .then(res => {
            commit("SET_ID", res.detail.id);
            commit("SET_ROLES", res.detail.roles);
            commit("SET_ROLES_NAME", res.detail.roles_name);
            commit("SET_ENVIRONMENTS", res.detail.environments);
            commit("SET_NAME", res.detail.name);
            commit("SET_USERNAME", res.detail.username);
            commit("SET_AVATAR", res.detail.avatar);
            commit("SET_EMAIL", res.detail.email);
            commit("SET_CREATE_TIME", parseTime(res.detail.createTime));
            resolve(res);
          })
          .catch(error => {
            reject(error);
          });
      });
    },

    // 登出
    LogOut({ commit }) {
      return new Promise((resolve, reject) => {
        commit("SET_TOKEN", "");
        commit("SET_ROLES", []);
        removeToken();
        resolve();
      });
    }
  }
};

export default user;
