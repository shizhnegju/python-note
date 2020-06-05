import request from '@/utils/request'

export function terminate(data) {
  return request({
    url: 'api/terminate/task/',
    method: 'post',
    data
  })
}
