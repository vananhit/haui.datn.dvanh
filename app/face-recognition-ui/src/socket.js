
import { io } from "socket.io-client";





export const socket = io('ws://localhost:8000', {
    autoConnect: false,
    transports: ["websocket"]
  });

socket.on("connect", () => {
  console.log("connected")
});

socket.on("disconnect", () => {
    console.log("disconnected")
});

