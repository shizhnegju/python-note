const getters = {
  sidebar: state => state.app.sidebar,
  device: state => state.app.device,
  token: state => state.user.token,
  avatar: state => state.user.avatar,
  visitedViews: state => state.tagsView.visitedViews,
  cachedViews: state => state.tagsView.cachedViews,
  cachePages: state => state.cache.cachePages,
  id: state => state.user.id,
  name: state => state.user.name,
  createTime: state => state.user.createTime,
  email: state => state.user.email,
  roles: state => state.user.roles,
  environments: state => state.user.environments,
  compileInfo: state => state.compile.compileInfo,
  permission_routers: state => state.permission.routers,
  addRouters: state => state.permission.addRouters,
};
export default getters;
