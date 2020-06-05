import moment from "moment";

const dateTimeFormat = function(time, fmt) {
  return moment(time).format(fmt);
};

export function date(value) {
  if (value) {
    return dateTimeFormat(value, "YYYY-MM-DD");
  } else {
    return "-";
  }
}

export function time(value) {
  if (value) {
    return dateTimeFormat(value, "YYYY-MM-DD HH:mm:ss");
  } else {
    return "-";
  }
}

export function minute(value) {
  if (value) {
    return dateTimeFormat(value, "YYYY-MM-DD HH:mm");
  } else {
    return "-";
  }
}

export function filterEnv(value) {
  switch (value) {
    case "dev":
      return "开发环境";
    case "test":
      return "测试环境";
    case "prod":
      return "生产环境";
    case "gamma":
      return "预发布环境";
    case "dr":
      return "容灾环境";
    default:
      return value;
  }
}
