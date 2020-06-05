import request from "@/utils/request";

export function getKeys(params) {
  return request({
    url: "api/keys/",
    method: "get",
    params
  });
}

export function add(data) {
  return request({
    url: "api/keys/",
    method: "post",
    data
  });
}

export function del(id) {
  return request({
    url: "api/keys/" + id + "/",
    method: "delete"
  });
}

export function retrieve(id) {
  return request({
    url: "api/keys/" + id + "/",
    method: "get"
  });
}

export function edit(id, data) {
  return request({
    url: "api/keys/" + id + "/",
    method: "put",
    data
  });
}
