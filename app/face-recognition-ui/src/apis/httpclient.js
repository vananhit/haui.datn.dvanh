import axios from "axios";

const token = localStorage.getItem('token')
export  const httpClient = axios.create({
    baseURL: `${window.__config.host_base}`,
    headers: {
      Authorization: `Bearer ${token}`
    }
  })