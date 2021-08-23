package models

import (
	"fmt"
	"log"
	"net/http"

	"github.com/go-httpproxy/httpproxy"
)

func OnError(ctx *httpproxy.Context, where string,
	err *httpproxy.Error, opErr error) {
	// Log errors.
	log.Printf("ERR: %s: %s [%s]", where, err, opErr)
}

func OnAccept(ctx *httpproxy.Context, w http.ResponseWriter,
	r *http.Request) bool {
	// Handle local request has path "/info"
	if r.Method == "GET" && !r.URL.IsAbs() && r.URL.Path == "/info" {
		w.Write([]byte("This is go-httpproxy."))
		return true
	}
	return false
}

func OnAuth(ctx *httpproxy.Context, authType string, user string, pass string) bool {
	// Auth test user.
	// if user == "test" && pass == "1234" {
	// 	return true
	// }
	return false
}

func OnConnect(ctx *httpproxy.Context, host string) (
	ConnectAction httpproxy.ConnectAction, newHost string) {
	// Apply "Man in the Middle" to all ssl connections. Never change host.
	return httpproxy.ConnectMitm, host
}

func OnRequest(ctx *httpproxy.Context, req *http.Request) (
	resp *http.Response) {
	// Log proxying requests.
	log.Printf("INFO: Proxy: %s %s", req.Method, req.URL.String())
	return
}

func OnResponse(ctx *httpproxy.Context, req *http.Request,
	resp *http.Response) {
	// Add header "Via: go-httpproxy".
	resp.Header.Add("Via", "go-httpproxy")
}

func InitProxy() {
	if Config.HttpProxyServerPort != 0 {
		prx, _ := httpproxy.NewProxy()
		// Set handlers.
		prx.OnError = OnError
		prx.OnAccept = OnAccept
		prx.OnAuth = OnAuth
		prx.OnConnect = OnConnect
		prx.OnRequest = OnRequest
		prx.OnResponse = OnResponse
		http.ListenAndServe(fmt.Sprintf(":%d", Config.HttpProxyServerPort), prx)
	}
}
