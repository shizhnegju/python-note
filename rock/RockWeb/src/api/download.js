import axios from 'axios'

// 获取所有的字典树
export function downloadRequest(url) {
  return axios.get(url,{
    responseType: 'blob'
})
}

