export function mask(){
    document.querySelector("#app-loading").style.visibility ='visible'
}
export function unMask(){
    document.querySelector("#app-loading").style.visibility ='hidden'
}

export function parseJwt() {
    let token = localStorage.getItem("token");
    let base64Url = token.split(".")[1];
    let base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
    let jsonPayload = decodeURIComponent(
      window
        .atob(base64)
        .split("")
        .map(function (c) {
          return "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2);
        })
        .join("")
    );

    return JSON.parse(jsonPayload);
  }