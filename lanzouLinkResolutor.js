const request = require('request')

function Resolve(LanzouLink, callback) {
    request(LanzouLink, null, (err, res, body) => {
        if (err) return
        SolveDownloadPageUri(body, (downloadPageUri) => {
            let downloadUrl = SolveDownloadUrl(downloadPageUri)
            callback(downloadUrl)
        })
    })

}

function SolveDownloadUrl(downloadPageUrl, callback) {
    request(downloadPageUrl, null, (err, res, body) => {
        let content = body
        let sign = ""
        let signValue = ""
        let data = ""
    
        // 获取Content中JS部分
        let jsRegex = new RegExp('<script type="text/javascript">\\n([\\S\\s]*?)</script>', 'g')
        let jsMatch = content.match(jsRegex)
    
        if (!jsMatch) {
            jsContent = jsMatch[0]
    
            // 注释替换表达式
            let descriptionRegex = new RegExp("//.*?[\\n]", 'g');
            let jsContent = jsContent.replace(descriptionRegex, "\n")
    
            // 获取data值
            let dataRegex = new RegExp("data : (.*?,'sign':(.*?),.*?})", 'g');
            let dataMatch = jsContent.match(dataRegex);
    
            if (!dataMatch) {
                let data = dataMatch[0];
                sign = dataMatch[1];
    
                //根据Sign获取Sign值
                let signRegex = new RegExp("var " + sign + " *?= *?'(.*?)';", 'g');
                let signMatch = jsContent.match(signRegex);
    
                if (!signMatch) {
                    signValue = signMatch[1];
                    data = data.replace("'sign':" + sign, "'sign':'" + signValue + "'");
                }
            }
        }
    
        //转化data为键值对
        // data = Json2FormData(data)
        // data = Encoding.UTF8.GetString(Encoding.Default.GetBytes(data))
        // let phpContent = PostAjax(data, downloadPageUrl)
    
        let options = {
            uri: downloadPageUrl,
            method: 'POST',
            json: data
        }
    
        request(options, function (error, response, body) {
            if (!error && response.statusCode == 200) {
                let phpContent = body
                let finalUrl = "";
                let domRegex = new RegExp("\"dom\":\"(.*)\",\"url\"", 'g')
                let urlRegex = new RegExp("\"url\":\"(.*)\",\"inf\"", 'g')
            
                let domMatch = phpContent.match(domRegex)
                let urlMatch = phpContent.match(urlRegex)
            
                if (domMatch.Success) {
                    finalUrl = domMatch[0].replace("\\", "")
                }
            
                finalUrl += "/file/"
            
                if (urlMatch.Success) {
                    finalUrl += urlMatch[0].replace("\\", "")
                }
            
                callback(finalUrl)
            }
        })
    })
}

function SolveDownloadPageUri(content) {
    let regex = new RegExp("<iframe class=\"ifr2\" name=\"[0-9]+\" src=\"(.+)\" frameborder=\"0\" scrolling=\"no\"></iframe>\n", 'g')
    let match = content.match(regex)
    let relativeUrl = ''
    if (!match) {
        relativeUrl = match[0]
    }

    if (relativeUrl !== '') {
        return "https://sdchao.lanzous.com" + relativeUrl
    }
    else
        return null
}


Resolve("https://wwe.lanzous.com/i9T15jhtm0h", (url) => {
    print(url)
})