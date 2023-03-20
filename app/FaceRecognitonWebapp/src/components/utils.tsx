import { GpuBuffer } from "@mediapipe/face_detection"
import { RefObject } from "react"

export interface Point {
    x: number,
    y: number,
}
export interface BoundingBox {
    height: number
    rectId: number
    rotation: number
    width: number
    xCenter: number
    yCenter: number
}
export interface OriginShape {
    width: number,
    height: number,
}

const x = [-1, 1, 1, - 1];
const y = [-1, - 1, 1, 1];
export function drawBoundingBox(ctx: CanvasRenderingContext2D, boundingBox: BoundingBox, originShape: OriginShape) {
    const xCenter = boundingBox.xCenter * originShape.width;
    const yCenter = boundingBox.yCenter * originShape.height;
    const boxWidth = boundingBox.width * originShape.width;
    const boxHeight = boundingBox.height * originShape.height;
    const arr: Point[] = [];
    for (let i = 0; i < 4; i++) {
        arr.push({
            x: xCenter + boxWidth * 0.5 * x[i],
            y: yCenter + boxHeight * 0.5 * y[i]
        })

    }

    lineLoop(ctx, arr);
}
export function lineLoop(ctx: CanvasRenderingContext2D, arr: Point[], style?: { color: string, lineWidth: number }) {

    const color = style ? style.color : "#1a7915"
    const lineWidth = style ? style.lineWidth : 2;
    if (arr.length < 1) return;
    ctx.moveTo(arr[0].x, arr[0].y);
    for (let i = 1; i < arr.length; i++) {
        ctx.lineTo(arr[i].x, arr[i].y);
    }
    ctx.lineTo(arr[0].x, arr[0].y);
    ctx.strokeStyle = color;
    ctx.lineWidth = lineWidth;
    ctx.stroke();
}

export interface circleStyle {
    radius: number,
    color: string
}
export function point(ctx: CanvasRenderingContext2D, point: Point, style?: circleStyle) {
    const radius = style ? style.radius : 2;
    const color = style ? style.color : "red";
    ctx.beginPath();
    ctx.arc(point.x, point.y, radius, 0, 2 * Math.PI, true);
    ctx.fillStyle = color;
    ctx.fill();
}

export interface fontStyle {
    size: number;
    name: string;
    color: string;
}

export function writeTex(ctx: CanvasRenderingContext2D, obj: any, xStart: number, yStart: number, font?: fontStyle) {
    ctx.font = font ? `${font.size}px ${font.name}` : "16px Georgia";
    ctx.fillStyle = font ? font.color : "black";
    let i = 1;

    for (const [key, value] of Object.entries(obj)) {
        ctx.beginPath()
        ctx.fillText(`${key} : ${value}`, xStart, yStart * i * 2 + xStart / 2);
        ctx.closePath()
        i = i + 1;
    }

}

export function extractFace(face: RefObject<HTMLCanvasElement>, input: GpuBuffer, boundingBox: BoundingBox) {
    if (!face.current) return ""
    const faceCropped = face.current;

    const ctx = faceCropped?.getContext('2d');
    if (!ctx) return "";



    //https://i.stack.imgur.com/LNgjx.png
    // drawImage(image,
    //     sx, sy, sw, sh,
    //     dx, dy, dw, dh);


    const boxWidth = boundingBox.width * input.width;
    const boxHeight = boundingBox.height * input.height;

    const xCenter = boundingBox.xCenter * input.width;
    const yCenter = boundingBox.yCenter * input.height;
    face.current.width = boxWidth;
    face.current.height = boxHeight;
    ctx.save();
    ctx.clearRect(0, 0, boxWidth, boxHeight);
    ctx.drawImage(input, xCenter - boxHeight * 0.5, yCenter - boxWidth * 0.5, boxWidth, boxHeight, 0, 0, boxWidth, boxHeight);

    return face.current.toDataURL()

}

export function downloadImageBase64(img: string) {
    var a = document.createElement("a"); //Create <a>
    a.href = img; //Image Base64 Goes here
    a.download = new Date().getTime() + ".png"; //File name Here
    a.click(); //Downloaded file
}

