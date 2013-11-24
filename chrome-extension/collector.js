endpoint = "http://localhost:5000/subdomains";

function collect(details) {
	var regex = /^([a-z]+):\/\/([a-z0-9\-]+)\.([a-z0-9\-]+)\.([a-z0-9\-]+)/
	try {
		console.log(details.url);
		subdomain = regex.exec(details.url)[2];
		console.log("Captured: " + subdomain)
		// Fire and forget.
		var xhr = new XMLHttpRequest();
		xhr.open("POST",endpoint,true);	
		xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
		xhr.send("name="+subdomain);
	} catch(e) {
		// I m lazy... not sure subdomains will always be parsed by the regex.
	}
	
}

//chrome.runtime.onInstalled.addListener(function() {
chrome.webRequest.onCompleted.addListener(collect, {urls: ["<all_urls>"]});
//});
