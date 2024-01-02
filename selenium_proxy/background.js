var config = {
  mode: "fixed_servers",
  rules: {
    singleProxy: {
      scheme: "http",
      host: "38.170.190.247",
      port: parseInt("9598"),
    },
    bypassList: ["foobar.com"],
  },
};
chrome.proxy.settings.set({ value: config, scope: "regular" }, function () {});
function callbackFn(details) {
  return {
    authCredentials: {
      username: "spmcbdkr",
      password: "f2puv4moz6e1",
    },
  };
}

chrome.webRequest.onAuthRequired.addListener(
  callbackFn,
  { urls: ["<all_urls>"] },
  ["blocking"]
);


// "scripts": [
//     "background.js"
// ],
// "persistent": false