function collect(details) {
	console.log(details.url);
}

//chrome.runtime.onInstalled.addListener(function() {
chrome.webRequest.onCompleted.addListener(collect, {urls: ["<all_urls>"]});
//});
