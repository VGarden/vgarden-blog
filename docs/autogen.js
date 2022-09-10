(async function() {
    function log() {
        console.log("autogen", ...arguments)
    }
    
    let [div, content] = await Promise.all([
        new Promise(resolve => document.addEventListener(
            "DOMContentLoaded", () => {
                log("Document is ready");
                resolve(document.getElementById("autogen_toc"))
            }
        )),
        
        (async function() {
            let headers = {
                'Accept': 'application/json'
            }
            /*
            See:
                https://developer.mozilla.org/en-US/docs/Web/API/fetch,
                https://developer.mozilla.org/en-US/docs/Web/API/Response
            */
            let response = await fetch("/vgarden-blog/navigation.json", { headers });
            log(response);
            if(! response.ok)
                throw "Unhandled error";
            
            return response.json();
        })()
    ])
    
    log(content);
    
    for(let ulContainer of div.querySelectorAll("ul")) {
        let dataFor = ulContainer.getAttribute("data-for");
        if(! dataFor) continue;
        
        for(let article of (content[dataFor] || [])) {
            let liElement = document.createElement("li");
            let aElement = document.createElement("a");
            aElement.setAttribute("href", article.hyperlink);
            aElement.textContent = article.name;
            liElement.appendChild(aElement);
            ulContainer.appendChild(liElement);
        }
    }
})()