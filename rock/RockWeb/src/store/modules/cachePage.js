const cache = {
  state: {
    cachePages: []
  },
  mutations: {
    SET_CACHE_PAGE: (state, componentName) => {
      if (state.cachePages.indexOf(componentName) === -1) {
        state.cachePages.push(componentName)
      }
    },
    DEL_CACHE_PAGE: (state, componentName) => {
      const position = state.cachePages.indexOf(componentName)
      if (position > -1) {
        state.cachePages.splice(position, 1)
      }
    },
    CLEAR_CACHE_PAGES: (state) => {
      state.cachePages = []
    }
  },
  actions: {
    setCachePage ({ commit }, componentName) {
      commit('SET_CACHE_PAGE', componentName)
    },
    delCachePage ({ commit }, componentName) {
      commit('DEL_CACHE_PAGE', componentName)
    },
    clearCachePages ({ commit }) {
      commit('CLEAR_CACHE_PAGES')
    }
  }
}

export default cache
