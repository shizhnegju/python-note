import Cookies from "js-cookie";

const TokenKey = "Token";
const TicketKey = "Ticket";

export function getToken() {
  return Cookies.get(TokenKey);
}

export function getTicket() {
  return Cookies.get(TicketKey);
}

export function setToken(token, rememberMe) {
  if (rememberMe) {
    return Cookies.set(TokenKey, token, { expires: 1 });
  } else return Cookies.set(TokenKey, token);
}

export function setTicket(ticket) {
  return Cookies.set(TicketKey, ticket);
}

export function removeToken() {
  return Cookies.remove(TokenKey);
}

export function removeTicket() {
  return Cookies.remove(TicketKey);
}
