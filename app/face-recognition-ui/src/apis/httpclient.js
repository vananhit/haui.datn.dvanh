import axios from "axios";

const token = localStorage.getItem('token')
export  const httpClient = axios.create({
    baseURL: `http://127.0.0.1:8000/api/v1/`,
    headers: {
      Authorization: `Bearer ${token}`
    }
  })