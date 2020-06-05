import request from '@/utils/request'

export function getDiscern() {
  return request({
    url: 'api/img_discern/',
    method: 'get'
  })
}

export function getAccuracyRate() {
  return request({
    url: 'api/accuracy/rate/',
    method: 'get'
  })
}

export function retrieve(id) {
  return request({
    url: 'api/img_discern/' + id + '/',
    method: 'get'
  })
}

export function add(data) {
  return request({
    url: 'api/dicts/',
    method: 'post',
    data
  })
}

export function del(id) {
  return request({
    url: 'api/img_discern/' + id + '/',
    method: 'delete'
  })
}

export function edit(id, data) {
  return request({
    url: 'api/img_discern/' + id + '/',
    method: 'put',
    data
  })
}

export function editPatch(id, data) {
  return request({
    url: 'api/img_discern/' + id + '/',
    method: 'patch',
    data
  })
}
