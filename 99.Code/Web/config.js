var config = {
    apiRootUrl: "http://192.168.2.60:5000/"
};
var api = {
    token: "",
    
    get: (url) => {
        return fetch(config.apiRootUrl + url, { method: 'GET' }).then((res) => res.json());
    },

    post: (url, data) => {
        var request = new Request(config.apiRootUrl + url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return fetch(request).then((res) => { });
    },
};